import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, os

random.seed(42)
np.random.seed(42)

OUT = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(OUT, exist_ok=True)

# ── Config ────────────────────────────────────────────────────────────────────
PRODUCTS = {
    'Amul Gold Milk':      {'category':'Milk',       'base_price':32,  'cost':22},
    'Amul Taaza Milk':     {'category':'Milk',       'base_price':26,  'cost':18},
    'Amul Shakti Milk':    {'category':'Milk',       'base_price':28,  'cost':19},
    'Amul Butter':         {'category':'Butter',     'base_price':56,  'cost':38},
    'Amul Cheese':         {'category':'Cheese',     'base_price':110, 'cost':72},
    'Amul Ice Cream':      {'category':'Ice Cream',  'base_price':80,  'cost':50},
    'Amul Ghee':           {'category':'Ghee',       'base_price':580, 'cost':390},
    'Amul Paneer':         {'category':'Paneer',     'base_price':90,  'cost':60},
    'Amul Curd':           {'category':'Curd',       'base_price':22,  'cost':14},
    'Amul Lassi':          {'category':'Lassi',      'base_price':20,  'cost':12},
}
REGIONS = ['Gujarat','Maharashtra','Rajasthan','Delhi','Uttar Pradesh','Karnataka','Tamil Nadu','West Bengal']
SEASONS = {'Jan':'Winter','Feb':'Winter','Mar':'Spring','Apr':'Spring',
           'May':'Summer','Jun':'Summer','Jul':'Monsoon','Aug':'Monsoon',
           'Sep':'Monsoon','Oct':'Autumn','Nov':'Autumn','Dec':'Winter'}
DATES = [datetime(2023,1,1) + timedelta(days=i) for i in range(730)]  # 2 years

# ── Production Data ───────────────────────────────────────────────────────────
prod_rows = []
for date in DATES:
    month = date.strftime('%b')
    season = SEASONS[month]
    # seasonal multiplier for milk production
    season_mult = {'Winter':1.15,'Spring':1.05,'Summer':0.90,'Monsoon':0.95,'Autumn':1.0}[season]
    for product, info in PRODUCTS.items():
        for region in REGIONS:
            region_mult = {'Gujarat':1.3,'Maharashtra':1.2,'Rajasthan':1.1,'Delhi':1.15,
                           'Uttar Pradesh':1.0,'Karnataka':0.95,'Tamil Nadu':0.9,'West Bengal':0.85}[region]
            base_qty = {'Milk':5000,'Butter':800,'Cheese':400,'Ice Cream':600,
                        'Ghee':300,'Paneer':700,'Curd':1200,'Lassi':900}[info['category']]
            noise = np.random.normal(1.0, 0.08)
            qty = max(50, int(base_qty * season_mult * region_mult * noise))
            fat_pct    = round(np.random.normal(4.2, 0.3), 2) if info['category']=='Milk' else None
            protein_pct= round(np.random.normal(3.4, 0.2), 2) if info['category']=='Milk' else None
            quality    = 'Grade A' if (fat_pct or 4)>3.8 and (protein_pct or 3.2)>3.2 else ('Grade B' if (fat_pct or 4)>3.5 else 'Grade C')
            prod_rows.append({
                'date': date.strftime('%Y-%m-%d'),
                'month': month,
                'year': date.year,
                'quarter': f"Q{(date.month-1)//3+1}",
                'season': season,
                'product': product,
                'category': info['category'],
                'region': region,
                'quantity_litres': qty,
                'fat_percentage': fat_pct,
                'protein_percentage': protein_pct,
                'quality_grade': quality,
                'production_cost_per_unit': info['cost'],
                'total_production_cost': round(qty * info['cost'] / 100, 2),
            })

prod_df = pd.DataFrame(prod_rows)
prod_df.to_csv(f'{OUT}/milk_production.csv', index=False)
print(f"Production: {len(prod_df):,} rows")

# ── Sales Data ────────────────────────────────────────────────────────────────
sales_rows = []
for date in DATES:
    month = date.strftime('%b')
    season = SEASONS[month]
    dow = date.weekday()  # 0=Mon
    weekend_boost = 1.12 if dow >= 5 else 1.0
    season_sales = {'Winter':1.1,'Spring':1.0,'Summer':1.2,'Monsoon':0.95,'Autumn':1.05}[season]
    for product, info in PRODUCTS.items():
        for region in REGIONS:
            region_demand = {'Gujarat':1.25,'Maharashtra':1.30,'Rajasthan':1.0,'Delhi':1.35,
                             'Uttar Pradesh':1.1,'Karnataka':1.05,'Tamil Nadu':1.0,'West Bengal':0.9}[region]
            base_qty = {'Milk':4500,'Butter':750,'Cheese':380,'Ice Cream':700,
                        'Ghee':280,'Paneer':650,'Curd':1100,'Lassi':850}[info['category']]
            noise = np.random.normal(1.0, 0.10)
            qty_sold = max(10, int(base_qty * season_sales * region_demand * weekend_boost * noise))
            price = info['base_price'] * np.random.uniform(0.97, 1.05)
            revenue = round(qty_sold * price / 100, 2)
            profit  = round(revenue - (qty_sold * info['cost'] / 100), 2)
            sales_rows.append({
                'date': date.strftime('%Y-%m-%d'),
                'month': month,
                'year': date.year,
                'quarter': f"Q{(date.month-1)//3+1}",
                'season': season,
                'day_of_week': date.strftime('%A'),
                'is_weekend': dow >= 5,
                'product': product,
                'category': info['category'],
                'region': region,
                'quantity_sold': qty_sold,
                'price_per_unit': round(price, 2),
                'revenue': revenue,
                'cost': round(qty_sold * info['cost'] / 100, 2),
                'profit': profit,
                'profit_margin_pct': round((profit / revenue * 100) if revenue > 0 else 0, 2),
            })

sales_df = pd.DataFrame(sales_rows)
sales_df.to_csv(f'{OUT}/milk_sales.csv', index=False)
print(f"Sales: {len(sales_df):,} rows")

# ── Farmer Procurement Data ───────────────────────────────────────────────────
farmers = []
for i in range(200):
    region = random.choice(REGIONS)
    farmers.append({
        'farmer_id': f'F{i+1:04d}',
        'farmer_name': f'Farmer {i+1}',
        'village': f'Village {random.randint(1,50)}',
        'region': region,
        'cattle_count': random.randint(5, 80),
        'avg_daily_litres': round(random.uniform(20, 300), 1),
        'fat_avg': round(random.uniform(3.5, 5.0), 2),
        'protein_avg': round(random.uniform(3.0, 3.8), 2),
        'years_with_amul': random.randint(1, 30),
        'payment_per_litre': round(random.uniform(28, 38), 2),
    })
farmer_df = pd.DataFrame(farmers)
farmer_df.to_csv(f'{OUT}/farmers.csv', index=False)
print(f"Farmers: {len(farmer_df):,} rows")

print("\n[SUCCESS] All datasets generated successfully!")
print(f"   Production : {OUT}/milk_production.csv")
print(f"   Sales      : {OUT}/milk_sales.csv")
print(f"   Farmers    : {OUT}/farmers.csv")
