"""
测试 McKinsey 风格 - 分组垂直柱状图
虚构数据：AI领先企业 vs 其他企业在不同AI应用场景的采纳率
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

# ── McKinsey 配色 ─────────────────────────────────────
MCK_CYAN = '#2CBDEF'
MCK_GRAY = '#D4D4D4'
MCK_DARK = '#051C2C'
MCK_META = '#8C8C8C'
MCK_LINE = '#D4D4D4'

# ── 布局常量 ──────────────────────────────────────────
LEFT_X       = 0.08
EXHIBIT_Y    = 0.96
SEP_LINE_Y   = 0.935
TITLE_Y      = 0.90
SUBTITLE_Y   = 0.78
LEGEND_RIGHT = 0.82
SOURCE_Y     = 0.04

def apply_mckinsey_frame(fig, ax, exhibit_label, title, subtitle,
                         legend_items, source):
    fig.text(LEFT_X, EXHIBIT_Y, exhibit_label,
             fontproperties=fp, fontsize=10, color=MCK_META, va='top', ha='left')
    ax.plot([LEFT_X, 0.96], [SEP_LINE_Y, SEP_LINE_Y],
            transform=fig.transFigure, clip_on=False,
            color=MCK_LINE, linewidth=0.8, zorder=20)
    fig.text(LEFT_X, TITLE_Y, title,
             fontproperties=fp_bold, fontsize=16, color=MCK_DARK, va='top', ha='left')
    fig.text(LEFT_X, SUBTITLE_Y, subtitle,
             fontproperties=fp_bold, fontsize=11.5, color=MCK_DARK, va='top', ha='left')
    legend_y = SUBTITLE_Y + 0.02
    for name, color in legend_items:
        ax.add_patch(mpatches.Rectangle(
            xy=(LEGEND_RIGHT, legend_y - 0.018), width=0.02, height=0.016,
            facecolor=color, edgecolor='none',
            transform=fig.transFigure, clip_on=False, zorder=20))
        fig.text(LEGEND_RIGHT + 0.026, legend_y - 0.010, name,
                 fontproperties=fp, fontsize=10, color=MCK_DARK, va='center', ha='left')
        legend_y -= 0.028
    fig.text(LEFT_X, SOURCE_Y, f'Source: {source}',
             fontproperties=fp, fontsize=9, color=MCK_DARK, va='bottom', ha='left')

def style_mckinsey_axes(ax, show_bottom=True):
    for spine in ax.spines.values():
        spine.set_visible(False)
    if show_bottom:
        ax.spines['bottom'].set_visible(True)
        ax.spines['bottom'].set_color(MCK_LINE)
        ax.spines['bottom'].set_linewidth(0.8)
    ax.grid(False)
    ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=MCK_DARK)
    ax.set_yticks([])

# ── 虚构数据 ──────────────────────────────────────────
categories = ['代码生成', '客服机器人', '内容营销', '数据分析', '产品设计', '供应链优化']
ai_leaders = [78, 72, 65, 61, 48, 42]    # AI领先企业采纳率%
others     = [31, 45, 38, 29, 18, 12]    # 其他企业

fig, ax = plt.subplots(figsize=(11, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X, right=0.96, top=0.70, bottom=0.18)

x = list(range(len(categories)))
width = 0.35
ax.bar([i - width/2 for i in x], ai_leaders, width=width, color=MCK_CYAN, zorder=3)
ax.bar([i + width/2 for i in x], others,     width=width, color=MCK_GRAY, zorder=3)

# 柱顶数字
for i, (t, o) in enumerate(zip(ai_leaders, others)):
    ax.text(i - width/2, t + 1.5, f'{t}', ha='center', va='bottom',
            fontproperties=fp_bold, fontsize=11, color=MCK_DARK)
    ax.text(i + width/2, o + 1.5, f'{o}', ha='center', va='bottom',
            fontproperties=fp_bold, fontsize=11, color=MCK_DARK)

ax.set_xticks(x)
ax.set_xticklabels(categories, fontproperties=fp, fontsize=11, color=MCK_DARK)
ax.set_ylim(0, max(max(ai_leaders), max(others)) * 1.3)

style_mckinsey_axes(ax)
apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 3',
    title='AI领先企业在各场景的采纳率远超同行，\n代码生成和客服是最大差距领域',
    subtitle='各AI应用场景的企业采纳率，% of respondents',
    legend_items=[('AI领先企业', MCK_CYAN), ('其他企业', MCK_GRAY)],
    source='虚构数据，仅用于风格测试')

plt.savefig('/home/ubuntu/.openclaw/workspace/output_mckinsey.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("McKinsey done!")
