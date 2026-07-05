#!/usr/bin/env python3
"""
kcell.py — core comun de las celdas de conocimiento del proyecto (patron estrangulador).

Una celda de conocimiento (ALE, AzerothCore, ...) es el MISMO sistema de 2 capas:
  Capa 1 (map)    -> emite mapa base + contratos de un dominio (contexto inyectable).
  Capa 2 (search) -> retrieval lexico BM25-lite sobre chunks, boost a la linea PREGUNTAS.
  lookup          -> ficha exacta por nombre (O(1) sobre un indice by_name).

Historicamente cada celda tenia su tool duplicada (ale.py, acw.py) con ~80% identico. Este
modulo extrae ese core; cada tool queda como thin wrapper que instancia KnowledgeCell con su
`cell.json`. Sin dependencias (stdlib), local-first, contrato del toolkit (describe/summary,
exit 0/1/2).

`cell.json` (junto a la tool de cada celda) declara lo que difiere entre celdas:
  {
    "tool": "acw",
    "cell": "azerothcore",
    "wow_version": "3.3.5a (build 12340)",
    "description": "...",
    "artifacts_dir": "artifacts",
    "index_file": "acw-index.json",
    "chunks_file": "chunks.jsonl",
    "core_flag": "gm_core",            # campo booleano de metadata que marca el nucleo del dominio
    "core_flag_cli": "gm-core",        # nombre del flag CLI (--gm-core)
    "domain_maps": {                   # dominios con Capa 1 curada -> (mapa, contratos)
      "cuentas-gm": ["mapa-cuentas-gm.md", "CONTRATOS-CUENTAS-GM.md"]
    }
  }

NOTA (paridad): la celda ALE (ale.py / eluna-index.json) NO migra a kcell hasta que una
pasada de paridad demuestre output identico (diff de map/lookup/search sobre casos reales).
Su indice usa methods/hooks (no by_name) y un lookup rico; ese modo se agrega como override
cuando se migre, con OK del orquestador. Por ahora kcell sirve a las celdas de indice by_name.
"""
import os
import re
import sys
import json
import math
import argparse
from collections import Counter

VERSION = "1.0.0"
SCHEMA_VERSION = 1

# El contenido emite markdown con simbolos UTF-8; en Windows el stdout arranca en cp1252 y
# rompe con UnicodeEncodeError. Forzamos UTF-8 para que map/lookup/search sean seguros.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


_TOKEN = re.compile(r"[a-z0-9_]+")

# Palabras vacias (es/en) que solo aportan ruido al ranking: un chunk corto sin ningun termino
# de contenido puede ganar por su alto TF-relativo de stopwords. Se excluyen de la QUERY (no del
# indexado de los chunks) -> las queries tecnicas de ALE (sin stopwords) quedan intactas.
_STOP = frozenset("""
a al ante bajo con contra de del desde donde durante e el en entre es esta este esto hacia hasta
la las le les lo los mas me mi mis no nos o para pero por porque que se si sin sobre su sus te
tu un una uno unos unas y ya
a an and are as at be by for from how in into is it of on or that the this to what when where which
""".split())


def _tokens(text):
    return _TOKEN.findall(text.lower())


def _query_tokens(text):
    """Tokens de la query sin stopwords; si todo era stopword, cae a los tokens crudos."""
    toks = [t for t in _tokens(text) if t not in _STOP]
    return toks or _tokens(text)


def _split_chunk(text):
    """Separa el cuerpo del chunk de su linea PREGUNTAS (para poder darle boost)."""
    m = re.search(r"\nPREGUNTAS:\s*(.*)$", text, re.S)
    preguntas = m.group(1) if m else ""
    body = text[:m.start()] if m else text
    return body, preguntas


