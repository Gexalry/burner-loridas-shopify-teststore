"""Coded chart images for the GLP-1 sections of product.default-copy.
Run: python3 chart-images/make_charts.py chart-images
Theme colors: orange accent #ff5801, ink #444444, muted #666666."""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

OUT = sys.argv[1]
ACCENT, INK, MUTED, CONTEXT, LIGHT, DARK = '#ff5801', '#444444', '#666666', '#8c8c8c', '#e6e6e6', '#2b2b2b'
for f in font_manager.findSystemFonts():
    if 'Inter' in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({'font.family': 'Inter', 'font.size': 13, 'text.color': INK,
                     'axes.edgecolor': LIGHT, 'xtick.color': MUTED, 'ytick.color': MUTED})


def rbar(ax, x, y, w, h, color, horizontal=False):
    """Bar with 4px-ish rounded data end, square at the baseline."""
    r = 0.06 if not horizontal else 0.08
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                fc=color, ec='none', mutation_aspect=1))


def clean(ax):
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])


def save(fig, name):
    fig.savefig(f'{OUT}/{name}.png', dpi=200, transparent=True, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)


# 1. Zepbound label: reported hair loss
fig, ax = plt.subplots(figsize=(6, 4.4))
vals = [(7.1, 'Women,\nZepbound', ACCENT), (0.5, 'Men,\nZepbound', CONTEXT), (1.3, 'Women,\nplacebo', CONTEXT)]
for i, (v, lab, c) in enumerate(vals):
    ax.bar(i, v, width=0.56, color=c)
    ax.text(i, v + 0.18, f'{v}%', ha='center', va='bottom', fontsize=22, fontweight='bold', color=INK)
    ax.text(i, -0.35, lab, ha='center', va='top', fontsize=13, color=MUTED)
ax.axhline(0, color='#cfcfcf', lw=1)
ax.set_xlim(-0.6, 2.6); ax.set_ylim(-1.6, 8.6)
clean(ax)
save(fig, 'glp1-chart-zepbound')

# 2. Famine Shed timeline (months 0-18)
fig, ax = plt.subplots(figsize=(7, 3.6))
segs = [(0, 0.6, DARK, 'Month 0', 'The famine signal'), (0.6, 3, CONTEXT, 'Months 1–3', 'The silence: 2–3 months'),
        (3, 6, ACCENT, 'Months 3–6', 'The shed: peaks months 4–6'),
        (6, 18, LIGHT, 'Months 6–18', 'Regrowth to full thickness: 12–18 months')]
for a, b, c, _, _ in segs:
    ax.barh(2.2, b - a, left=a, height=0.8, color=c, edgecolor='white', linewidth=2)
for m in (0, 3, 6, 12, 18):
    ax.text(m, 1.62, str(m), ha='center', va='top', fontsize=11, color=MUTED)
ax.text(18, 1.2, 'months', ha='right', va='top', fontsize=10.5, color=MUTED)
for i, (_, _, c, when, lab) in enumerate(segs):
    y = 0.55 - i * 0.48
    ax.scatter(0.25, y, s=150, marker='s', color=c)
    ax.text(0.75, y, when, va='center', fontsize=12, fontweight='semibold', color=INK)
    ax.text(5.0, y, lab, va='center', fontsize=12, color=MUTED)
ax.set_xlim(-0.2, 18.2); ax.set_ylim(-1.1, 2.7)
clean(ax)
save(fig, 'glp1-chart-famine-shed-timeline')

# 3. BMJ: hair loss per 1,000 person-years
fig, axes = plt.subplots(2, 1, figsize=(6, 4.6), sharex=True)
groups = [('vs SGLT-2 drugs: +37%', [('GLP-1', 6.91, ACCENT), ('SGLT-2', 5.04, CONTEXT)]),
          ('vs DPP-4 drugs: +68%', [('GLP-1', 6.53, ACCENT), ('DPP-4', 3.89, CONTEXT)])]
for ax, (head, rows) in zip(axes, groups):
    for j, (lab, v, c) in enumerate(rows):
        y = 1 - j
        ax.barh(y, v, height=0.62, color=c)
        ax.text(-0.15, y, lab, ha='right', va='center', fontsize=13, color=MUTED)
        ax.text(v + 0.12, y, f'{v:.2f}', ha='left', va='center', fontsize=15, fontweight='bold', color=INK)
    ax.text(-1.6, 1.62, head, ha='left', va='center', fontsize=14, fontweight='semibold', color=INK)
    ax.plot([0, 0], [-0.4, 1.4], color='#cfcfcf', lw=1)
    ax.set_xlim(-1.6, 8.2); ax.set_ylim(-0.5, 1.9)
    clean(ax)
