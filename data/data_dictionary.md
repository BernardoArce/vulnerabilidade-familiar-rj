# Dicionário de dados

**Arquivo:** `data/processed/indicadores_vulnerabilidade.csv.gz` (UTF-8, separador vírgula, 1 linha = 1 unidade territorial × 1 ano; 314 linhas)
**Fonte:** IPP, Armazém de Dados, Tabela 1179 — cálculos da Fundação João Pinheiro (Convênio IPP, IUPERJ, IPEA, 2003). Censos 1991 e 2000.

| Variável | Tipo | Formato / domínio | Significado |
|---|---|---|---|
| `nivel` | string | `RA` ou `Bairro` | Nível territorial da linha |
| `ano` | int | 1991 ou 2000 | Ano do Censo |
| `codigo` | Int64 (nulável) | 1–33 para RAs; vazio para bairros e agregado | Código da Região Administrativa |
| `nome` | string | texto livre | Nome da unidade (bairros podem vir agrupados, ex.: "Botafogo, Urca") |
| `idosos_sozinhos_pct` | float | 0–100 | % de pessoas com 65 anos ou mais que vivem sozinhas em domicílio particular permanente |
| `dependencia_gt75_pct` | float | 0–100 | % de pessoas em famílias cuja razão de dependência (membros de 0–14 e 65+ ÷ membros de 15–64) é maior que 0,75 |
| `mulheres_chefes_pct` | float | 0–100 | % de mulheres chefes de família, sem cônjuge, com filhos menores de 15 anos em casa |
| `agregado_municipal` | bool | True/False | True na linha que representa o município do Rio de Janeiro como um todo (excluir de rankings de RAs) |

**Variável derivada (calculada em `etl.variacao`, não persistida):** `*_delta_pp` = valor de 2000 − valor de 1991, em pontos percentuais.

**Observações:** a fonte informa que Paquetá não tem dados suficientes em 1991; as divisões territoriais de 1991 seguem a malha disponível na época e podem não coincidir exatamente com as de 2000.
