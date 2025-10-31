# IBGE Panorama Scraper (sem API)

Scraper em Python + Playwright que coleta os **cards do Panorama Estadual** no site do IBGE  
e salva em `data/ibge_estados.xlsx`. **Sem uso de API.**

## Como rodar
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
playwright install
python scraper.py

Observações

No panorama estadual, não existem cards de Saúde e Meio Ambiente → o script preenche "N/D".

O script ignora números que são apenas ano (ex.: 2019/2022) para evitar capturas erradas.