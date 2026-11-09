"""Render the benchmark charts (benchmarks/*.png / *.svg).

Two grouped bar charts from RESULTS.md (40-email corpus, local Qwen 2.5):

- ``auditability-3b-7b`` — plain prompt, 3B vs 7B: similar accuracy, very
  different grounding / faithfulness / trustworthiness.
- ``fewshot-7b`` — qwen2.5:7b, plain vs few-shot: few-shot lifts grounding but
  leaves faithfulness (and so trustworthiness) flat.

    pip install matplotlib
    python benchmarks/make_chart.py

Light surface, categorical blue/aqua from the project's data-viz palette
(validated for CVD, worst-adjacent ΔE 73.6); direct value labels satisfy the
relief rule for the sub-3:1 aqua.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, AQUA = "#2a78d6", "#1baf7a"  # categorical slots 1 & 2
INK, SECONDARY, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"

plt.rcParams["font.family"] = "DejaVu Sans"


def grouped_chart(name, title, subtitle, groups, series):
    """series: list of (label, color, values) — one bar per series within each group."""
    n_groups, n_series = len(groups), len(series)
    fig, ax = plt.subplots(figsize=(1.15 * n_groups + 3.2, 4.5), dpi=160)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    fig.subplots_adjust(top=0.80, bottom=0.11, left=0.08, right=0.97)

    x = list(range(n_groups))
    total = 0.74  # width of a group's bars together
    w = total / n_series
    for si, (label, color, values) in enumerate(series):
        offs = [xi - total / 2 + w / 2 + si * w for xi in x]
        ax.bar(offs, values, width=w * 0.92, color=color, label=label, zorder=3)
        for px, v in zip(offs, values, strict=True):
            ax.text(
                px,
                v + 1.8,
                f"{v}%",
                ha="center",
                va="bottom",
                fontsize=10,
                color=INK,
                fontweight="bold",
            )

    ax.set_ylim(0, 100)
    ax.set_xlim(-0.6, n_groups - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(groups, fontsize=11.5, color=INK)
    ax.set_yticks(range(0, 101, 20))
    ax.set_yticklabels([f"{t}%" for t in range(0, 101, 20)], fontsize=9, color=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)

    fig.text(0.02, 0.93, title, fontsize=13.5, color=INK, fontweight="bold")
    fig.text(0.02, 0.865, subtitle, fontsize=9.5, color=SECONDARY)
    leg = ax.legend(
        loc="upper right",
        frameon=False,
        fontsize=10,
        ncol=n_series,
        handlelength=1.0,
        handleheight=1.0,
        columnspacing=1.4,
        bbox_to_anchor=(1.0, 1.03),
    )
    for t in leg.get_texts():
        t.set_color(SECONDARY)

    out = Path(__file__).with_name(name)
    fig.savefig(out.with_suffix(".svg"), facecolor=SURFACE, bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), facecolor=SURFACE, bbox_inches="tight", dpi=160)
    plt.close(fig)
    print("wrote", out.with_suffix(".svg").name, "and", out.with_suffix(".png").name)


# Plain prompt, 3B vs 7B — same ballpark accuracy, very different auditability.
grouped_chart(
    "auditability-3b-7b",
    "Same accuracy, very different auditability",
    "plain prompt, 40 labelled emails  ·  higher is better",
    ["Accuracy", "Grounded", "Faithful", "Trustworthy"],
    [("qwen2.5:3b", BLUE, [82, 98, 45, 45]), ("qwen2.5:7b", AQUA, [78, 48, 18, 18])],
)

# qwen2.5:7b, plain vs few-shot — grounding recovers, faithfulness doesn't.
grouped_chart(
    "fewshot-7b",
    "Few-shot recovers the 7B's grounding — not its faithfulness",
    "qwen2.5:7b on 40 labelled emails  ·  higher is better",
    ["Grounded", "Faithful", "Trustworthy"],
    [("plain prompt", BLUE, [48, 18, 18]), ("few-shot prompt", AQUA, [80, 20, 18])],
)
