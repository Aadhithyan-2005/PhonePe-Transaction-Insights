# 📱 PhonePe Transaction Insights

![PhonePe](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/PhonePe_Logo.svg/320px-PhonePe_Logo.svg.png)

## 📌 Project Overview

A comprehensive data analysis project on PhonePe's digital payment transaction data spanning **2018 to 2024** across all Indian states and union territories. The project covers end-to-end data engineering, exploratory data analysis, hypothesis testing, machine learning and an interactive Streamlit dashboard.

| Detail | Info |
|--------|------|
| **Domain** | Finance / Payment Systems |
| **Project Type** | EDA + Data Analysis + ML |
| **Database** | PostgreSQL 18 |
| **Total Records** | 116,799 rows across 9 tables |
| **Data Period** | 2018 – 2024 |
| **States Covered** | 36 States & Union Territories |

---

## 🎯 Problem Statement

With the increasing reliance on digital payment systems like PhonePe, understanding the dynamics of transactions, user engagement, and insurance-related data is crucial for improving services and targeting users effectively. This project aims to:

- Analyze aggregated values of payment categories across states and quarters
- Create geographic visualizations for total transaction values at state and district levels
- Identify top-performing states, districts, and pin codes
- Build a machine learning model to predict transaction amounts
- Generate actionable business insights from the data

---

## 🗂️ Project Structure

```
PhonePe-Transaction-Insights/
│
├── pulse/                              # Cloned PhonePe Pulse GitHub repo
│
├── data_extraction.py                  # ETL - Parse JSON files into DataFrames
├── db_setup.py                         # Create PostgreSQL tables
├── db_load.py                          # Load DataFrames into PostgreSQL
│
├── PhonePe_Analysis.ipynb              # Main analysis notebook
├── dashboard.py                        # Streamlit interactive dashboard
├── sql_queries.sql                     # 20 Business SQL queries
│
├── best_model_xgb.pkl                  # Saved XGBoost model
├── scaler.pkl                          # Saved StandardScaler
│
├── PhonePe_Transaction_Insights_Report.pdf  # Project report
└── README.md                           # This file
```

---

## 🗄️ Database Schema

9 tables were created in PostgreSQL to store the PhonePe Pulse data:

| Table | Rows | Description |
|-------|------|-------------|
| `aggregated_transaction` | 5,034 | State-wise transaction data by payment category |
| `aggregated_user` | 7,128 | State-wise user and device data |
| `aggregated_insurance` | 682 | State-wise insurance transaction data |
| `map_transaction` | 20,604 | District-level transaction data |
| `map_user` | 20,608 | District-level user data |
| `map_insurance` | 13,876 | District-level insurance data |
| `top_transaction` | 18,295 | Top districts and pincodes by transactions |
| `top_user` | 18,296 | Top districts and pincodes by users |
| `top_insurance` | 12,276 | Top districts and pincodes by insurance |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.x
- PostgreSQL 18
- Git

### Step 1 — Clone this repository
```bash
git clone https://github.com/Aadhithyan-2005/PhonePe-Transaction-Insights.git
cd PhonePe-Transaction-Insights
```

### Step 2 — Clone PhonePe Pulse data
```bash
git clone https://github.com/PhonePe/pulse.git
```

### Step 3 — Install dependencies
```bash
pip install pandas sqlalchemy psycopg2-binary plotly matplotlib seaborn streamlit xgboost scikit-learn jupyter ipykernel
```

### Step 4 — Configure database
Open `db_setup.py` and update your PostgreSQL credentials:
```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "phonepe_db",
    "user":     "postgres",
    "password": "your_password",  # ← Update this
}
```

### Step 5 — Create database in PostgreSQL
```bash
psql -U postgres
CREATE DATABASE phonepe_db;
\q
```

### Step 6 — Load data into PostgreSQL
```bash
python db_load.py
```

This will extract all JSON files, create 9 tables and load 116,799 rows.

### Step 7 — Run the Jupyter Notebook
```bash
jupyter notebook PhonePe_Analysis.ipynb
```

### Step 8 — Launch Streamlit Dashboard
```bash
streamlit run dashboard.py
```

---

## 📊 Analysis Highlights

### 15 Charts (UBM Framework)

