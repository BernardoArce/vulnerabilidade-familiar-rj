
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
try:
    from . import etl
except ImportError:
    import etl

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
LAB = {"idosos_sozinhos_pct": "Idosos (65+) morando sozinhos (%)",
       "dependencia_gt75_pct": "Pessoas em famílias com razão de dependência > 75% (%)",
       "mulheres_chefes_pct": "Mulheres chefes de família sem cônjuge, filhos < 15 anos (%)"}
C91, C00 = "#9aa5b1", "#0b6e4f"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 130})


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ROOT / "data/processed/indicadores_vulnerabilidade.csv.gz")
    ra, bai = df[(df.nivel == "RA") & ~df.agregado_municipal], df[df.nivel == "Bairro"]
    mun = df[df.agregado_municipal].set_index("ano")[etl.COLS]
    res = {"municipio": {str(a): mun.loc[a].round(2).to_dict() for a in (1991, 2000)}}

    fig, ax = plt.subplots(figsize=(7, 3.6)); x = range(3); w = .38
    ax.bar([i - w/2 for i in x], mun.loc[1991], w, color=C91, label="1991")
    ax.bar([i + w/2 for i in x], mun.loc[2000], w, color=C00, label="2000")
    for i, c in enumerate(etl.COLS):
        for dx, a in ((-w/2, 1991), (w/2, 2000)):
            ax.text(i + dx, mun.loc[a, c] + .5, f"{mun.loc[a, c]:.1f}", ha="center", fontsize=9)
    ax.set_xticks(list(x)); ax.set_xticklabels(["Idosos\nsozinhos", "Dependência\n> 75%", "Mulheres\nchefes"])
    ax.set_ylabel("% da população de referência"); ax.legend(frameon=False); ax.set_title("Município do Rio de Janeiro, 1991 e 2000")
    fig.tight_layout(); fig.savefig(ASSETS / "fig1_municipio.png"); plt.close(fig)

    v = etl.variacao(df, "RA").sort_values("idosos_sozinhos_delta_pp")
    fig, ax = plt.subplots(figsize=(7, 7.2))
    ax.barh(v.nome, v.idosos_sozinhos_delta_pp, color=[C00 if d > 0 else "#b5452f" for d in v.idosos_sozinhos_delta_pp])
    ax.axvline(0, color="k", lw=.8); ax.set_xlabel("Variação 2000 − 1991 (pontos percentuais)")
    ax.set_title("Idosos morando sozinhos: variação por Região Administrativa"); ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout(); fig.savefig(ASSETS / "fig2_variacao_ra.png"); plt.close(fig)
    res["rq1"] = {"ras_aumento": int((v.idosos_sozinhos_delta_pp > 0).sum()), "n_ras": len(v),
                  "maior": v.iloc[-1][["nome", "idosos_sozinhos_delta_pp"]].tolist(),
                  "menor": v.iloc[0][["nome", "idosos_sozinhos_delta_pp"]].tolist(),
                  "mulheres_ras_queda": int((v.mulheres_chefes_delta_pp < 0).sum())}

   
    r0 = ra[ra.ano == 2000].set_index("nome")
    top = r0.sort_values("dependencia_gt75_pct")
    sel = pd.concat([top.head(5), top.tail(5)])
    fig, axs = plt.subplots(1, 2, figsize=(8.5, 3.8), sharey=True)
    for ax, c, col in zip(axs, ["dependencia_gt75_pct", "idosos_sozinhos_pct"], ["#b5452f", C00]):
        ax.barh(sel.index, sel[c], color=col); ax.set_title(LAB[c].split(" (")[0][:34] + " (%)", fontsize=9)
        ax.tick_params(axis="y", labelsize=8)
    fig.suptitle("RAs com menor e maior dependência familiar, 2000", fontsize=10)
    fig.tight_layout(); fig.savefig(ASSETS / "fig3_extremos_ra.png"); plt.close(fig)
    res["rq2"] = {"menores_dep": [[n, round(x, 1)] for n, x in top.dependencia_gt75_pct.head(3).items()],
                  "maiores_dep": [[n, round(x, 1)] for n, x in top.dependencia_gt75_pct.tail(3)[::-1].items()],
                  "maiores_idosos": [[n, round(x, 1)] for n, x in r0.idosos_sozinhos_pct.nlargest(3).items()],
                  "razao_dep": round(top.dependencia_gt75_pct.iloc[-1] / top.dependencia_gt75_pct.iloc[0], 2)}

  
    b = bai[bai.ano == 2000]
    rho1 = stats.spearmanr(b.idosos_sozinhos_pct, b.dependencia_gt75_pct)
    rho2 = stats.spearmanr(b.mulheres_chefes_pct, b.dependencia_gt75_pct)
    fig, axs = plt.subplots(1, 2, figsize=(8.5, 3.6))
    for ax, (cx, r) in zip(axs, [("idosos_sozinhos_pct", rho1), ("mulheres_chefes_pct", rho2)]):
        ax.scatter(b[cx], b.dependencia_gt75_pct, s=14, alpha=.7, color=C00)
        ax.set_xlabel(LAB[cx].split(" (")[0] + " (%)", fontsize=8); ax.set_title(f"Spearman ρ = {r.statistic:.2f}", fontsize=9)
    axs[0].set_ylabel("Dependência > 75% (%)")
    fig.suptitle(f"Bairros, 2000 (n = {len(b)})", fontsize=10); fig.tight_layout(); fig.savefig(ASSETS / "fig4_correlacao.png"); plt.close(fig)
    vb = etl.variacao(df, "Bairro"); b91 = bai[bai.ano == 1991].set_index("nome").loc[vb.nome]
    rho3 = stats.spearmanr(b91.idosos_sozinhos_pct.values, vb.idosos_sozinhos_delta_pp.values)
    res["rq3"] = {"n": len(b), "rho_idosos_dep": [round(rho1.statistic, 2), float(f"{rho1.pvalue:.2g}")],
                  "rho_mulheres_dep": [round(rho2.statistic, 2), float(f"{rho2.pvalue:.2g}")],
                  "rho_nivel91_delta": [round(rho3.statistic, 2), float(f"{rho3.pvalue:.2g}")]}
    (ROOT / "data/processed/resultados.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=1))
