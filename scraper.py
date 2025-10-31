import re
import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright

TARGET_LABELS = [
    "População",
    "Trabalho e Rendimento",
    "Educação",
    "Economia",
    "Saúde",          # não existe no panorama do ESTADO
    "Meio Ambiente",  # não existe no panorama do ESTADO
    "Território",
]

BRAZIL_STATES = [
    ("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"),
    ("BA", "Bahia"), ("CE", "Ceará"), ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"), ("GO", "Goiás"), ("MA", "Maranhão"),
    ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"), ("MG", "Minas Gerais"),
    ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"), ("PE", "Pernambuco"),
    ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"),
    ("SC", "Santa Catarina"), ("SP", "São Paulo"), ("SE", "Sergipe"),
    ("TO", "Tocantins"),
]

BASE_URL = "https://cidades.ibge.gov.br/brasil/{uf}"
NOT_FOUND = "N/D"

# ======= FUNÇÕES UTIL (corrigidas) =======
# valor: 1.234.567,89 | 987.654 | 123 | 45,6
RE_VALUE = re.compile(r"\b\d{1,3}(?:\.\d{3})*(?:,\d+)?\b")
# ano: 2019, 2020, 2021, 2022, 2023, 2024...
RE_YEAR  = re.compile(r"\b(?:19|20)\d{2}\b")

def parse_values(text: str):
    if not text:
        return []
    vals = RE_VALUE.findall(text)
    vals = [v for v in vals if not RE_YEAR.fullmatch(v)]
    return vals

def pick_best(values):
    if not values:
        return None
    def score(v):
        return (',' in v, v.count('.'), len(v))
    return sorted(values, key=score, reverse=True)[0]

def extract_label_value(page, label: str):
    locs = page.locator(f"text={label}")
    count = locs.count()
    if count == 0:
        return NOT_FOUND  # bloco não existe nessa página - IMPORTANTE

    for i in range(count):
        handle = locs.nth(i)
        container = handle.locator("xpath=ancestor-or-self::*[self::* or self::div][1]")
        try:
            text = container.inner_text()
            best = pick_best(parse_values(text))
            if best:
                return best

            for k in range(1, 6):
                sib = handle.locator(f"xpath=following::*[{k}]")
                try:
                    stext = sib.inner_text()
                    best = pick_best(parse_values(stext))
                    if best:
                        return best
                except Exception:
                    continue
        except Exception:
            continue

    try:
        box = locs.first
        next_block = box.locator("xpath=following::*[self::div or self::section or self::li or self::p][1]")
        text = next_block.inner_text()
        best = pick_best(parse_values(text))
        return best if best else NOT_FOUND
    except Exception:
        return NOT_FOUND

def main(out_path="data/ibge_estados.xlsx", headed=False, delay_ms=0):
    os.makedirs("data", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed, slow_mo=delay_ms)
        context = browser.new_context()
        page = context.new_page()

        rows = []
        for uf, nome in BRAZIL_STATES:
            url = BASE_URL.format(uf=uf.lower())
            print(f"[{uf}] Acessando {url} ...")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass

                row = {"UF": uf, "Estado": nome}
                for label in TARGET_LABELS:
                    try:
                        val = extract_label_value(page, label)
                    except Exception:
                        val = NOT_FOUND
                    row[label] = val or NOT_FOUND

                rows.append(row)
            except Exception as e:
                print(f"[{uf}] Erro: {e}")
                row = {"UF": uf, "Estado": nome}
                for label in TARGET_LABELS:
                    row[label] = NOT_FOUND
                rows.append(row)

            time.sleep(0.5)

        context.close()
        browser.close()

    df = pd.DataFrame(rows, columns=["UF", "Estado"] + TARGET_LABELS)
    df.to_excel(out_path, index=False)
    print(f"\n✅ Arquivo salvo em: {out_path}")

if __name__ == "__main__":
    main(out_path="data/ibge_estados.xlsx", headed=False, delay_ms=0)