**Univariate Analysis**
- Transaction Type Distribution (Donut Chart)
- Top 10 States by Transaction Amount (Bar Chart)
- Quarterly Transaction Trend (Line Chart)
- Top 10 States by Registered Users (Bar Chart)
- Mobile Device Brand Distribution (Bar Chart)

**Bivariate Analysis**
- Transaction Count vs Amount by State (Scatter Plot)
- Year-wise Transaction Growth (Grouped Bar Chart)
- Transaction Amount by Payment Type (Box Plot)
- App Opens vs Registered Users (Scatter Plot)
- Top States by Insurance Amount (Bar Chart)

**Multivariate Analysis**
- Quarter-wise Trend by Year (Multi-Line Chart)
- Top 15 Districts by Transaction Amount (Bar Chart)
- State-wise User Growth Heatmap
- Correlation Heatmap
- Pair Plot of Key Metrics

---

## 🔬 Hypothesis Testing

| Hypothesis | Test Used | Result |
|-----------|-----------|--------|
| Southern states have higher transaction amounts than Northern states | Mann-Whitney U Test | ✅ Confirmed |
| Q4 transaction amounts are significantly higher than other quarters | Mann-Whitney U Test | ✅ Confirmed |
| Positive correlation between registered users and transaction count | Spearman Rank Correlation | ✅ Confirmed |

All three null hypotheses were rejected at **95% confidence level (p < 0.05)**

---

## 🤖 Machine Learning Models

**Target Variable:** Transaction Amount (log transformed)

**Features Used:**
- state_encoded, transaction_type_encoded
- year, quarter, transaction_count
- avg_transaction_value *(engineered)*
- is_q4, is_recent, year_quarter_num *(engineered)*

| Model | Tuning Method | Result |
|-------|--------------|--------|
| Linear Regression | 5-Fold Cross Validation | Baseline |
| Random Forest | RandomizedSearchCV | Improved |
| **XGBoost** | **GridSearchCV** | **Best** ✅ |

**XGBoost** was selected as the final model for its superior performance and production readiness.

---

## 🖥️ Streamlit Dashboard

The interactive dashboard has **5 pages:**

| Page | Content |
|------|---------|
| 🏠 Overview | KPI metrics, transaction type distribution, quarterly trend |
| 💳 Transactions | State-wise analysis, heatmap, payment category breakdown |
| 👥 Users | Registered users, device brands, engagement analysis |
| 🛡️ Insurance | State-wise insurance analysis, trend over time |
| 🏆 Top Performers | Top districts, pincodes, raw data viewer |

**Run the dashboard:**
```bash
streamlit run dashboard.py
```

---

## 💡 Key Business Insights

1. **P2P transfers dominate** — Users primarily use PhonePe for money transfers between individuals
2. **Q4 is peak season** — Festive season drives maximum transaction volumes consistently
3. **Maharashtra leads** — Top state by both transaction amount and user count
4. **Xiaomi dominates** — Mid-range smartphone users form PhonePe's primary user base
5. **Southern states engage more** — Higher app opens per registered user ratio
6. **Insurance opportunity** — Massive untapped insurance market in tier 2 and tier 3 cities

---

## 🏆 Business Recommendations

- **Q4 Strategy** — Scale infrastructure and run maximum offers during festive season
- **State Targeting** — Premium products for top states, vernacular campaigns for low-engagement states
- **Device Partnerships** — Pre-installation deals with Xiaomi, Samsung and Vivo
- **User Activation** — Cashback campaigns for states with high users but low transactions
- **Insurance Expansion** — Simplified regional-language insurance products for tier 2 cities
- **Merchant Onboarding** — Target emerging tier 2 cities like Pune and Ahmedabad

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.x |
| Database | PostgreSQL 18 |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| ML Libraries | Scikit-learn, XGBoost |
| DB Connectivity | SQLAlchemy, psycopg2 |
| Statistical Tests | SciPy |
| Version Control | Git + GitHub |
| IDE | VS Code + Jupyter Notebook |

---

## 📁 Data Source

- **PhonePe Pulse GitHub Repository:** [https://github.com/PhonePe/pulse](https://github.com/PhonePe/pulse)

---

## 👤 Author

**Aadhithyan M**
- GitHub: [@Aadhithyan-2005](https://github.com/Aadhithyan-2005)

---

## 📄 License

This project is for educational purposes. Data sourced from PhonePe Pulse public repository.
