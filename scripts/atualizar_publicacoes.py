#!/usr/bin/env python3
"""Busca na OpenAlex os artigos dos professores do laboratório.

Grava o resultado em data/publicacoes.json, que a página publicacoes.html lê.

Uso:
    python3 scripts/atualizar_publicacoes.py

Só usa a biblioteca padrão do Python.
"""
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import date

API = "https://api.openalex.org/works"
CONTATO = "labmet-ufopa@users.noreply.github.com"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "data", "publicacoes.json")

ANO_INICIAL = 2013

# A OpenAlex divide a produção de uma mesma pessoa em vários perfis e, às
# vezes, mistura homônimos. Por isso cada professor tem uma lista de perfis
# e um padrão que o nome, como aparece no artigo, precisa atender.
PROFESSORES = [
    {
        "nome": "Julio Tota",
        "perfis": ["A5107225494", "A5107247453", "A5046440248", "A5073205744",
                   "A5010771375", "A5143401118", "A5140865608"],
        "padrao": r"^(j(\.|[uú]lio)?\b.*t[oó]ta|t[oó]ta.*,\s*j)",
        "padrao_extra": r"^julio t\. silva$",
    },
    {
        "nome": "Antonio Marcos Andrade",
        "perfis": ["A5068434340"],
        "padrao": r"ant[oô]nio.*andrade|andrade.*,\s*a|^a\..*andrade",
        "padrao_extra": None,
    },
    {
        "nome": "Helvecio Neto",
        "perfis": ["A5052835164", "A5005219507"],
        "padrao": r"helv[eé]cio|^h\..*neto",
        "padrao_extra": None,
    },
]

# Artigos fora dos temas do laboratório (saúde, qualidade da água, uso da
# terra) ou registros que não são artigos. Inclua aqui o DOI para retirar.
EXCLUIR = {
    "10.14393/hygeia2069916",
    "10.12957/tamoios.2023.58887",
    "10.33448/rsd-v11i4.27359",
    "10.6008/cbpc2179-6858.2020.007.0044",
    "10.11137/2020_2_277_288",
    "10.5902/2179460x34097",
    "10.6008/cbpc2179-6858.2018.005.0030",
    "10.5380/abclima.v23i0.50256",
    "10.5902/2179460x19691",
    "10.1159/000275286",
    "10.21680/2447-3359.2021v7n2id24543",
    "10.21438/rbgas(2021)081939",   # artigo retratado
    "10.26848/rbgf.v10.6.p057-069",  # registro duplicado
}

FONTES_IGNORADAS = ("agu fall meeting", "agufm", "biblioteca digital", "ssrn", "figshare")

SIGLAS = {"co2", "wrf", "gfs", "sib", "goamazon", "atto", "mgb-iph", "enos", "pa", "am"}


def buscar(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"labmet-site (mailto:{CONTATO})"})
    ultimo = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60, context=ssl.create_default_context()) as r:
                return json.loads(r.read())
        except Exception as erro:  # rede instável: tenta de novo
            ultimo = erro
    raise SystemExit(f"Não foi possível consultar a OpenAlex: {ultimo}")


def obras_do_perfil(perfil):
    cursor = "*"
    campos = "id,doi,title,publication_year,type,primary_location,authorships,cited_by_count,open_access"
    while cursor:
        url = (f"{API}?filter=author.id:{perfil},type:article,from_publication_date:{ANO_INICIAL}-01-01"
               f"&per-page=200&select={campos}&cursor={urllib.parse.quote(cursor)}")
        dados = buscar(url)
        for obra in dados.get("results", []):
            yield obra
        cursor = dados.get("meta", {}).get("next_cursor") if dados.get("results") else None


def arrumar_titulo(titulo):
    titulo = re.sub(r"<[^>]+>", "", titulo or "").strip()
    titulo = re.sub(r"\s+", " ", titulo)
    letras = [c for c in titulo if c.isalpha()]
    if letras and sum(c.isupper() for c in letras) / len(letras) > 0.7:
        palavras = titulo.lower().split(" ")
        palavras = [p.upper() if p.strip("():,.;") in SIGLAS else p for p in palavras]
        titulo = " ".join(palavras)
        titulo = titulo[0].upper() + titulo[1:]
        titulo = re.sub(r"([:.]\s+)([a-zà-ú])", lambda m: m.group(1) + m.group(2).upper(), titulo)
    for errado, certo in (("amazônia", "Amazônia"), ("amazonia", "Amazonia"), ("li-7500a", "LI-7500A"),
                          ("santarém", "Santarém"), ("pará", "Pará"), ("brasil", "Brasil")):
        titulo = re.sub(rf"\b{errado}\b", certo, titulo)
    return titulo.rstrip(".")


def nome_curto(nome):
    nome = re.sub(r"\s+", " ", nome or "").strip()
    if "," in nome:
        sobrenome, resto = [p.strip() for p in nome.split(",", 1)]
        nome = f"{resto} {sobrenome}"
    if nome.isupper():
        nome = nome.title()
    return nome


def main():
    publicacoes = {}
    for prof in PROFESSORES:
        for perfil in prof["perfis"]:
            for obra in obras_do_perfil(perfil):
                doi = (obra.get("doi") or "").replace("https://doi.org/", "").lower()
                fonte = ((obra.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
                if not doi or not fonte or doi in EXCLUIR:
                    continue
                if any(f in fonte.lower() for f in FONTES_IGNORADAS):
                    continue

                autores, do_professor = [], False
                for a in obra.get("authorships", []):
                    nome = a.get("raw_author_name") or (a.get("author") or {}).get("display_name") or ""
                    perfil_autor = ((a.get("author") or {}).get("id") or "").split("/")[-1]
                    do_lab = False
                    if perfil_autor in prof["perfis"]:
                        n = nome.lower().strip()
                        if re.search(prof["padrao"], n) or (prof["padrao_extra"] and re.search(prof["padrao_extra"], n)):
                            do_lab = do_professor = True
                    autores.append({"nome": nome_curto(nome), "lab": do_lab})
                if not do_professor:
                    continue

                item = publicacoes.get(doi)
                if item:
                    # o mesmo artigo pode ter dois professores do laboratório
                    for novo, antigo in zip(autores, item["autores"]):
                        antigo["lab"] = antigo["lab"] or novo["lab"]
                    if prof["nome"] not in item["professores"]:
                        item["professores"].append(prof["nome"])
                    continue

                publicacoes[doi] = {
                    "titulo": arrumar_titulo(obra.get("title")),
                    "ano": obra.get("publication_year"),
                    "periodico": fonte,
                    "doi": doi,
                    "autores": autores,
                    "professores": [prof["nome"]],
                    "citacoes": obra.get("cited_by_count", 0),
                    "acesso_aberto": bool((obra.get("open_access") or {}).get("is_oa")),
                }

    lista = sorted(publicacoes.values(), key=lambda p: (-p["ano"], p["titulo"].lower()))
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump({"atualizado_em": date.today().isoformat(), "fonte": "OpenAlex",
                   "ano_inicial": ANO_INICIAL, "publicacoes": lista}, f, ensure_ascii=False, indent=1)
    print(f"{len(lista)} publicações gravadas em {os.path.relpath(SAIDA, RAIZ)}")
    return lista


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
