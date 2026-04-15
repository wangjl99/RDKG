"""
generate_all_figures.py
=======================
Generates all publication figures for the RDKG paper at 300 DPI.
Output saved to ./figures/ in the same directory as this script.

Usage:
    cd /Users/jwang58/Downloads/RDKG
    pip install matplotlib numpy
    python figures/generate_all_figures.py

Figures generated:
    fig1_architecture.png        — System architecture (pipeline overview)
    fig2_query_workflow.png      — Phenotype-driven query workflow
    fig3_harmonization.png       — Before/after semantic harmonization
    fig4_coverage.png            — Annotation coverage statistics
    fig5_inheritance_similarity.png — Inheritance + phenotypic similarity
    fig6_drug_repurposing.png    — Drug repurposing candidates (Marfan)
"""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

# Output directory = figures/ next to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = SCRIPT_DIR
os.makedirs(OUT_DIR, exist_ok=True)

def out(filename):
    return os.path.join(OUT_DIR, filename)

# ── Shared style ──────────────────────────────────────────────────────────────
COL = {
    "purple":    "#7F77DD",
    "purple_b":  "#534AB7",
    "purple_l":  "#AFA9EC",
    "teal":      "#5DCAA5",
    "teal_b":    "#0F6E56",
    "teal_l":    "#9FE1CB",
    "amber":     "#EF9F27",
    "amber_l":   "#FAC775",
    "gray":      "#D3D1C7",
    "gray_b":    "#B4B2A9",
    "text":      "#2C2C2A",
    "muted":     "#5F5E5A",
    "grid":      "#EBEBEB",
    "white":     "#FFFFFF",
}

def style_ax(ax):
    ax.set_facecolor(COL["white"])
    ax.spines[["top","right","left"]].set_visible(False)
    ax.spines["bottom"].set_color(COL["grid"])
    ax.tick_params(axis="both", length=0)
    ax.yaxis.grid(True, color=COL["grid"], linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)


# ════════════════════════════════════════════════════════════════════════════
# Figure 4 — Annotation coverage
# ════════════════════════════════════════════════════════════════════════════
def fig4_coverage():
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

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    fig.patch.set_facecolor(COL["white"])
    ax.set_facecolor(COL["white"])

    x = np.arange(len(labels))
    w = 0.52
    ax.bar(x, pcts,   width=w, color=COL["purple"],
           edgecolor=COL["purple_b"], linewidth=0.5, zorder=3,
           label="Annotated")
    ax.bar(x, remain, width=w, bottom=pcts,
           color=COL["gray"], edgecolor=COL["gray_b"],
           linewidth=0.5, zorder=3, label="Unannotated")

    for i, (pct, cnt) in enumerate(zip(pcts, counts)):
        if pct >= 8:
            ax.text(x[i], pct/2, f"{pct}%",
                    ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color="white", zorder=4)
        else:
            ax.text(x[i], pct + 1.5, f"{pct}%",
                    ha="center", va="bottom",
                    fontsize=9, fontweight="bold",
                    color=COL["purple_b"], zorder=4)
        ax.text(x[i], 102, f"n={cnt:,}",
                ha="center", va="bottom",
                fontsize=8, color=COL["muted"], zorder=4)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, color=COL["text"],
                       multialignment="center", linespacing=1.4)
    ax.set_ylim(0, 113)
    ax.set_ylabel("% of all diseases in RDKG", fontsize=9,
                  color=COL["muted"], labelpad=8)
    ax.yaxis.set_tick_params(labelsize=8.5, labelcolor=COL["muted"])
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    style_ax(ax)
    ax.spines["bottom"].set_color(COL["grid"])
    ax.tick_params(axis="x", length=0, pad=8)

    pa = mpatches.Patch(facecolor=COL["purple"], edgecolor=COL["purple_b"],
                        linewidth=0.5, label="Annotated")
    pu = mpatches.Patch(facecolor=COL["gray"], edgecolor=COL["gray_b"],
                        linewidth=0.5, label="Unannotated")
    ax.legend(handles=[pa, pu], loc="upper right", fontsize=9,
              frameon=True, framealpha=0.95,
              edgecolor=COL["grid"], fancybox=False)

    ax.text(0.5, 1.03,
            f"Total: {TOTAL:,} diseases  ·  72,368 nodes  ·  "
            f"834,260 edges  ·  15 relationship types",
            transform=ax.transAxes, ha="center", va="bottom",
            fontsize=8, color=COL["muted"], style="italic")

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(out("fig4_coverage.png"), dpi=300,
                bbox_inches="tight", facecolor=COL["white"], edgecolor="none")
    plt.close(fig)
    print("✓ fig4_coverage.png")


