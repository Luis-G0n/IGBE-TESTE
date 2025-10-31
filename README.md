# IBGE Panorama Scraper (sem API)

Script em **Python + Playwright** que coleta os **cards do Panorama Estadual** no site do IBGE  
e salva em `data/ibge_estados.xlsx`. **Não usa APIs** — é navegação e extração do HTML.

## ✅ Indicadores coletados
- **População**
- **Trabalho e Rendimento**
- **Educação**
- **Economia**
- **Território**
- **Saúde** → _no panorama estadual não existe cartão_; o script preenche **`N/D`**
- **Meio Ambiente** → _no panorama estadual não existe cartão_; o script preenche **`N/D`**

> Se quiser capturar “Saúde/Meio Ambiente” para municípios, basta adaptar para clicar em **Selecionar local** e navegar até a página municipal.

---

## ⚙️ Requisitos
- Python 3.10+
- O navegador será baixado pelo Playwright

---

## 🚀 Como rodar

```bash
# 1) criar e ativar o ambiente (Windows/macOS/Linux)
python -m venv .venv
# Windows:
.\.venv\Scriptsctivate
# macOS/Linux:
source .venv/bin/activate

# 2) instalar dependências
pip install -r requirements.txt
playwright install

# 3) executar
python scraper.py
```

Saída padrão: `data/ibge_estados.xlsx`

---

## 🧩 Estrutura do projeto
```
.
├─ scraper.py
├─ requirements.txt
├─ .gitignore
├─ README.md
└─ data/
   └─ ibge_estados.xlsx
```

---

## 🔎 Como funciona (resumo técnico)
- Abre `https://cidades.ibge.gov.br/brasil/{uf}` para cada UF.
- Para cada rótulo-alvo, localiza o **card** pelo texto e extrai o **valor mais informativo**.
- A heurística **ignora números que são apenas ano** (ex.: 2019/2022) para evitar capturas erradas.
- Se o rótulo **não existir** na página (caso de “Saúde/Meio Ambiente” no estado), preenche **`N/D`**.

---

## 🛠️ Opções rápidas (editar no final do `scraper.py`)
```python
# visualizar o navegador durante a execução:
main(out_path="data/ibge_estados.xlsx", headed=True, delay_ms=150)
# padrão headless:
main(out_path="data/ibge_estados.xlsx", headed=False, delay_ms=0)
```

---

## ❗ Troubleshooting
- **Planilha não move / erro de arquivo em uso**: feche o Excel e rode de novo.
- **Playwright não encontra navegador**: rode `playwright install`.
- **Firewall/Proxy corporativo**: pode bloquear o download do navegador — tente em rede doméstica.

---

## 📄 Licença
MIT — use à vontade para estudos e testes técnicos.
