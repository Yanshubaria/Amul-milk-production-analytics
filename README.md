# 🥛 AMUL Milk Production & Sales Analyst System

A complete data analytics web application for analyzing AMUL milk production, product sales, revenue, profitability, quality, regional performance, and farmer procurement data.

---

## 📋 Project Overview

The **AMUL Milk Production & Sales Analyst System** is a Flask-based data analytics web application developed to analyze dairy production and sales operations.

The system processes and visualizes:

* More than **58,400 milk production records**
* More than **58,400 sales records**
* **200 farmer profiles**
* **10 analytical charts**
* Production, sales, revenue, profit, quality, and regional performance data
* Farmer procurement and milk-quality information

The application provides interactive dashboards, analytical reports, performance comparisons, and REST API endpoints for accessing processed data.

---

## ✨ Key Features

### Executive Dashboard

* Eight KPI cards
* Total revenue
* Total profit
* Total milk production
* Total quantity sold
* Average profit margin
* Year-over-year revenue growth
* Top-performing region
* Top-performing product
* Monthly revenue trend for 2023 and 2024
* Revenue distribution by product category
* Region-wise revenue analysis
* Year-over-year performance comparison

### Production Analysis

* Monthly production analysis
* Year-based production filters
* Production by product category
* Region-wise production comparison
* Seasonal production heatmap
* Milk quality-grade distribution
* Grade A, Grade B, and Grade C analysis

### Sales and Revenue Analysis

* Monthly sales and revenue analysis
* Product performance leaderboard
* Region-wise sales performance
* Profit analysis
* Average profit margin by category
* Cumulative revenue growth
* Top-performing products
* Product-category breakdown
* Yearly sales comparison

### Farmer Procurement Analysis

* Directory of 200 farmer profiles
* Paginated farmer records
* Region-based farmer filtering
* Total daily milk procurement
* Average daily milk contribution per farmer
* Average fat percentage
* Average protein percentage
* Average payment per litre
* Average association duration with AMUL
* Region-wise farmer procurement analysis

### Annual Reports

* Report selection for 2023 and 2024
* Total annual revenue
* Total annual profit
* Total production
* Total quantity sold
* Average profit margin
* Best-performing month
* Best-performing product
* Best-performing region
* Monthly performance breakdown
* Product-category revenue and profit analysis

---

## 🗂️ Project Structure

```text
milk_project/
│
├── app.py
├── generate_data.py
├── generate_charts.py
├── requirements.txt
├── run_project.bat
├── README.md
│
├── data/
│   ├── milk_production.csv
│   ├── milk_sales.csv
│   └── farmers.csv
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── production.html
│   ├── sales.html
│   ├── farmers.html
│   └── reports.html
│
└── static/
    └── charts/
        ├── chart_revenue_trend.png
        ├── chart_category_donut.png
        ├── chart_region_revenue.png
        ├── chart_seasonal_heatmap.png
        ├── chart_top_products.png
        ├── chart_profit_margin.png
        ├── chart_weekly_pattern.png
        ├── chart_prod_vs_sales.png
        ├── chart_cumulative_revenue.png
        └── chart_farmer_regions.png
```

---

## 🛠️ Technology Stack

| Layer                    | Technology                      |
| ------------------------ | ------------------------------- |
| Backend                  | Python 3.x, Flask               |
| Data Processing          | Pandas, NumPy                   |
| Data Visualization       | Matplotlib, Seaborn             |
| Machine Learning Library | Scikit-learn                    |
| Frontend                 | HTML5, CSS3, Vanilla JavaScript |
| Data Storage             | CSV files                       |
| Spreadsheet Support      | OpenPyXL                        |
| API Format               | JSON REST API                   |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/amul-milk-production-analytics.git
```

Move into the project directory:

```bash
cd amul-milk-production-analytics
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies

```bash
pip install flask pandas numpy matplotlib seaborn scikit-learn openpyxl
```

Alternatively, install the dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

### 1. Generate the Datasets

Run this command when the CSV files are not already available inside the `data` folder:

```bash
python generate_data.py
```

This script generates:

* `milk_production.csv`
* `milk_sales.csv`
* `farmers.csv`

### 2. Generate the Charts

Run the following command after generating the datasets:

```bash
python generate_charts.py
```

The generated charts will be saved inside:

```text
static/charts/
```

### 3. Start the Flask Application

```bash
python app.py
```

### 4. Open the Application

Open the following address in your browser:

```text
http://localhost:5050
```

---

## 🪟 Running on Windows

Windows users can also run the application using:

```text
run_project.bat
```

Double-click the file or execute it through Command Prompt:

```bash
run_project.bat
```

---

## 📈 Dataset Summary