fig.text(0.5, 0.0, 'Hair loss cases per 1,000 person-years', ha='center', fontsize=11, color=MUTED)
fig.subplots_adjust(hspace=0.15)
save(fig, 'glp1-chart-bmj')

# 4. Trial: growth phase, pull test, root (stacked panels)
fig = plt.figure(figsize=(6, 10.2))
gs = fig.add_gridspec(3, 1, height_ratios=[1.25, 1.35, 0.7], hspace=0.45)

ax = fig.add_subplot(gs[0])
bars = [(0, 24.6, CONTEXT, 'Day 1'), (1, 37.4, ACCENT, 'Day 90'), (2.6, 25.5, CONTEXT, 'Day 1'), (3.6, 20.2, DARK, 'Day 90')]
for x, v, c, lab in bars:
    ax.bar(x, v, width=0.78, color=c)
    ax.text(x, v + 0.8, f'{v}', ha='center', va='bottom', fontsize=15, fontweight='bold', color=INK)
    ax.text(x, -1.2, lab, ha='center', va='top', fontsize=11, color=MUTED)
ax.text(1, 45.5, '+52%', ha='center', fontsize=13, fontweight='bold', color=ACCENT)
ax.text(3.6, 28.3, '−21%', ha='center', fontsize=13, fontweight='bold', color=INK)
ax.text(0.5, -6.5, 'Spermidine-based supplement', ha='center', va='top', fontsize=12, color=INK, fontweight='semibold')
ax.text(3.1, -6.5, 'Placebo', ha='center', va='top', fontsize=12, color=INK, fontweight='semibold')
ax.text(-0.55, 54, 'Growth-phase hairs per 100 plucked', ha='left', fontsize=12.5, fontweight='semibold', color=INK)
ax.axhline(0, color='#cfcfcf', lw=1)
ax.set_xlim(-0.6, 4.2); ax.set_ylim(-11, 57)
clean(ax)

ax = fig.add_subplot(gs[1])
ax.text(0, 8.9, 'Pull test at 6 months: hair came loose', ha='left', fontsize=12.5, fontweight='semibold', color=INK)
for gx, lost, title in [(0, 0, 'Spermidine: 0 of 50'), (5.6, 34, 'Placebo: 34 of 50')]:
    ax.text(gx, 7.7, title, ha='left', fontsize=13, fontweight='bold', color=ACCENT if lost == 0 else INK)
    for i in range(50):
        r, c = divmod(i, 10)
        ax.scatter(gx + c * 0.48 + 0.2, 6.7 - r * 0.55 - 0.3, s=110,
                   color=DARK if i < lost else LIGHT, edgecolors='white', linewidths=1.2)
ax.scatter(0.2, 3.3, s=90, color=DARK); ax.text(0.45, 3.3, 'Came loose on a firm tug', va='center', fontsize=11, color=MUTED)
ax.scatter(5.8, 3.3, s=90, color=LIGHT); ax.text(6.05, 3.3, 'Held', va='center', fontsize=11, color=MUTED)
ax.set_xlim(-0.1, 11); ax.set_ylim(2.8, 9.3)
clean(ax)

ax = fig.add_subplot(gs[2])
ax.text(-16, 1.15, 'Cell division at the root after 90 days', ha='left', fontsize=12.5, fontweight='semibold', color=INK)
ax.barh(0.3, -5, height=0.55, color=CONTEXT)
ax.barh(0.3, 14, height=0.55, color=ACCENT)
ax.plot([0, 0], [-0.05, 0.65], color=INK, lw=1.2)
ax.text(-5.3, 0.3, 'Placebo −5%', ha='right', va='center', fontsize=12, color=INK, fontweight='semibold')
ax.text(14.3, 0.3, 'Spermidine +14%', ha='left', va='center', fontsize=12, color=INK, fontweight='semibold')
ax.set_xlim(-16, 26); ax.set_ylim(-0.3, 1.4)
clean(ax)
save(fig, 'glp1-chart-trial')
