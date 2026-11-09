"""Render the headline benchmark chart (benchmarks/fewshot-7b.png / .svg).

On qwen2.5:7b (40-email corpus, see RESULTS.md), `--prompt few-shot` lifts
grounding but leaves faithfulness — and so trustworthiness — flat. The chart shows
that at a glance. Numbers come straight from RESULTS.md.

    pip install matplotlib
    python benchmarks/make_chart.py

Light surface, categorical blue/aqua from the project's data-viz palette
(validated for CVD); direct value labels satisfy the relief rule for the
sub-3:1 aqua.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, AQUA = "#2a78d6", "#1baf7a"  # categorical slots 1 & 2 -> plain / few-shot
INK, SECONDARY, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"

metrics = ["Grounded", "Faithful", "Trustworthy"]
plain = [48, 18, 18]  # qwen2.5:7b, --prompt plain
fewshot = [80, 20, 18]  # qwen2.5:7b, --prompt few-shot

plt.rcParams["font.family"] = "DejaVu Sans"
fig, ax = plt.subplots(figsize=(7.4, 4.5), dpi=160)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
fig.subplots_adjust(top=0.80, bottom=0.11, left=0.09, right=0.97)

x = list(range(len(metrics)))
w, gap = 0.36, 0.03
left = [xi - (w / 2 + gap / 2) for xi in x]
right = [xi + (w / 2 + gap / 2) for xi in x]

ax.bar(left, plain, width=w, color=BLUE, label="plain prompt", zorder=3)
ax.bar(right, fewshot, width=w, color=AQUA, label="few-shot prompt", zorder=3)
for px, v in [*zip(left, plain, strict=True), *zip(right, fewshot, strict=True)]:
    ax.text(
        px, v + 1.8, f"{v}%", ha="center", va="bottom", fontsize=10.5, color=INK, fontweight="bold"
    )

ax.set_ylim(0, 100)
ax.set_xlim(-0.6, len(metrics) - 0.4)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=11.5, color=INK)
ax.set_yticks(range(0, 101, 20))
ax.set_yticklabels([f"{t}%" for t in range(0, 101, 20)], fontsize=9, color=MUTED)
ax.yaxis.grid(True, color=GRID, linewidth=1, zorder=0)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(length=0)

fig.text(
    0.02,
    0.93,
    "Few-shot recovers the 7B's grounding — not its faithfulness",
    fontsize=13.5,
    color=INK,
    fontweight="bold",
)
fig.text(
    0.02,
    0.865,
    "qwen2.5:7b on 40 labelled emails  ·  higher is better",
    fontsize=9.5,
    color=SECONDARY,
)
leg = ax.legend(
    loc="upper center",
    frameon=False,
    fontsize=10,
    ncol=2,
    handlelength=1.0,
    handleheight=1.0,
    columnspacing=1.4,
    bbox_to_anchor=(0.5, 1.02),
)
for t in leg.get_texts():
    t.set_color(SECONDARY)

out = Path(__file__).with_name("fewshot-7b")
fig.savefig(out.with_suffix(".svg"), facecolor=SURFACE, bbox_inches="tight")
fig.savefig(out.with_suffix(".png"), facecolor=SURFACE, bbox_inches="tight", dpi=160)
print("wrote", out.with_suffix(".svg").name, "and", out.with_suffix(".png").name)
