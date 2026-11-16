from pathlib import Path
import numpy as np
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = Path(__file__).resolve().parents[1] / "data" / "processed"
COLS = ["idosos_sozinhos_pct", "dependencia_gt75_pct", "mulheres_chefes_pct"]


def _raw_path() -> Path:
    try:
        import xlrd  
        return RAW / "1179.xls"
    except ImportError:
        return RAW / "1179_convertido.xlsx"


def _read(sheet: str, nivel: str, ano: int) -> pd.DataFrame:
    df = pd.read_excel(_raw_path(), sheet_name=sheet, header=None, skiprows=6)
    if nivel == "RA":
        df = df.iloc[:, [0, 1, 2, 3, 4]]
        df.columns = ["codigo", "nome"] + COLS
    else:
        df = df.iloc[:, [0, 1, 2, 3]]
        df.columns = ["nome"] + COLS
        df.insert(0, "codigo", np.nan)
    for c in COLS:                                 
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=COLS, how="all").copy()   
    df["nome"] = df["nome"].astype(str).str.strip()
    df["codigo"] = pd.to_numeric(df["codigo"], errors="coerce").astype("Int64")
    df["nivel"], df["ano"] = nivel, ano
    return df


def build() -> pd.DataFrame:
    parts = [_read(f"{n}_{a}", "RA" if n == "RA" else "Bairro", a)
             for n, a in [("RA", 1991), ("RA", 2000), ("Bairros", 1991), ("Bairros", 2000)]]
    df = pd.concat(parts, ignore_index=True)
    df["agregado_municipal"] = (df["nivel"] == "RA") & (df["nome"].str.lower() == "rio de janeiro")
    return df[["nivel", "ano", "codigo", "nome", *COLS, "agregado_municipal"]]


def variacao(df: pd.DataFrame, nivel: str) -> pd.DataFrame:
    d = df[(df.nivel == nivel) & (~df.agregado_municipal)]
    w = d.pivot_table(index="nome", columns="ano", values=COLS)
    out = pd.DataFrame({c.replace("_pct", "_delta_pp"): w[(c, 2000)] - w[(c, 1991)] for c in COLS})
    return out.dropna().reset_index()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    df = build()
    df.to_csv(OUT / "indicadores_vulnerabilidade.csv.gz", index=False, compression="gzip")
    print(df.groupby(["nivel", "ano"]).size())
