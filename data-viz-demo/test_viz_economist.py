"""
测试 The Economist 风格 - 折线图
虚构数据：2020-2024 全球AI投资趋势（中美对比）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

# ── 字体 ──────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fp      = FontProperties(fname=font_path)
fp_bold = FontProperties(fname=font_path, weight='bold')

# ── Economist 配色 ───────────────────────────────────
ECON_RED   = '#E3120B'
ECON_BLUE  = '#006BA2'
ECON_GREY  = '#758D99'
ECON_GRID  = '#A8BAC4'
TEXT_DARK  = '#121212'
TEXT_SUB   = '#555555'

# ── 布局常量 ──────────────────────────────────────────
LEFT_X     = 0.14
RED_LINE_Y = 0.970
TAG_W, TAG_H = 0.055, 0.030
TITLE_Y    = 0.920
SUBTITLE_Y = 0.860
SOURCE_Y   = 0.025

# ── 虚构数据 ──────────────────────────────────────────
years = [2020, 2021, 2022, 2023, 2024]
us    = [480, 620, 580, 850, 1200]   # 亿美元
china = [180, 260, 310, 420, 680]
world = [820, 1050, 1080, 1560, 2300]
series = [
    ('美国',   us,    ECON_RED),     # 重点
    ('中国',   china, ECON_BLUE),    # 重点
    ('全球',   world, ECON_GREY),    # 灰化对照
]

# ── 画布 ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X, right=0.86, top=0.76, bottom=0.12)

for name, vals, color in series:
    ax.plot(years, vals, color=color, linewidth=2.5,
            marker='o', markersize=6, markerfacecolor=color,
            markeredgecolor='white', markeredgewidth=1.5, zorder=3)
    # 末端系列名（替代图例）
    ax.text(years[-1] + 0.15, vals[-1], name,
            fontproperties=fp_bold, fontsize=11, color=color,
            va='center', ha='left')

ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], fontsize=11, color=TEXT_DARK)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}'))
ax.set_xlim(years[0] - 0.3, years[-1] + 1.2)
ax.set_ylim(0, 2800)

# 边框 + 网格
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color('#444444')
ax.spines['bottom'].set_linewidth(1.2)
ax.yaxis.grid(True, color=ECON_GRID, linewidth=1.0, zorder=0)
ax.xaxis.grid(False)
ax.set_axisbelow(True)
ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=ECON_GREY)
ax.tick_params(axis='x', labelsize=11, labelcolor=TEXT_DARK)

# ── 红线 + 红色方块 tag ──────────────────────────────
ax.plot([LEFT_X, 1.0], [RED_LINE_Y, RED_LINE_Y],
        transform=fig.transFigure, clip_on=False,
        color=ECON_RED, linewidth=2.5, solid_capstyle='butt', zorder=20)
ax.add_patch(mpatches.Rectangle(
    xy=(LEFT_X, RED_LINE_Y - TAG_H), width=TAG_W, height=TAG_H,
    facecolor=ECON_RED, edgecolor='none',
    transform=fig.transFigure, clip_on=False, zorder=20))

# ── 标题 / 副标题 / 来源 ─────────────────────────────
fig.text(LEFT_X, TITLE_Y, '美国AI投资遥遥领先，中国加速追赶',
         fontproperties=fp_bold, fontsize=13, color=TEXT_DARK, va='top', ha='left')
fig.text(LEFT_X, SUBTITLE_Y, '全球AI领域风险投资额，2020–2024，亿美元',
         fontproperties=fp, fontsize=10.5, color=TEXT_SUB, va='top', ha='left')
fig.text(LEFT_X, SOURCE_Y, '来源：虚构数据，仅用于风格测试',
         fontproperties=fp, fontsize=9, color=ECON_GREY, va='bottom', ha='left')

plt.savefig('/home/ubuntu/.openclaw/workspace/output_economist.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("Economist done!")
