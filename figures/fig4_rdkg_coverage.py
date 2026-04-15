import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

TOTAL = 26_106

labels = [
    "HPO phenotypes\n(HPOA)",
    "Drug annotation\n(TREATS/CONTRA)",
    "Orphanet ID\n(xref)",
    "Phenotype + drug\n(both sources)",
    "Gene association\n(OMIM/ClinVar)",
]
counts = [11_926, 5_288, 2_660, 1_596, 206]
pcts   = [round(c / TOTAL * 100, 1) for c in counts]
remain = [round(100 - p, 1) for p in pcts]

COL_A  = "#7F77DD"
COL_U  = "#D3D1C7"
COL_AB = "#534AB7"
COL_UB = "#B4B2A9"
COL_TX = "#2C2C2A"
COL_MU = "#5F5E5A"
COL_GR = "#EBEBEB"

fig, ax = plt.subplots(figsize=(7.5, 4.8))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

x = np.arange(len(labels))
w = 0.52

bars_a = ax.bar(x, pcts,   width=w, color=COL_A,  edgecolor=COL_AB, linewidth=0.5, zorder=3)
bars_u = ax.bar(x, remain, width=w, bottom=pcts,
                color=COL_U, edgecolor=COL_UB, linewidth=0.5, zorder=3)

for bar, pct, cnt in zip(bars_a, pcts, counts):
    # percentage inside bar
    if pct >= 8:
        ax.text(bar.get_x() + w/2, pct/2,
                f"{pct}%", ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="white", zorder=4)
    else:
        ax.text(bar.get_x() + w/2, pct + 1.2,
                f"{pct}%", ha="center", va="bottom",
                fontsize=9, color=COL_A, fontweight="bold", zorder=4)
    # n= label above full bar
    ax.text(bar.get_x() + w/2, 102,
            f"n={cnt:,}", ha="center", va="bottom",
            fontsize=8, color=COL_MU, zorder=4)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9, color=COL_TX, multialignment="center", linespacing=1.4)
ax.set_ylim(0, 113)
ax.set_ylabel("% of all diseases in RDKG", fontsize=9, color=COL_MU, labelpad=8)
ax.yaxis.set_tick_params(labelsize=8.5, labelcolor=COL_MU)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.yaxis.grid(True, color=COL_GR, linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
ax.spines[["top","right","left"]].set_visible(False)
ax.spines["bottom"].set_color(COL_GR)
ax.tick_params(axis="x", length=0, pad=8)
ax.tick_params(axis="y", length=0)

pa = mpatches.Patch(facecolor=COL_A, edgecolor=COL_AB, linewidth=0.5, label="Annotated")
pu = mpatches.Patch(facecolor=COL_U, edgecolor=COL_UB, linewidth=0.5, label="Unannotated")
ax.legend(handles=[pa, pu], loc="upper right", fontsize=9,
          frameon=True, framealpha=0.95, edgecolor=COL_GR, fancybox=False)

ax.text(0.5, 1.03,
        f"Total: {TOTAL:,} diseases  ·  72,368 nodes  ·  834,260 edges  ·  15 relationship types",
        transform=ax.transAxes, ha="center", va="bottom",
        fontsize=8, color=COL_MU, style="italic")

plt.tight_layout(rect=[0, 0, 1, 0.97])
out = "./figures/fig4_rdkg_coverage.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
plt.close(fig)
print(f"Saved: {out}")
