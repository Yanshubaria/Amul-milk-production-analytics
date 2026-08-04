from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import os, json

app = Flask(__name__)

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, 'data')

# ── Load Data ─────────────────────────────────────────────────────────────────
prod_df   = pd.read_csv(f'{DATA}/milk_production.csv')
sales_df  = pd.read_csv(f'{DATA}/milk_sales.csv')
farmer_df = pd.read_csv(f'{DATA}/farmers.csv')

def to_json(df): return df.to_dict(orient='records')

# ─────────────────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/')
def index(): return render_template('index.html')

@app.route('/production')
def production(): return render_template('production.html')

@app.route('/sales')
def sales(): return render_template('sales.html')

@app.route('/farmers')
def farmers(): return render_template('farmers.html')

@app.route('/reports')
def reports(): return render_template('reports.html')

# ─────────────────────────────────────────────────────────────────────────────
# API – KPI SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/kpis')
def kpis():
    total_revenue   = round(sales_df['revenue'].sum() / 1e6, 2)
    total_profit    = round(sales_df['profit'].sum() / 1e6, 2)
    total_prod      = round(prod_df['quantity_litres'].sum() / 1e6, 2)
    total_sold      = round(sales_df['quantity_sold'].sum() / 1e6, 2)
    avg_margin      = round(sales_df['profit_margin_pct'].mean(), 2)
    total_farmers   = len(farmer_df)
    yoy_rev         = sales_df.groupby('year')['revenue'].sum()
    yoy_growth      = round((yoy_rev[2024]-yoy_rev[2023])/yoy_rev[2023]*100, 2) if 2023 in yoy_rev and 2024 in yoy_rev else 0
    return jsonify({
        'total_revenue_m':   total_revenue,
        'total_profit_m':    total_profit,
        'total_production_m':total_prod,
        'total_sold_m':      total_sold,
        'avg_profit_margin': avg_margin,
        'total_farmers':     total_farmers,
        'yoy_growth_pct':    yoy_growth,
        'top_region':        sales_df.groupby('region')['revenue'].sum().idxmax(),
        'top_product':       sales_df.groupby('product')['revenue'].sum().idxmax(),
        'top_category':      sales_df.groupby('category')['revenue'].sum().idxmax(),
    })

# ─────────────────────────────────────────────────────────────────────────────
# API – PRODUCTION
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/production/monthly')
def prod_monthly():
    year = request.args.get('year', 'all')
    df = prod_df if year == 'all' else prod_df[prod_df['year'] == int(year)]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    result = df.groupby('month')['quantity_litres'].sum().reindex(months).fillna(0).reset_index()
    result.columns = ['month','quantity']
    return jsonify(result.to_dict(orient='records'))

@app.route('/api/production/by-category')
def prod_by_category():
    result = prod_df.groupby('category')['quantity_litres'].sum().reset_index()
    result.columns = ['category','quantity']
    return jsonify(result.sort_values('quantity', ascending=False).to_dict(orient='records'))

@app.route('/api/production/by-region')
def prod_by_region():
    result = prod_df.groupby('region')['quantity_litres'].sum().reset_index()
    result.columns = ['region','quantity']
    return jsonify(result.sort_values('quantity', ascending=False).to_dict(orient='records'))

@app.route('/api/production/quality')
def prod_quality():
    result = prod_df.groupby('quality_grade')['quantity_litres'].sum().reset_index()
    result.columns = ['grade','quantity']
    return jsonify(result.to_dict(orient='records'))

@app.route('/api/production/seasonal')
def prod_seasonal():
    result = prod_df.groupby(['season','category'])['quantity_litres'].sum().reset_index()
    result.columns = ['season','category','quantity']
    return jsonify(result.to_dict(orient='records'))

# ─────────────────────────────────────────────────────────────────────────────
# API – SALES
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/sales/monthly')
def sales_monthly():
    year = request.args.get('year', 'all')
    df = sales_df if year == 'all' else sales_df[sales_df['year'] == int(year)]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    result = df.groupby('month').agg(revenue=('revenue','sum'), profit=('profit','sum'),
                                      quantity=('quantity_sold','sum')).reindex(months).fillna(0).reset_index()
    result.columns = ['month','revenue','profit','quantity']
    return jsonify(result.to_dict(orient='records'))

@app.route('/api/sales/by-product')
def sales_by_product():
    result = sales_df.groupby('product').agg(
        revenue=('revenue','sum'), profit=('profit','sum'),
        margin=('profit_margin_pct','mean'), qty=('quantity_sold','sum')
    ).reset_index().sort_values('revenue', ascending=False)
    return jsonify(result.round(2).to_dict(orient='records'))

