"""
128渠道存量用户数据分析 - McKinsey风格可视化
=============================================
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ── 字体设置 ──────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_path_bold = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
fp = FontProperties(fname=font_path)
fp_bold = FontProperties(fname=font_path_bold)

# ── McKinsey 配色 ─────────────────────────────────
MCK_CYAN = '#2CBDEF'
MCK_GRAY = '#D4D4D4'
MCK_DARK = '#051C2C'
MCK_META = '#8C8C8C'
MCK_LINE = '#D4D4D4'
MCK_COLORS = ['#2CBDEF', '#1A8BB5', '#0E6E8F', '#D4D4D4', '#B0B0B0', '#8C8C8C']

LEFT_X = 0.08
EXHIBIT_Y = 0.96
SEP_LINE_Y = 0.935
TITLE_Y = 0.90
SUBTITLE_Y = 0.78
LEGEND_RIGHT = 0.78
SOURCE_Y = 0.04

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 通用函数 ──────────────────────────────────────
def apply_mckinsey_frame(fig, ax, exhibit_label, title, subtitle,
                         legend_items, source, subtitle_y=SUBTITLE_Y):
    fig.text(LEFT_X, EXHIBIT_Y, exhibit_label,
             fontproperties=fp, fontsize=10, color=MCK_META, va='top', ha='left')
    ax.plot([LEFT_X, 0.96], [SEP_LINE_Y, SEP_LINE_Y],
            transform=fig.transFigure, clip_on=False,
            color=MCK_LINE, linewidth=0.8, zorder=20)
    fig.text(LEFT_X, TITLE_Y, title,
             fontproperties=fp_bold, fontsize=15, color=MCK_DARK, va='top', ha='left')
    fig.text(LEFT_X, subtitle_y, subtitle,
             fontproperties=fp_bold, fontsize=11, color=MCK_DARK, va='top', ha='left')
    legend_y = subtitle_y + 0.02
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


# ── 读取数据 ──────────────────────────────────────
df = pd.read_excel('/tmp/128.xlsx', sheet_name='Sheet2')
total_users = len(df)

# ============================================================
# CHART 1: ytag来源占比 (环形图)
# ============================================================
print("=== Chart 1: ytag来源占比 ===")

ggsem_mask = df['综合ytag'].astype(str).str.contains('ggsem', case=False, na=False)
non_zero_mask = df['综合ytag'].astype(str) != '0'

ggsem_count = ggsem_mask.sum()
other_ytag_count = (~ggsem_mask & non_zero_mask).sum()
no_ytag_count = (~non_zero_mask).sum()

print(f"ggsem用户: {ggsem_count} ({ggsem_count/total_users*100:.1f}%)")
print(f"其他ytag: {other_ytag_count} ({other_ytag_count/total_users*100:.1f}%)")
print(f"无ytag(0): {no_ytag_count} ({no_ytag_count/total_users*100:.1f}%)")

fig, ax = plt.subplots(figsize=(10, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X, right=0.96, top=0.70, bottom=0.15)

sizes = [ggsem_count, other_ytag_count, no_ytag_count]
labels_data = [f'ggsem\n{ggsem_count:,} ({ggsem_count/total_users*100:.1f}%)',
          f'Other ytag\n{other_ytag_count:,} ({other_ytag_count/total_users*100:.1f}%)',
          f'No ytag\n{no_ytag_count:,} ({no_ytag_count/total_users*100:.1f}%)']
colors = [MCK_CYAN, '#1A8BB5', MCK_GRAY]

wedges, texts, autotexts = ax.pie(sizes, labels=labels_data, colors=colors,
    autopct='', startangle=90, pctdistance=0.85,
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
for t in texts:
    t.set_fontproperties(fp_bold)
    t.set_fontsize(11)
    t.set_color(MCK_DARK)

ax.text(0, 0, f'Total\n{total_users:,}', ha='center', va='center',
        fontproperties=fp_bold, fontsize=16, color=MCK_DARK)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 1',
    title='ggsem(Google Ads)is the largest identified acquisition channel,\naccounting for 42.6% of all registered users',
    subtitle=f'User distribution by ytag source, N={total_users:,}',
    legend_items=[('ggsem (Google Ads)', MCK_CYAN), ('Other ytag', '#1A8BB5'), ('No ytag', MCK_GRAY)],
    source='128 Channel User Data')

plt.savefig(f'{OUTPUT_DIR}/01_ytag_source_distribution.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Chart 1 saved.")

# ============================================================
# CHART 2: ggsem用户中 search vs pmax 占比
# ============================================================
print("\n=== Chart 2: ggsem中search vs pmax ===")

ggsem_df = df[ggsem_mask].copy()
ggsem_total = len(ggsem_df)

# Classify by ytag suffix
def classify_campaign_type(ytag):
    ytag_str = str(ytag).lower()
    if '_pmax' in ytag_str:
        return 'PMax'
    elif '_search' in ytag_str:
        return 'Search'
    elif '_display' in ytag_str:
        return 'Display'
    else:
        return 'Other'

ggsem_df['campaign_type'] = ggsem_df['综合ytag'].apply(classify_campaign_type)
type_counts = ggsem_df['campaign_type'].value_counts()

print(f"ggsem total: {ggsem_total}")
for ct, cnt in type_counts.items():
    print(f"  {ct}: {cnt} ({cnt/ggsem_total*100:.1f}%)")

fig, ax = plt.subplots(figsize=(10, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X+0.05, right=0.96, top=0.70, bottom=0.15)

type_colors = {'Search': MCK_CYAN, 'PMax': '#1A8BB5', 'Display': '#0E6E8F', 'Other': MCK_GRAY}
bars_data = type_counts.sort_values(ascending=True)
bar_colors = [type_colors.get(k, MCK_GRAY) for k in bars_data.index]

y_pos = range(len(bars_data))
bars = ax.barh(y_pos, bars_data.values, height=0.55, color=bar_colors, zorder=3)

ax.set_yticks(list(y_pos))
ax.set_yticklabels(bars_data.index, fontproperties=fp_bold, fontsize=12, color=MCK_DARK)

for i, (val, idx) in enumerate(zip(bars_data.values, bars_data.index)):
    pct = val / ggsem_total * 100
    ax.text(val + ggsem_total*0.01, i, f'{val:,} ({pct:.1f}%)',
            ha='left', va='center', fontproperties=fp_bold, fontsize=11, color=MCK_DARK)

ax.set_xlim(0, max(bars_data.values) * 1.35)
style_mckinsey_axes(ax)
ax.spines['left'].set_visible(True)
ax.spines['left'].set_color(MCK_LINE)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 2',
    title='Among ggsem users, Search and PMax campaigns\ncontribute nearly equally as primary acquisition drivers',
    subtitle=f'ggsem user breakdown by campaign type, N={ggsem_total:,}',
    legend_items=[],
    source='128 Channel User Data')

plt.savefig(f'{OUTPUT_DIR}/02_ggsem_campaign_type.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Chart 2 saved.")

# ============================================================
# CHART 3: 月注册量趋势
# ============================================================
print("\n=== Chart 3: Monthly registration trend ===")

df['reg_month'] = pd.to_datetime(df['注册时间']).dt.to_period('M')
monthly_reg = df.groupby('reg_month').size().reset_index(name='count')
monthly_reg['month_str'] = monthly_reg['reg_month'].astype(str)

# Filter meaningful months (>= 2023-08)
monthly_reg = monthly_reg[monthly_reg['reg_month'] >= '2023-08']

print(f"Monthly data points: {len(monthly_reg)}")
print(monthly_reg.to_string())

fig, ax = plt.subplots(figsize=(14, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X+0.02, right=0.96, top=0.70, bottom=0.18)

x_vals = range(len(monthly_reg))
ax.plot(list(x_vals), monthly_reg['count'].values, color=MCK_CYAN, linewidth=2.5,
        marker='o', markersize=5, markerfacecolor=MCK_CYAN,
        markeredgecolor='white', markeredgewidth=1.5, zorder=3)

# Fill area
ax.fill_between(list(x_vals), monthly_reg['count'].values, alpha=0.15, color=MCK_CYAN, zorder=2)

# Annotate peaks
peak_idx = monthly_reg['count'].idxmax()
peak_month = monthly_reg.loc[peak_idx, 'month_str']
peak_val = monthly_reg.loc[peak_idx, 'count']
peak_x = list(x_vals)[monthly_reg.index.get_loc(peak_idx)]
ax.annotate(f'{peak_val:,}', xy=(peak_x, peak_val), xytext=(peak_x, peak_val + 400),
            fontproperties=fp_bold, fontsize=11, color=MCK_DARK,
            ha='center', va='bottom',
            arrowprops=dict(arrowstyle='->', color=MCK_META, lw=1))

# Show every 3rd month label to avoid crowding
tick_positions = list(x_vals)
tick_labels = monthly_reg['month_str'].values
show_every = max(1, len(tick_labels) // 12)
display_labels = [l if i % show_every == 0 else '' for i, l in enumerate(tick_labels)]
ax.set_xticks(tick_positions)
ax.set_xticklabels(display_labels, fontproperties=fp, fontsize=9, color=MCK_DARK, rotation=45, ha='right')

# Y grid
ax.yaxis.grid(True, color='#E8E8E8', linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color(MCK_LINE)
ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=MCK_DARK)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 3',
    title='128 Channel monthly registration trend shows\nsignificant growth acceleration since mid-2024',
    subtitle='Monthly new registrations, Aug 2023 - Apr 2026',
    legend_items=[],
    source='128 Channel User Data')

plt.savefig(f'{OUTPUT_DIR}/03_monthly_registration_trend.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Chart 3 saved.")

# ============================================================
# CHART 4: 注册客户 vs 充值客户 - 月度趋势
# ============================================================
print("\n=== Chart 4: Registration vs Recharge monthly ===")

has_recharge = df['累计充值金额$'].notna() & (df['累计充值金额$'] > 0)
df['has_recharge'] = has_recharge

monthly_total = df.groupby('reg_month').size().reset_index(name='registered')
monthly_recharge = df[df['has_recharge']].groupby('reg_month').size().reset_index(name='recharged')
monthly_combined = monthly_total.merge(monthly_recharge, on='reg_month', how='left').fillna(0)
monthly_combined['recharged'] = monthly_combined['recharged'].astype(int)
monthly_combined['conversion_rate'] = (monthly_combined['recharged'] / monthly_combined['registered'] * 100).round(1)
monthly_combined['month_str'] = monthly_combined['reg_month'].astype(str)
monthly_combined = monthly_combined[monthly_combined['reg_month'] >= '2023-08']

print(monthly_combined[['month_str','registered','recharged','conversion_rate']].to_string())

fig, ax = plt.subplots(figsize=(14, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X+0.02, right=0.88, top=0.70, bottom=0.18)

x_vals = range(len(monthly_combined))
ax.plot(list(x_vals), monthly_combined['registered'].values, color=MCK_CYAN, linewidth=2.5,
        marker='o', markersize=5, markerfacecolor=MCK_CYAN,
        markeredgecolor='white', markeredgewidth=1.5, zorder=3, label='Registered')
ax.plot(list(x_vals), monthly_combined['recharged'].values, color='#E8833A', linewidth=2.5,
        marker='s', markersize=5, markerfacecolor='#E8833A',
        markeredgecolor='white', markeredgewidth=1.5, zorder=3, label='Recharged')

# End labels
last_idx = len(monthly_combined) - 1
ax.text(last_idx + 0.3, monthly_combined['registered'].values[-1], 'Registered',
        fontproperties=fp_bold, fontsize=10, color=MCK_CYAN, va='center')
ax.text(last_idx + 0.3, monthly_combined['recharged'].values[-1], 'Recharged',
        fontproperties=fp_bold, fontsize=10, color='#E8833A', va='center')

tick_positions = list(x_vals)
tick_labels = monthly_combined['month_str'].values
show_every = max(1, len(tick_labels) // 12)
display_labels = [l if i % show_every == 0 else '' for i, l in enumerate(tick_labels)]
ax.set_xticks(tick_positions)
ax.set_xticklabels(display_labels, fontproperties=fp, fontsize=9, color=MCK_DARK, rotation=45, ha='right')

ax.yaxis.grid(True, color='#E8E8E8', linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color(MCK_LINE)
ax.tick_params(axis='both', length=0, labelsize=10, labelcolor=MCK_DARK)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 4',
    title='Registration-to-recharge conversion remains a key\noptimization opportunity across all cohorts',
    subtitle='Monthly registered vs recharged users, Aug 2023 - Apr 2026',
    legend_items=[('Registered', MCK_CYAN), ('Recharged', '#E8833A')],
    source='128 Channel User Data')

plt.savefig(f'{OUTPUT_DIR}/04_registration_vs_recharge_trend.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Chart 4 saved.")

# ============================================================
# CHART 5: 注册 vs 充值 - 总量对比柱状图
# ============================================================
print("\n=== Chart 5: Registration vs Recharge summary ===")

total_registered = len(df)
total_recharged = has_recharge.sum()
conversion_rate = total_recharged / total_registered * 100
avg_recharge = df.loc[has_recharge, '累计充值金额$'].mean()
total_revenue = df['累计充值金额$'].sum()

print(f"Total registered: {total_registered:,}")
print(f"Total recharged: {total_recharged:,}")
print(f"Conversion: {conversion_rate:.1f}%")
print(f"Avg recharge: ${avg_recharge:,.0f}")
print(f"Total revenue: ${total_revenue:,.0f}")

fig, ax = plt.subplots(figsize=(10, 7.5))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=LEFT_X+0.02, right=0.96, top=0.68, bottom=0.15)

bars = ax.bar([0, 1], [total_registered, total_recharged], width=0.38,
              color=[MCK_CYAN, '#E8833A'], zorder=3)
ax.text(0, total_registered + 1500, f'{total_registered:,}', ha='center', va='bottom',
        fontproperties=fp_bold, fontsize=14, color=MCK_DARK)
ax.text(1, total_recharged + 1500, f'{total_recharged:,}\n({conversion_rate:.1f}%)',
        ha='center', va='bottom', fontproperties=fp_bold, fontsize=14, color=MCK_DARK)

ax.set_xticks([0, 1])
ax.set_xticklabels(['Registered', 'Recharged'], fontproperties=fp_bold, fontsize=13, color=MCK_DARK)
ax.set_ylim(0, total_registered * 1.25)
style_mckinsey_axes(ax)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 5',
    title=f'Only {conversion_rate:.1f}% of registered users convert to paying,\nwith ${total_revenue:,.0f} total revenue from {total_recharged:,} users',
    subtitle=f'Total registered vs recharged users, avg recharge ${avg_recharge:,.0f}/user',
    legend_items=[('Registered', MCK_CYAN), ('Recharged', '#E8833A')],
    source='128 Channel User Data')

plt.savefig(f'{OUTPUT_DIR}/05_registration_vs_recharge_bar.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Chart 5 saved.")

# ============================================================
# CHART 6: 关键词分析 - Top 20
# ============================================================
print("\n=== Chart 6: Keyword analysis ===")

# Filter out '0' (no keyword)
kw_df = df[df['关键词'].astype(str) != '0'].copy()
kw_counts = kw_df['关键词'].value_counts().head(20)

# Also calculate recharge rate per keyword
kw_stats = kw_df.groupby('关键词').agg(
    reg_count=('company_id', 'count'),
    recharge_count=('has_recharge', 'sum'),
    total_revenue=('累计充值金额$', 'sum')
).sort_values('reg_count', ascending=False).head(20)
kw_stats['conversion_rate'] = (kw_stats['recharge_count'] / kw_stats['reg_count'] * 100).round(1)
kw_stats['avg_revenue'] = (kw_stats['total_revenue'] / kw_stats['recharge_count']).round(0)
kw_stats['avg_revenue'] = kw_stats['avg_revenue'].fillna(0)

print(kw_stats.to_string())

fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=0.22, right=0.96, top=0.72, bottom=0.10)

top_kw = kw_stats.sort_values('reg_count', ascending=True)
y_pos = range(len(top_kw))
bar_colors = [MCK_CYAN if r > 10 else MCK_GRAY for r in top_kw['conversion_rate'].values]
bars = ax.barh(list(y_pos), top_kw['reg_count'].values, height=0.6, color=bar_colors, zorder=3)

ax.set_yticks(list(y_pos))
ax.set_yticklabels(top_kw.index, fontproperties=fp, fontsize=10, color=MCK_DARK)

for i, (cnt, cvr) in enumerate(zip(top_kw['reg_count'].values, top_kw['conversion_rate'].values)):
    ax.text(cnt + max(top_kw['reg_count'].values)*0.01, i, f'{cnt:,} (CVR {cvr:.1f}%)',
            ha='left', va='center', fontproperties=fp, fontsize=9, color=MCK_DARK)

ax.set_xlim(0, max(top_kw['reg_count'].values) * 1.35)
style_mckinsey_axes(ax)
ax.spines['left'].set_visible(True)
ax.spines['left'].set_color(MCK_LINE)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 6',
    title='Display and PMax dominate keyword volume,\nbut branded/specific keywords show higher conversion',
    subtitle='Top 20 keywords by registration volume, with conversion rate (CVR)',
    legend_items=[('CVR > 10%', MCK_CYAN), ('CVR <= 10%', MCK_GRAY)],
    source='128 Channel User Data')

plt.savefig(f'{OUTPUT_DIR}/06_keyword_top20.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Chart 6 saved.")

# ============================================================
# CHART 7: 关键词 - 充值转化率 Top 20 (最少50注册)
# ============================================================
print("\n=== Chart 7: Keyword conversion rate ranking ===")

kw_all_stats = kw_df.groupby('关键词').agg(
    reg_count=('company_id', 'count'),
    recharge_count=('has_recharge', 'sum'),
    total_revenue=('累计充值金额$', 'sum')
)
kw_all_stats['conversion_rate'] = (kw_all_stats['recharge_count'] / kw_all_stats['reg_count'] * 100).round(1)
# Min 50 registrations
kw_cvr_top = kw_all_stats[kw_all_stats['reg_count'] >= 50].sort_values('conversion_rate', ascending=False).head(20)

print(kw_cvr_top.to_string())

fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor('white'); ax.set_facecolor('white')
fig.subplots_adjust(left=0.22, right=0.96, top=0.72, bottom=0.10)

top_cvr = kw_cvr_top.sort_values('conversion_rate', ascending=True)
y_pos = range(len(top_cvr))
bars = ax.barh(list(y_pos), top_cvr['conversion_rate'].values, height=0.6, color=MCK_CYAN, zorder=3)

ax.set_yticks(list(y_pos))
ax.set_yticklabels(top_cvr.index, fontproperties=fp, fontsize=10, color=MCK_DARK)

for i, (cvr, reg, rev) in enumerate(zip(top_cvr['conversion_rate'].values, top_cvr['reg_count'].values, top_cvr['total_revenue'].values)):
    ax.text(cvr + 0.5, i, f'{cvr:.1f}% (n={reg:,}, ${rev:,.0f})',
            ha='left', va='center', fontproperties=fp, fontsize=9, color=MCK_DARK)

ax.set_xlim(0, max(top_cvr['conversion_rate'].values) * 1.5)
style_mckinsey_axes(ax)
ax.spines['left'].set_visible(True)
ax.spines['left'].set_color(MCK_LINE)

apply_mckinsey_frame(fig, ax,
    exhibit_label='Exhibit 7',
    title='Specific product keywords drive significantly higher\nconversion than generic campaign keywords',
    subtitle='Top 20 keywords by conversion rate (min 50 registrations)',
    legend_items=[],
    source='128 Channel User Data')

plt.savefig(f'{OUTPUT_DIR}/07_keyword_cvr_ranking.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Chart 7 saved.")

# ============================================================
# Export data tables to CSV
# ============================================================
print("\n=== Exporting data tables ===")

# Monthly registration table
monthly_export = monthly_combined[['month_str','registered','recharged','conversion_rate']].copy()
monthly_export.columns = ['Month', 'Registered', 'Recharged', 'Conversion Rate (%)']
monthly_export.to_csv(f'{OUTPUT_DIR}/monthly_registration_data.csv', index=False)

# Keyword stats table
kw_export = kw_all_stats.reset_index()
kw_export.columns = ['Keyword', 'Registrations', 'Recharges', 'Total Revenue ($)', 'Conversion Rate (%)']
kw_export = kw_export.sort_values('Registrations', ascending=False)
kw_export.to_csv(f'{OUTPUT_DIR}/keyword_analysis_data.csv', index=False)

# ytag source table
ytag_stats = df.groupby(df['综合ytag'].astype(str).apply(
    lambda x: 'ggsem' if 'ggsem' in x.lower() else ('Other ytag' if x != '0' else 'No ytag')
)).agg(
    users=('company_id', 'count'),
    recharge_users=('has_recharge', 'sum'),
    total_revenue=('累计充值金额$', 'sum')
)
ytag_stats['pct'] = (ytag_stats['users'] / total_users * 100).round(1)
ytag_stats['conversion_rate'] = (ytag_stats['recharge_users'] / ytag_stats['users'] * 100).round(1)
ytag_stats.to_csv(f'{OUTPUT_DIR}/ytag_source_summary.csv')

print("\n=== ALL DONE ===")
print(f"Output files in: {OUTPUT_DIR}/")
for f in sorted(os.listdir(OUTPUT_DIR)):
    fsize = os.path.getsize(f'{OUTPUT_DIR}/{f}')
    print(f"  {f} ({fsize/1024:.0f}KB)")