# ════════════════════════════════════════════════════════════════════════════
# Figure 5 — Inheritance distribution + Phenotypic similarity
# ════════════════════════════════════════════════════════════════════════════
def fig5_inheritance_similarity():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.8))
    fig.patch.set_facecolor(COL["white"])

    # Panel A: Inheritance patterns
    inheritance = [
        ("Mitochondrial",     39,  COL["amber_l"]),
        ("X-linked\ndominant",103, COL["amber"]),
        ("Multifactorial",   200,  COL["teal_l"]),
        ("X-linked",         388,  COL["teal"]),
        ("Autosomal\ndominant", 1923, COL["purple_l"]),
        ("Autosomal\nrecessive", 2560, COL["purple"]),
    ]
    labels_i = [x[0] for x in inheritance]
    counts_i = [x[1] for x in inheritance]
    colors_i = [x[2] for x in inheritance]

    bars = ax1.barh(range(len(labels_i)), counts_i,
                    color=colors_i, edgecolor=COL["white"],
                    linewidth=0.5, zorder=3, height=0.6)
    for bar, cnt in zip(bars, counts_i):
        ax1.text(bar.get_width() + 30,
                 bar.get_y() + bar.get_height()/2,
                 f"{cnt:,}", va="center", ha="left",
                 fontsize=8.5, color=COL["muted"])

    ax1.set_yticks(range(len(labels_i)))
    ax1.set_yticklabels(labels_i, fontsize=9, color=COL["text"])
    ax1.set_xlabel("Number of diseases", fontsize=9, color=COL["muted"])
    ax1.set_xlim(0, 3300)
    ax1.set_facecolor(COL["white"])
    ax1.spines[["top","right","left"]].set_visible(False)
    ax1.spines["bottom"].set_color(COL["grid"])
    ax1.xaxis.grid(True, color=COL["grid"], linewidth=0.6, zorder=0)
    ax1.set_axisbelow(True)
    ax1.tick_params(axis="both", length=0)
    ax1.set_title(
        "A  Inheritance pattern distribution\n"
        "(5,216 diseases with HAS_MODE_OF_INHERITANCE)",
        fontsize=9, loc="left", color=COL["text"], pad=10)

    # Panel B: Phenotypic similarity to Marfan syndrome
    sim_data = [
        ("Rubinstein-Taybi\nsyndrome",           37),
        ("Ehlers-Danlos\nmusculocontractural",    38),
        ("Loeys-Dietz\nsyndrome 1",               51),
        ("Aneurysm-osteoarthritis\nsyndrome",     55),
        ("Loeys-Dietz\nsyndrome 2",               67),
        ("Familial thoracic\naortic aneurysm",    92),
    ]
    labels_s = [x[0] for x in sim_data]
    counts_s = [x[1] for x in sim_data]

    bars2 = ax2.barh(range(len(labels_s)), counts_s,
                     color=COL["teal"], edgecolor=COL["teal_b"],
                     linewidth=0.5, zorder=3, height=0.6)
    for bar, n in zip(bars2, counts_s):
        ax2.text(bar.get_width() + 0.8,
                 bar.get_y() + bar.get_height()/2,
                 str(n), va="center", ha="left",
                 fontsize=8.5, color=COL["muted"])

    ax2.set_yticks(range(len(labels_s)))
    ax2.set_yticklabels(labels_s, fontsize=8.5, color=COL["text"])
    ax2.set_xlabel("Shared HPO phenotypes", fontsize=9, color=COL["muted"])
    ax2.set_xlim(0, 115)
    ax2.set_facecolor(COL["white"])
    ax2.spines[["top","right","left"]].set_visible(False)
    ax2.spines["bottom"].set_color(COL["grid"])
    ax2.xaxis.grid(True, color=COL["grid"], linewidth=0.6, zorder=0)
    ax2.set_axisbelow(True)
    ax2.tick_params(axis="both", length=0)
    ax2.set_title(
        "B  Phenotypic similarity to Marfan syndrome\n"
        "(MONDO:0007947, via shared HAS_PHENOTYPE edges)",
        fontsize=9, loc="left", color=COL["text"], pad=10)

    plt.tight_layout(pad=2.5)
    fig.savefig(out("fig5_inheritance_similarity.png"), dpi=300,
                bbox_inches="tight", facecolor=COL["white"], edgecolor="none")
    plt.close(fig)
    print("✓ fig5_inheritance_similarity.png")