| Dataset         | Number of Records | Period                       |
| --------------- | ----------------: | ---------------------------- |
| Milk Production |           58,400+ | January 2023 – December 2024 |
| Sales Records   |           58,400+ | January 2023 – December 2024 |
| Farmer Profiles |               200 | Static reference data        |

---

## 🥛 Products Included

The system includes data for the following AMUL products:

* Amul Gold Milk
* Amul Taaza Milk
* Amul Shakti Milk
* Amul Butter
* Amul Cheese
* Amul Ice Cream
* Amul Ghee
* Amul Paneer
* Amul Curd
* Amul Lassi

---

## 📍 Regions Included

The application analyzes data from the following regions:

* Gujarat
* Maharashtra
* Rajasthan
* Delhi
* Uttar Pradesh
* Karnataka
* Tamil Nadu
* West Bengal

---

## 📊 Generated Visualizations

The project generates the following charts:

1. Monthly revenue trend for 2023 and 2024
2. Revenue share by product category
3. Region-wise total revenue
4. Seasonal production heatmap
5. Top products by revenue
6. Average profit margin by category
7. Weekly sales pattern
8. Monthly production versus sales
9. Cumulative revenue growth
10. Farmer procurement by region

---

## 📡 API Endpoints

### KPI Endpoint

| Method | Endpoint    | Description                             |
| ------ | ----------- | --------------------------------------- |
| GET    | `/api/kpis` | Returns all major dashboard KPI metrics |

### Production Endpoints

| Method | Endpoint                      | Description                            |
| ------ | ----------------------------- | -------------------------------------- |
| GET    | `/api/production/monthly`     | Returns monthly production data        |
| GET    | `/api/production/by-category` | Returns production grouped by category |
| GET    | `/api/production/by-region`   | Returns production grouped by region   |
| GET    | `/api/production/quality`     | Returns production by quality grade    |
| GET    | `/api/production/seasonal`    | Returns seasonal production data       |

### Sales Endpoints

| Method | Endpoint                        | Description                                         |
| ------ | ------------------------------- | --------------------------------------------------- |
| GET    | `/api/sales/monthly`            | Returns monthly revenue, profit, and sales quantity |
| GET    | `/api/sales/by-product`         | Returns product-wise sales performance              |
| GET    | `/api/sales/by-region`          | Returns region-wise sales performance               |
| GET    | `/api/sales/yearly-comparison`  | Returns yearly sales comparison                     |
| GET    | `/api/sales/top-products`       | Returns the top-performing products                 |
| GET    | `/api/sales/category-breakdown` | Returns category-wise sales performance             |

### Farmer Endpoints

| Method | Endpoint                 | Description                            |
| ------ | ------------------------ | -------------------------------------- |
| GET    | `/api/farmers/summary`   | Returns farmer procurement KPIs        |
| GET    | `/api/farmers/by-region` | Returns region-wise farmer statistics  |
| GET    | `/api/farmers/list`      | Returns the paginated farmer directory |

### Report Endpoint

| Method | Endpoint              | Description                                  |
| ------ | --------------------- | -------------------------------------------- |
| GET    | `/api/reports/annual` | Returns a complete annual performance report |

---

## 🔎 Example API Requests

Retrieve all dashboard KPIs:

```text
http://localhost:5050/api/kpis
```

Retrieve production data for 2024:

```text
http://localhost:5050/api/production/monthly?year=2024
```

Retrieve the top five products:

```text
http://localhost:5050/api/sales/top-products?n=5
```

Retrieve the first page of farmer records:

```text
http://localhost:5050/api/farmers/list?page=1&per=20
```

Retrieve the annual report for 2023:

```text
http://localhost:5050/api/reports/annual?year=2023
```

---

## 🎯 Project Objectives

The primary objectives of this project are:

* To analyze milk production and dairy product sales
* To identify production and sales trends
* To compare regional performance
* To evaluate product profitability
* To assess seasonal production patterns
* To analyze milk quality indicators
* To organize and evaluate farmer procurement data
* To provide management-friendly dashboards and reports
* To demonstrate the use of Python and Flask in data analytics

---

## ⚠️ Data Disclaimer

The data used in this project is generated for educational, analytical, and demonstration purposes.

This repository is not an official AMUL software product. The generated records should not be interpreted as AMUL's actual confidential production, sales, financial, or farmer data.

AMUL product names and trademarks belong to their respective owner.

---

## 👩‍🎓 Academic Information

**Student:** Yanshu Baria
**Enrollment Number:** 70552300076
**Program:** Computer Science
**College:** SVKM's NMIMS

---

## 📄 License

This project is intended for educational and academic use.

Before applying an open-source license, ensure that all source code, datasets, images, logos, and other materials included in the repository are eligible for public redistribution.

---

## 📬 Contact

**Yanshu Baria**
Computer Science
**Mukesh Patel School of Technology Management and Engineering**
