# Vulnerabilidade da situação familiar no Rio de Janeiro (Censos 1991 e 2000)

Projeto final — Bacharelado em Sistemas de Informação, 6º período, *Linguagem de Programação*.
**Autores:** [Bernardo Teixeira de Oliveira Arce] · **Instituição:** [Uni La Salle] · **Semestre:** [2026.2]
**Artigo (GitHub Pages):** https://BernardoArce.github.io/vulnerabilidade-familiar-rj/

## Resumo executivo
Análise de três indicadores de vulnerabilidade familiar (idosos morando sozinhos, dependência familiar elevada e mulheres chefes de família com filhos pequenos) por Região Administrativa e bairro do Rio de Janeiro em 1991 e 2000. Respondemos a três perguntas de pesquisa sobre evolução temporal, distribuição territorial e associação entre indicadores.

**Palavras-chave:** vulnerabilidade familiar; envelhecimento; Rio de Janeiro; Censo demográfico; ciência aberta; FAIR.

## Dados
Fonte original: Instituto Pereira Passos, *Armazém de Dados*, Tabela 1179 (cálculos da Fundação João Pinheiro). Link perene: https://www.data.rio/ (buscar "Tabela 1179"). Arquivo bruto em `data/raw/1179.xls`.

## Estrutura
```
data/raw/        dados originais (.xls) + cópia convertida (.xlsx)
data/processed/  CSV comprimido + resultados.json
data/data_dictionary.md
notebooks/analise_exploratoria.ipynb
src/etl.py  src/analysis.py  src/build_article.py
docs/index.html  docs/assets/   (artigo, publicado via GitHub Pages)
```

## Como reproduzir
```bash
python -m venv .venv && source .venv/bin/activate  
pip install -r requirements.txt
python src/etl.py && python src/analysis.py && python src/build_article.py
```
Abra `docs/index.html` no navegador. Para publicar: *Settings → Pages → Deploy from branch → `main` / `/docs`*.

## Licenças
Código: MIT (`LICENSE`). Dados processados e texto: CC BY 4.0. Dados brutos: termos da fonte original.