@app.route('/api/sales/by-region')
def sales_by_region():
    result = sales_df.groupby('region').agg(
        revenue=('revenue','sum'), profit=('profit','sum'),
        qty=('quantity_sold','sum'), margin=('profit_margin_pct','mean')
    ).reset_index().sort_values('revenue', ascending=False)
    return jsonify(result.round(2).to_dict(orient='records'))

@app.route('/api/sales/yearly-comparison')
def sales_yearly():
    result = sales_df.groupby('year').agg(
        revenue=('revenue','sum'), profit=('profit','sum'),
        qty=('quantity_sold','sum'), margin=('profit_margin_pct','mean')
    ).reset_index()
    return jsonify(result.round(2).to_dict(orient='records'))

@app.route('/api/sales/top-products')
def sales_top():
    n = int(request.args.get('n', 5))
    result = sales_df.groupby('product').agg(
        revenue=('revenue','sum'), profit=('profit','sum'), margin=('profit_margin_pct','mean')
    ).nlargest(n,'revenue').reset_index()
    return jsonify(result.round(2).to_dict(orient='records'))

@app.route('/api/sales/category-breakdown')
def sales_category():
    result = sales_df.groupby('category').agg(
        revenue=('revenue','sum'), profit=('profit','sum'),
        margin=('profit_margin_pct','mean'), qty=('quantity_sold','sum')
    ).reset_index().sort_values('revenue', ascending=False)
    return jsonify(result.round(2).to_dict(orient='records'))

# ─────────────────────────────────────────────────────────────────────────────
# API – FARMERS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/farmers/summary')
def farmers_summary():
    return jsonify({
        'total_farmers': len(farmer_df),
        'total_daily_litres': round(farmer_df['avg_daily_litres'].sum(), 1),
        'avg_daily_per_farmer': round(farmer_df['avg_daily_litres'].mean(), 1),
        'avg_fat': round(farmer_df['fat_avg'].mean(), 2),
        'avg_protein': round(farmer_df['protein_avg'].mean(), 2),
        'avg_payment_per_litre': round(farmer_df['payment_per_litre'].mean(), 2),
        'avg_years_with_amul': round(farmer_df['years_with_amul'].mean(), 1),
    })

@app.route('/api/farmers/by-region')
def farmers_by_region():
    result = farmer_df.groupby('region').agg(
        count=('farmer_id','count'),
        total_litres=('avg_daily_litres','sum'),
        avg_fat=('fat_avg','mean'),
        avg_cattle=('cattle_count','mean')
    ).reset_index().sort_values('total_litres', ascending=False)
    return jsonify(result.round(2).to_dict(orient='records'))

@app.route('/api/farmers/list')
def farmers_list():
    page = int(request.args.get('page', 1))
    per  = int(request.args.get('per', 20))
    region = request.args.get('region', '')
    df = farmer_df if not region else farmer_df[farmer_df['region']==region]
    total = len(df)
    chunk = df.iloc[(page-1)*per : page*per]
    return jsonify({'total': total, 'page': page, 'data': chunk.round(2).to_dict(orient='records')})

# ─────────────────────────────────────────────────────────────────────────────
# API – REPORT DATA
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/api/reports/annual')
def annual_report():
    year = int(request.args.get('year', 2024))
    s = sales_df[sales_df['year']==year]
    p = prod_df[prod_df['year']==year]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    monthly = s.groupby('month').agg(revenue=('revenue','sum'), profit=('profit','sum'),
                                      qty=('quantity_sold','sum')).reindex(months).fillna(0)
    best_month = monthly['revenue'].idxmax()
    return jsonify({
        'year': year,
        'total_revenue': round(s['revenue'].sum()),
        'total_profit': round(s['profit'].sum()),
        'total_production': round(p['quantity_litres'].sum()),
        'total_sales_qty': round(s['quantity_sold'].sum()),
        'avg_margin': round(s['profit_margin_pct'].mean(), 2),
        'best_month': best_month,
        'best_product': s.groupby('product')['revenue'].sum().idxmax(),
        'best_region': s.groupby('region')['revenue'].sum().idxmax(),
        'monthly': monthly.reset_index().round(2).to_dict(orient='records'),
        'by_category': s.groupby('category').agg(revenue=('revenue','sum'), profit=('profit','sum')).reset_index().round(2).to_dict(orient='records'),
    })

if __name__ == '__main__':
    app.run(debug=True, port=5050)