# ════════════════════════════════════════════════════════════════════════════
# Figure 6 — Drug repurposing candidates for Marfan syndrome
# ════════════════════════════════════════════════════════════════════════════
def fig6_drug_repurposing():
    drugs = [
        ("Triamcinolone",       59),
        ("Prednisolone",        60),
        ("Testosterone",        61),
        ("Methylprednisolone",  62),
        ("Dexamethasone",       63),
        ("Prednisone",          65),
        ("Aliskiren",           71),
        ("Atenolol",            76),
        ("Losartan",            82),
    ]
    labels_d = [x[0] for x in drugs]
    scores   = [x[1] for x in drugs]

    # Color known treatments differently
    known = {"Losartan", "Atenolol"}
    colors_d = [COL["purple"] if l in known else COL["purple_l"]
                for l in labels_d]
    edges_d  = [COL["purple_b"] if l in known else COL["purple"]
                for l in labels_d]

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    fig.patch.set_facecolor(COL["white"])

    bars = ax.barh(range(len(labels_d)), scores,
                   color=colors_d, edgecolor=edges_d,
                   linewidth=0.5, zorder=3, height=0.6)
    for bar, s, lbl in zip(bars, scores, labels_d):
        ax.text(bar.get_width() + 0.5,
                bar.get_y() + bar.get_height()/2,
                str(s), va="center", ha="left",
                fontsize=9, color=COL["muted"])

    ax.set_yticks(range(len(labels_d)))
    ax.set_yticklabels(labels_d, fontsize=9.5, color=COL["text"])
    ax.set_xlabel("Phenotypic similarity score\n(shared HPO phenotypes with treated diseases)",
                  fontsize=9, color=COL["muted"])
    ax.set_xlim(0, 105)
    ax.set_facecolor(COL["white"])
    ax.spines[["top","right","left"]].set_visible(False)
    ax.spines["bottom"].set_color(COL["grid"])
    ax.xaxis.grid(True, color=COL["grid"], linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", length=0)

    # Validation annotation
    ax.annotate("Clinically validated\nfirst-line treatments",
                xy=(82, 8), xytext=(60, 6.5),
                fontsize=8, color=COL["purple_b"],
                arrowprops=dict(arrowstyle="-", color=COL["purple_b"],
                                lw=0.8))

    p_known = mpatches.Patch(facecolor=COL["purple"],
                              edgecolor=COL["purple_b"], linewidth=0.5,
                              label="Known Marfan treatment (validated)")
    p_cand  = mpatches.Patch(facecolor=COL["purple_l"],
                              edgecolor=COL["purple"], linewidth=0.5,
                              label="Candidate drug")
    ax.legend(handles=[p_known, p_cand], loc="lower right",
              fontsize=8.5, frameon=True, framealpha=0.95,
              edgecolor=COL["grid"], fancybox=False)

    ax.set_title(
        "Drug repurposing candidates for Marfan syndrome (MONDO:0007947)\n"
        "via phenotype-matched disease traversal in RDKG",
        fontsize=9, loc="left", color=COL["text"], pad=10)

    plt.tight_layout()
    fig.savefig(out("fig6_drug_repurposing.png"), dpi=300,
                bbox_inches="tight", facecolor=COL["white"], edgecolor="none")
    plt.close(fig)
    print("✓ fig6_drug_repurposing.png")


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Saving figures to: {OUT_DIR}\n")
    fig4_coverage()
    fig5_inheritance_similarity()
    fig6_drug_repurposing()
    print(f"\nAll figures saved to {OUT_DIR}")
