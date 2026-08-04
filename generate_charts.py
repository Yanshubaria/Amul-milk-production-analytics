import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import warnings, os
warnings.filterwarnings('ignore')

DATA = os.path.join(os.path.dirname(__file__), 'data')
OUT  = os.path.join(os.path.dirname(__file__), 'static', 'charts')
os.makedirs(OUT, exist_ok=True)

prod_df  = pd.read_csv(f'{DATA}/milk_production.csv')
sales_df = pd.read_csv(f'{DATA}/milk_sales.csv')
farmer_df= pd.read_csv(f'{DATA}/farmers.csv')

# ── Style ─────────────────────────────────────────────────────────────────────
AMUL_RED   = '#E8192C'
AMUL_GOLD  = '#F7B731'
AMUL_DARK  = '#1a1a2e'
AMUL_BLUE  = '#16213e'
COLORS     = [AMUL_RED,'#2196F3','#4CAF50','#FF9800','#9C27B0','#00BCD4','#FF5722','#607D8B']
plt.rcParams.update({'figure.facecolor':'#0f172a','axes.facecolor':'#1e293b',
                     'axes.edgecolor':'#334155','text.color':'white',
                     'axes.labelcolor':'white','xtick.color':'white',
                     'ytick.color':'white','grid.color':'#334155',
                     'grid.alpha':0.4,'font.family':'DejaVu Sans'})

def save(name):
    plt.tight_layout()
    plt.savefig(f'{OUT}/{name}.png', dpi=120, bbox_inches='tight',
                facecolor='#0f172a', edgecolor='none')
    plt.close()
    print(f"  * {name}.png")

print("Generating charts...")

# ── 1. Monthly Revenue Trend (2023 vs 2024) ───────────────────────────────────
fig, ax = plt.subplots(figsize=(12,5))
for year, color in [(2023, AMUL_RED), (2024, AMUL_GOLD)]:
    m = sales_df[sales_df['year']==year].groupby('month')['revenue'].sum().reset_index()
    mo = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    m['month'] = pd.Categorical(m['month'], categories=mo, ordered=True)
    m = m.sort_values('month')
    ax.plot(m['month'], m['revenue']/1e6, marker='o', linewidth=2.5,
            markersize=7, color=color, label=str(year))
    ax.fill_between(m['month'], m['revenue']/1e6, alpha=0.12, color=color)
ax.set_title('Monthly Revenue Trend — 2023 vs 2024', fontsize=16, fontweight='bold', pad=15, color='white')
ax.set_ylabel('Revenue (₹ Millions)', fontsize=12)
ax.legend(fontsize=12, facecolor='#1e293b', edgecolor='#334155', labelcolor='white')
ax.grid(True, alpha=0.3)
save('chart_revenue_trend')

# ── 2. Revenue by Product Category (Donut) ────────────────────────────────────
fig, ax = plt.subplots(figsize=(9,7))
cat_rev = sales_df.groupby('category')['revenue'].sum().sort_values(ascending=False)
wedges, texts, autotexts = ax.pie(
    cat_rev, labels=cat_rev.index, autopct='%1.1f%%',
    colors=COLORS[:len(cat_rev)], startangle=140,
    pctdistance=0.78, wedgeprops=dict(width=0.55, edgecolor='#0f172a', linewidth=2))
for t in texts: t.set_color('white'); t.set_fontsize(11)
for at in autotexts: at.set_color('white'); at.set_fontsize(10); at.set_fontweight('bold')
ax.set_title('Revenue Share by Product Category', fontsize=15, fontweight='bold', color='white', pad=20)
save('chart_category_donut')

# ── 3. Region-wise Sales Bar Chart ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12,5))
reg_rev = sales_df.groupby('region')['revenue'].sum().sort_values(ascending=False)
bars = ax.bar(reg_rev.index, reg_rev.values/1e6, color=COLORS[:len(reg_rev)],
              edgecolor='#0f172a', linewidth=0.8, width=0.6)
for bar, val in zip(bars, reg_rev.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'₹{val/1e6:.1f}M', ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')
ax.set_title('Region-wise Total Revenue', fontsize=16, fontweight='bold', color='white', pad=15)
ax.set_ylabel('Revenue (₹ Millions)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=15)
save('chart_region_revenue')

# ── 4. Seasonal Production Heatmap ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12,6))
pivot = prod_df.groupby(['season','category'])['quantity_litres'].sum().unstack(fill_value=0)
pivot = pivot.div(1e3)  # in thousands
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd',
            ax=ax, linewidths=0.5, linecolor='#0f172a',
            annot_kws={'size':10,'weight':'bold'},
            cbar_kws={'label':'Quantity (000s litres)'})
ax.set_title('Seasonal Production Heatmap (000s litres)', fontsize=15, fontweight='bold', color='white', pad=15)
ax.set_xlabel('Product Category', fontsize=12)
ax.set_ylabel('Season', fontsize=12)
ax.tick_params(colors='white')
save('chart_seasonal_heatmap')

# ── 5. Top 10 Product Revenue Bar ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12,5))
prod_rev = sales_df.groupby('product')['revenue'].sum().sort_values(ascending=True).tail(10)
colors_h = [AMUL_RED if i==len(prod_rev)-1 else '#2d6a9f' for i in range(len(prod_rev))]
bars = ax.barh(prod_rev.index, prod_rev.values/1e6, color=colors_h,
               edgecolor='#0f172a', linewidth=0.8)
for bar, val in zip(bars, prod_rev.values):
    ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
            f'₹{val/1e6:.1f}M', va='center', fontsize=10, color='white', fontweight='bold')