class KnowledgeCell:
    """Una celda de conocimiento parametrizada por su cell.json. `base` = dir de la tool."""

    def __init__(self, config, base):
        self.cfg = config
        self.base = base
        self.art = os.path.join(base, config.get("artifacts_dir", "artifacts"))
        self.index_path = os.path.join(self.art, config["index_file"])
        self.chunks_path = os.path.join(self.art, config["chunks_file"])
        self.core_flag = config.get("core_flag")            # p.ej. "gm_core"
        self.domain_maps = config.get("domain_maps", {})

    # ------------------------- carga -------------------------

    def load_index(self):
        with open(self.index_path, encoding="utf-8") as f:
            return json.load(f)

    def load_chunks(self):
        out = []
        with open(self.chunks_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    # ------------------------- describe / summary -------------------------

    def cmd_describe(self, as_json):
        cli = self.cfg.get("core_flag_cli", "core")
        d = {
            "tool": self.cfg["tool"],
            "version": VERSION,
            "schema_version": SCHEMA_VERSION,
            "role": "knowledge_cell",
            "description": self.cfg["description"],
            "commands": [
                {"name": "map", "args": [f"--domain {next(iter(self.domain_maps), 'DOMAIN')}"],
                 "description": "Emit Capa 1 base context (mapa + contratos) for a domain",
                 "token_cost_estimate": "medium"},
                {"name": "lookup", "args": ["NAME"],
                 "description": "Exact card by name (command / table / procedure / method)",
                 "token_cost_estimate": "low"},
                {"name": "search", "args": ["QUERY", "--category C", f"--{cli}", "--gotcha", "--k N"],
                 "description": "Lexical retrieval over chunks (Capa 2), boosts PREGUNTAS synonyms",
                 "token_cost_estimate": "low"},
            ],
            "outputs": ["stdout"],
            "consumes": [f"{self.cfg.get('artifacts_dir', 'artifacts')}/{self.cfg['index_file']}",
                         f"{self.cfg.get('artifacts_dir', 'artifacts')}/{self.cfg['chunks_file']}"],
            "supports_json": True,
        }
        print(json.dumps(d, ensure_ascii=False, indent=2) if as_json else d["description"])
        return 0

    def cmd_summary(self, as_json):
        try:
            idx = self.load_index()
            chunks = self.load_chunks()
        except FileNotFoundError as e:
            self._err(f"artefacto faltante: {e}")
            return 1
        meta = idx.get("_meta", {})
        core = sum(1 for c in chunks if self.core_flag and c["metadata"].get(self.core_flag))
        gotcha = sum(1 for c in chunks if c["metadata"].get("has_gotcha"))
        cats = Counter(c["metadata"]["category"] for c in chunks)
        # nombre "bonito" para el resumen humano; cae al _meta.cell / cfg.cell
        display = self.cfg.get("cell_display", meta.get("cell", self.cfg.get("cell")))
        s = {
            "tool": self.cfg["tool"],
            "schema_version": SCHEMA_VERSION,
            "cell": meta.get("cell", self.cfg.get("cell")),
            "wow_version": meta.get("wow_version", self.cfg.get("wow_version")),
            "domains_enriched": meta.get("domains_enriched", list(self.domain_maps)),
            "chunks": len(chunks),
            "commands": len(idx.get("commands", {})),
            "tables": len(idx.get("tables", {})),
            "procedures": len(idx.get("procedures", {})),
            "with_gotcha": gotcha,
            "categories": dict(cats),
        }
        # cuenta del nucleo bajo su nombre real (gm_core/econ_core) para no romper consumidores
        if self.core_flag:
            s[self.core_flag] = core
        if as_json:
            print(json.dumps(s, ensure_ascii=False, indent=2))
        else:
            print(f"{self.cfg['tool']} {VERSION} | {display} {s['wow_version']} | dominios: "
                  f"{', '.join(s['domains_enriched'])} | {s['chunks']} chunks "
                  f"({s['commands']} cmd, {s['tables']} tbl, {s['procedures']} proc, {gotcha} gotcha)")
        return 0

    # ------------------------- map (Capa 1) -------------------------

    def cmd_map(self, domain):
        if domain not in self.domain_maps:
            self._err(f"dominio '{domain}' sin capa 1 curada todavía. "
                      f"Disponibles: {', '.join(self.domain_maps) or '(ninguno)'} "
                      f"(ver PROCEDIMIENTO-ENRIQUECIMIENTO.md).")
            return 2
        parts = []
        for fname in self.domain_maps[domain]:
            p = os.path.join(self.art, fname)
            if not os.path.exists(p):
                self._err(f"falta {p}")
                return 1
            with open(p, encoding="utf-8") as f:
                parts.append(f.read())
        print("\n\n---\n\n".join(parts))
        return 0

    # ------------------------- lookup (index by_name) -------------------------

    def cmd_lookup(self, name, as_json):
        idx = self.load_index()
        chunks = {c["id"]: c for c in self.load_chunks()}
        key = name.lower()
        cid = idx.get("by_name", {}).get(key)
        if cid and cid in chunks:
            c = chunks[cid]
            if as_json:
                print(json.dumps({"id": c["id"], "metadata": c["metadata"], "text": c["text"]},
                                 ensure_ascii=False, indent=2))
            else:
                print(c["text"])
            return 0
        cand = [n for n in idx.get("by_name", {}) if key in n][:8]
        self._err(f"'{name}' no encontrado." + (f" ¿Quisiste?: {', '.join(cand)}" if cand else ""))
        return 1

    # ------------------------- search (Capa 2 lexica) -------------------------

    def cmd_search(self, query, category, core, gotcha, k, as_json):
        chunks = self.load_chunks()

        def keep(c):
            md = c["metadata"]
            if category and md["category"] != category:
                return False
            if core and not (self.core_flag and md.get(self.core_flag)):
                return False
            if gotcha and not md.get("has_gotcha"):
                return False
            return True

        pool = [c for c in chunks if keep(c)]
        if not pool:
            self._err("ningun chunk pasa el filtro")
            return 1

        q = _query_tokens(query)
        if not q:
            self._err("query vacia")
            return 2

        N = len(pool)
        df = Counter()
        docs = []
        for c in pool:
            body, preg = _split_chunk(c["text"])
            tf = Counter(_tokens(body))
            for t, n in Counter(_tokens(preg)).items():
                tf[t] += n * 3           # boost a los sinonimos de intencion (PREGUNTAS)
            docs.append(tf)
            for t in tf:
                df[t] += 1
        idf = {t: math.log(1 + N / (1 + df[t])) for t in df}

        scored = []
        for c, tf in zip(pool, docs):
            total = sum(tf.values()) or 1
            score = 0.0
            for t in q:
                if t in tf:
                    score += (tf[t] / total) * idf.get(t, 0)
            name = (c["metadata"].get("name")
                    or c["metadata"].get("method")
                    or c["metadata"].get("event_const") or "").lower()
            for t in q:
                if t in name:
                    score += 0.15
            if score > 0:
                scored.append((score, c))
        scored.sort(key=lambda x: -x[0])
        top = scored[:k]

        if not top:
            self._err("sin resultados")
            return 1
        if as_json:
            print(json.dumps([{"score": round(s, 4), "id": c["id"],
                               "metadata": c["metadata"], "text": c["text"]}
                              for s, c in top], ensure_ascii=False, indent=2))
        else:
            for s, c in top:
                print(f"\n### score={s:.3f}  id={c['id']}")
                print(c["text"])
        return 0

    # ------------------------- util -------------------------

    def _err(self, msg):
        sys.stderr.write(f"[{self.cfg['tool']}] {msg}\n")

    # ------------------------- dispatch (argparse compartido) -------------------------

    def run(self, argv=None):
        cli = self.cfg.get("core_flag_cli", "core")
        ap = argparse.ArgumentParser(prog=self.cfg["tool"], description=self.cfg["description"])
        ap.add_argument("--describe", action="store_true")
        ap.add_argument("--summary", action="store_true")
        ap.add_argument("--format", choices=["text", "json"], default="text")
        sub = ap.add_subparsers(dest="cmd")

        p_map = sub.add_parser("map")
        p_map.add_argument("--domain", default=next(iter(self.domain_maps), None))

        p_look = sub.add_parser("lookup")
        p_look.add_argument("name")

        p_search = sub.add_parser("search")
        p_search.add_argument("query")
        p_search.add_argument("--category")
        p_search.add_argument(f"--{cli}", dest="core", action="store_true")
        p_search.add_argument("--gotcha", action="store_true")
        p_search.add_argument("--k", type=int, default=5)

        args = ap.parse_args(argv)
        as_json = args.format == "json"

        if args.describe:
            return self.cmd_describe(as_json)
        if args.summary:
            return self.cmd_summary(as_json)
        if args.cmd == "map":
            return self.cmd_map(args.domain)
        if args.cmd == "lookup":
            return self.cmd_lookup(args.name, as_json)
        if args.cmd == "search":
            return self.cmd_search(args.query, args.category, args.core,
                                   args.gotcha, args.k, as_json)
        ap.print_help()
        return 2


def load_cell(base):
    """Carga cell.json ubicado junto a la tool (en `base`) y devuelve una KnowledgeCell."""
    with open(os.path.join(base, "cell.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    return KnowledgeCell(cfg, base)
