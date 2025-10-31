
Coleta indicadores do panorama estadual no site https://cidades.ibge.gov.br/
(usando Playwright) e salva em `data/ibge_estados.xlsx`.

## Como rodar
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
playwright install
python scraper.py
