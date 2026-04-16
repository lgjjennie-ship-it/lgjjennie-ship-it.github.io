"""
测试 BCG 风格 - 水平柱状图
虚构数据：2024全球AI大模型公司融资额Top 6
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# ── 字体（Linux Noto Sans CJK）──────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fp = FontProperties(fname=font_path)

# ── BCG 配色 ──────────────────────────────────────────
COLOR_MAIN = '#2ca02c'

# ── 虚构数据 ──────────────────────────────────────────
companies = ['Anthropic', 'OpenAI', 'xAI', 'Mistral', '智谱AI', 'MiniMax']
funding = [300, 256, 120, 65, 42, 28]  # 亿美元
N = 6

# ── 画布 ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('white')
fig.subplots_adjust(left=0.12, right=0.92, top=0.88, bottom=0.12)

# ── 绘图 ──────────────────────────────────────────────
bars = ax.barh(range(len(companies)), funding, color=COLOR_MAIN, height=0.58)
ax.set_yticks(range(len(companies)))
ax.set_yticklabels(companies, fontproperties=fp, fontsize=14)
ax.set_xlabel('融资额（亿美元）', fontproperties=fp, fontsize=12)
ax.set_xlim(0, max(funding) * 1.25)
ax.tick_params(axis='x', labelsize=11)
ax.set_title(f'2024年全球AI大模型公司融资额Top 6 (N={N})',
             fontproperties=fp, fontsize=17, fontweight='bold', pad=14)

# ── 边框处理 ──────────────────────────────────────────
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['left'].set_linewidth(1)
ax.grid(False)

# ── 数据标签 ──────────────────────────────────────────
for bar, val in zip(bars, funding):
    ax.text(val + max(funding) * 0.015, bar.get_y() + bar.get_height() / 2,
            f'${val}亿', va='center', fontproperties=fp, fontsize=12)

# ── 来源注脚 ──────────────────────────────────────────
fig.text(0.12, 0.02, '来源：虚构数据，仅用于风格测试',
         fontproperties=fp, fontsize=9, color='#888888', va='bottom')

plt.savefig('/home/ubuntu/.openclaw/workspace/output_bcg.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("BCG done!")