ax.set_title('Top Products by Total Revenue', fontsize=15, fontweight='bold', color='white', pad=15)
ax.set_xlabel('Revenue (₹ Millions)', fontsize=12)
ax.grid(axis='x', alpha=0.3)
save('chart_top_products')

# ── 6. Profit Margin by Category ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10,5))
pm = sales_df.groupby('category')['profit_margin_pct'].mean().sort_values(ascending=False)
bars = ax.bar(pm.index, pm.values, color=[AMUL_RED if v==pm.max() else AMUL_GOLD if v==pm.min() else '#2196F3' for v in pm.values],
              edgecolor='#0f172a', width=0.6)
for bar, val in zip(bars, pm.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
            f'{val:.1f}%', ha='center', fontsize=11, color='white', fontweight='bold')
ax.set_title('Average Profit Margin by Category', fontsize=15, fontweight='bold', color='white', pad=15)
ax.set_ylabel('Profit Margin (%)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
save('chart_profit_margin')

# ── 7. Weekly Sales Pattern ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10,5))
dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow_sales = sales_df.groupby('day_of_week')['revenue'].mean().reindex(dow_order)
bar_colors = [AMUL_RED if d in ['Saturday','Sunday'] else '#2d6a9f' for d in dow_order]
bars = ax.bar(dow_order, dow_sales.values/1e3, color=bar_colors, edgecolor='#0f172a', width=0.6)
for bar, val in zip(bars, dow_sales.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f'₹{val/1e3:.1f}K', ha='center', fontsize=10, color='white', fontweight='bold')
ax.set_title('Average Daily Revenue by Day of Week', fontsize=15, fontweight='bold', color='white', pad=15)
ax.set_ylabel('Avg Revenue (₹ Thousands)', fontsize=12)
ax.grid(axis='y', alpha=0.3)
weekend_patch = mpatches.Patch(color=AMUL_RED, label='Weekend')
weekday_patch = mpatches.Patch(color='#2d6a9f', label='Weekday')
ax.legend(handles=[weekend_patch, weekday_patch], facecolor='#1e293b', labelcolor='white')
plt.xticks(rotation=15)
save('chart_weekly_pattern')

# ── 8. Production vs Sales Comparison ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12,5))
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
p2024 = prod_df[prod_df['year']==2024].groupby('month')['quantity_litres'].sum()
s2024 = sales_df[sales_df['year']==2024].groupby('month')['quantity_sold'].sum()
p2024 = p2024.reindex(months).fillna(0)/1e6
s2024 = s2024.reindex(months).fillna(0)/1e6
x = np.arange(len(months))
w = 0.35
ax.bar(x-w/2, p2024, w, label='Production (M litres)', color=AMUL_RED, edgecolor='#0f172a', alpha=0.9)
ax.bar(x+w/2, s2024, w, label='Sales (M units)', color=AMUL_GOLD, edgecolor='#0f172a', alpha=0.9)
ax.set_xticks(x); ax.set_xticklabels(months)
ax.set_title('Monthly Production vs Sales — 2024', fontsize=15, fontweight='bold', color='white', pad=15)
ax.set_ylabel('Quantity (Millions)', fontsize=12)
ax.legend(facecolor='#1e293b', labelcolor='white')
ax.grid(axis='y', alpha=0.3)
save('chart_prod_vs_sales')

# ── 9. Cumulative Revenue Growth ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12,5))
for year, color in [(2023, '#2196F3'), (2024, AMUL_RED)]:
    d = sales_df[sales_df['year']==year].copy()
    d['date'] = pd.to_datetime(d['date'])
    daily = d.groupby('date')['revenue'].sum().reset_index()
    daily['cumulative'] = daily['revenue'].cumsum()/1e6
    ax.plot(range(len(daily)), daily['cumulative'], linewidth=2.5, color=color, label=str(year))
ax.fill_between(range(len(daily)), daily['cumulative']*0, daily['cumulative'], alpha=0.1, color=AMUL_RED)
ax.set_title('Cumulative Revenue Growth', fontsize=15, fontweight='bold', color='white', pad=15)
ax.set_ylabel('Cumulative Revenue (₹ Millions)', fontsize=12)
ax.set_xlabel('Day of Year', fontsize=12)
ax.legend(facecolor='#1e293b', labelcolor='white')
ax.grid(alpha=0.3)
save('chart_cumulative_revenue')

# ── 10. Farmer Region Distribution ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9,6))
freg = farmer_df.groupby('region')['avg_daily_litres'].sum().sort_values(ascending=False)
wedges, texts, autotexts = ax.pie(
    freg, labels=freg.index, autopct='%1.1f%%',
    colors=COLORS, startangle=90,
    wedgeprops=dict(edgecolor='#0f172a', linewidth=2))
for t in texts: t.set_color('white'); t.set_fontsize(10)
for at in autotexts: at.set_color('white'); at.set_fontsize(9); at.set_fontweight('bold')
ax.set_title('Farmer Procurement by Region\n(% of Daily Litres)', fontsize=14, fontweight='bold', color='white', pad=15)
save('chart_farmer_regions')

print("\n[SUCCESS] All 10 charts generated!")
