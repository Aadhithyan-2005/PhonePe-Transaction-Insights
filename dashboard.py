import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #5f259f; color: white; 
                border-radius: 10px; padding: 10px; }
    .stMetric label { color: white !important; }
    .stMetric div { color: white !important; }
    h1 { color: #5f259f; }
    h2 { color: #5f259f; }
    h3 { color: #5f259f; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────
@st.cache_resource
def get_engine():
    password = quote_plus("Eremika@0139")  
    return create_engine(
        f"postgresql+psycopg2://postgres:{password}@localhost:5432/phonepe_db"
    )

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    engine = get_engine()
    agg_trans = pd.read_sql("SELECT * FROM aggregated_transaction", engine)
    agg_user  = pd.read_sql("SELECT * FROM aggregated_user", engine)
    agg_ins   = pd.read_sql("SELECT * FROM aggregated_insurance", engine)
    map_trans = pd.read_sql("SELECT * FROM map_transaction", engine)
    map_user  = pd.read_sql("SELECT * FROM map_user", engine)
    top_trans = pd.read_sql("SELECT * FROM top_transaction", engine)
    top_user  = pd.read_sql("SELECT * FROM top_user", engine)

    # Clean state names
    for df in [agg_trans, agg_user, agg_ins, map_trans, map_user, top_trans, top_user]:
        df['state'] = df['state'].str.replace('-', ' ').str.title()

    return agg_trans, agg_user, agg_ins, map_trans, map_user, top_trans, top_user

# Load all data
agg_trans, agg_user, agg_ins, map_trans, map_user, top_trans, top_user = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/PhonePe_Logo.svg/320px-PhonePe_Logo.svg.png",
    width=200
)
st.sidebar.title("📊 Filters")

# Year filter
years = sorted(agg_trans['year'].unique())
selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(years))

# Quarter filter
quarters = sorted(agg_trans['quarter'].unique())
selected_quarter = st.sidebar.selectbox("Select Quarter", ["All"] + list(quarters))

# State filter
states = sorted(agg_trans['state'].unique())
selected_state = st.sidebar.selectbox("Select State", ["All"] + list(states))

# Apply filters
def apply_filters(df):
    filtered = df.copy()
    if selected_year != "All":
        filtered = filtered[filtered['year'] == selected_year]
    if selected_quarter != "All":
        filtered = filtered[filtered['quarter'] == selected_quarter]
    if selected_state != "All" and 'state' in filtered.columns:
        filtered = filtered[filtered['state'] == selected_state]
    return filtered

filtered_trans = apply_filters(agg_trans)
filtered_user  = apply_filters(agg_user)
filtered_ins   = apply_filters(agg_ins)

# ─────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview",
     "💳 Transactions",
     "👥 Users",
     "🛡️ Insurance",
     "🏆 Top Performers"]
)

# ═════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("📱 PhonePe Transaction Insights Dashboard")
    st.markdown("**Interactive analysis of PhonePe's digital payment data across India (2018-2024)**")
    st.markdown("---")

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)

    total_amount = filtered_trans['transaction_amount'].sum() / 1e7
    total_count  = filtered_trans['transaction_count'].sum() / 1e7
    total_users  = filtered_user['registered_users'].sum() / 1e7
    total_states = filtered_trans['state'].nunique()

    col1.metric("💰 Total Amount (Cr)", f"₹{total_amount:,.0f}")
    col2.metric("🔢 Total Transactions (Cr)", f"{total_count:,.2f}")
    col3.metric("👥 Registered Users (Cr)", f"{total_users:,.2f}")
    col4.metric("🗺️ States Covered", f"{total_states}")

    st.markdown("---")

    # Two charts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transaction Type Distribution")
        tx_type = filtered_trans.groupby('transaction_type')['transaction_count'].sum().reset_index()
        fig = px.pie(
            tx_type, names='transaction_type', values='transaction_count',
            color_discrete_sequence=px.colors.qualitative.Set3, hole=0.3
        )
        fig.update_layout(margin=dict(t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Quarterly Transaction Trend")
        quarterly = filtered_trans.groupby(['year', 'quarter'])['transaction_count'].sum().reset_index()
        quarterly['year_quarter'] = quarterly['year'].astype(str) + ' Q' + quarterly['quarter'].astype(str)
        quarterly = quarterly.sort_values(['year', 'quarter'])
        fig = px.line(
            quarterly, x='year_quarter', y='transaction_count',
            markers=True, color_discrete_sequence=['#5f259f']
        )
        fig.update_layout(margin=dict(t=0, b=0), xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    # Year wise growth
    st.subheader("Year-wise Transaction Growth")
    yearly = filtered_trans.groupby('year').agg(
        total_count=('transaction_count', 'sum'),
        total_amount=('transaction_amount', 'sum')
    ).reset_index()
    yearly['amount_cr'] = yearly['total_amount'] / 1e7
    yearly['count_cr']  = yearly['total_count'] / 1e7

    fig = go.Figure()
    fig.add_trace(go.Bar(x=yearly['year'], y=yearly['count_cr'],
                         name='Transaction Count (Cr)', marker_color='#5f259f'))
    fig.add_trace(go.Bar(x=yearly['year'], y=yearly['amount_cr'],
                         name='Transaction Amount (Cr)', marker_color='#f7c84e'))
    fig.update_layout(barmode='group', xaxis_title='Year', yaxis_title='Value (Crores)')
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════
# PAGE 2 — TRANSACTIONS
# ═════════════════════════════════════════════
elif page == "💳 Transactions":
    st.title("💳 Transaction Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 States by Transaction Amount")
        top_states = filtered_trans.groupby('state')['transaction_amount'].sum().reset_index()
        top_states = top_states.sort_values('transaction_amount', ascending=False).head(10)
        top_states['amount_cr'] = top_states['transaction_amount'] / 1e7
        fig = px.bar(
            top_states, x='amount_cr', y='state', orientation='h',
            color='amount_cr', color_continuous_scale='Purples',
            labels={'amount_cr': 'Amount (Cr)', 'state': 'State'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, margin=dict(t=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Transaction Amount by Type")
        tx_amount = filtered_trans.groupby('transaction_type')['transaction_amount'].sum().reset_index()
        tx_amount['amount_cr'] = tx_amount['transaction_amount'] / 1e7
        fig = px.bar(
            tx_amount, x='transaction_type', y='amount_cr',
            color='transaction_type',
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'amount_cr': 'Amount (Cr)', 'transaction_type': 'Type'}
        )
        fig.update_layout(margin=dict(t=0), xaxis_tickangle=30, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("State-wise Transaction Heatmap")
    state_year = filtered_trans.groupby(['state', 'year'])['transaction_amount'].sum().reset_index()
    state_pivot = state_year.pivot(index='state', columns='year', values='transaction_amount').fillna(0)
    top15 = filtered_trans.groupby('state')['transaction_amount'].sum().nlargest(15).index
    state_pivot_top = state_pivot[state_pivot.index.isin(top15)]

    fig = px.imshow(
        state_pivot_top / 1e7,
        color_continuous_scale='Purples',
        labels=dict(color="Amount (Cr)"),
        aspect='auto'
    )
    fig.update_layout(margin=dict(t=0))
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════
# PAGE 3 — USERS
# ═════════════════════════════════════════════
elif page == "👥 Users":
    st.title("👥 User Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 States by Registered Users")
        top_users = filtered_user.groupby('state')['registered_users'].sum().reset_index()
        top_users = top_users.sort_values('registered_users', ascending=False).head(10)
        top_users['users_cr'] = top_users['registered_users'] / 1e7
        fig = px.bar(
            top_users, x='state', y='users_cr',
            color='users_cr', color_continuous_scale='Teal',
            labels={'users_cr': 'Users (Cr)', 'state': 'State'}
        )
        fig.update_layout(margin=dict(t=0), xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top Mobile Brands")
        brand_data = filtered_user[filtered_user['brand'].notna() &
                                   (filtered_user['brand'] != 'Unknown')]
        brand_dist = brand_data.groupby('brand')['device_count'].sum().reset_index()
        brand_dist = brand_dist.sort_values('device_count', ascending=False).head(10)
        fig = px.bar(
            brand_dist, x='brand', y='device_count',
            color='device_count', color_continuous_scale='Oranges',
            labels={'device_count': 'Users', 'brand': 'Brand'}
        )
        fig.update_layout(margin=dict(t=0), xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("App Opens vs Registered Users by State")
    user_state = filtered_user.groupby('state').agg(
        total_registered=('registered_users', 'sum'),
        total_app_opens=('app_opens', 'sum')
    ).reset_index()
    user_state['engagement_ratio'] = (
        user_state['total_app_opens'] / user_state['total_registered'].replace(0, 1)
    )
    fig = px.scatter(
        user_state, x='total_registered', y='total_app_opens',
        text='state', color='engagement_ratio', size='engagement_ratio',
        color_continuous_scale='RdYlGn',
        labels={'total_registered': 'Registered Users',
                'total_app_opens': 'App Opens',
                'engagement_ratio': 'Engagement Ratio'}
    )
    fig.update_traces(textposition='top center', textfont_size=8)
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════
# PAGE 4 — INSURANCE
# ═════════════════════════════════════════════
elif page == "🛡️ Insurance":
    st.title("🛡️ Insurance Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 States by Insurance Amount")
        ins_state = filtered_ins.groupby('state')['transaction_amount'].sum().reset_index()
        ins_state = ins_state.sort_values('transaction_amount', ascending=False).head(10)
        ins_state['amount_cr'] = ins_state['transaction_amount'] / 1e7
        fig = px.bar(
            ins_state, x='state', y='amount_cr',
            color='amount_cr', color_continuous_scale='Purples',
            labels={'amount_cr': 'Amount (Cr)', 'state': 'State'}
        )
        fig.update_layout(margin=dict(t=0), xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Insurance Transaction Trend")
        ins_trend = filtered_ins.groupby(['year', 'quarter'])['transaction_count'].sum().reset_index()
        ins_trend['year_quarter'] = ins_trend['year'].astype(str) + ' Q' + ins_trend['quarter'].astype(str)
        ins_trend = ins_trend.sort_values(['year', 'quarter'])
        fig = px.line(
            ins_trend, x='year_quarter', y='transaction_count',
            markers=True, color_discrete_sequence=['#5f259f'],
            labels={'transaction_count': 'Count', 'year_quarter': 'Quarter'}
        )
        fig.update_layout(margin=dict(t=0), xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Insurance Amount Distribution by State (All Years)")
    ins_all = agg_ins.groupby('state')['transaction_amount'].sum().reset_index()
    ins_all['amount_cr'] = ins_all['transaction_amount'] / 1e7
    ins_all = ins_all.sort_values('amount_cr', ascending=False)
    fig = px.bar(
        ins_all, x='state', y='amount_cr',
        color='amount_cr', color_continuous_scale='Blues',
        labels={'amount_cr': 'Amount (Cr)', 'state': 'State'}
    )
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════
# PAGE 5 — TOP PERFORMERS
# ═════════════════════════════════════════════
elif page == "🏆 Top Performers":
    st.title("🏆 Top Performers")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Districts by Transaction Amount")
        top_dist = top_trans[top_trans['entity_type'] == 'district']
        top_dist = top_dist.groupby('entity_name')['transaction_amount'].sum().reset_index()
        top_dist = top_dist.sort_values('transaction_amount', ascending=False).head(10)
        top_dist['amount_cr'] = top_dist['transaction_amount'] / 1e7
        fig = px.bar(
            top_dist, x='amount_cr', y='entity_name', orientation='h',
            color='amount_cr', color_continuous_scale='Teal',
            labels={'amount_cr': 'Amount (Cr)', 'entity_name': 'District'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, margin=dict(t=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 10 Districts by Registered Users")
        top_dist_user = top_user[top_user['entity_type'] == 'district']
        top_dist_user = top_dist_user.groupby('entity_name')['registered_users'].sum().reset_index()
        top_dist_user = top_dist_user.sort_values('registered_users', ascending=False).head(10)
        fig = px.bar(
            top_dist_user, x='registered_users', y='entity_name', orientation='h',
            color='registered_users', color_continuous_scale='Oranges',
            labels={'registered_users': 'Users', 'entity_name': 'District'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, margin=dict(t=0))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Pincodes by Transaction Amount")
    top_pin = top_trans[top_trans['entity_type'] == 'pincode']
    top_pin = top_pin.groupby('entity_name')['transaction_amount'].sum().reset_index()
    top_pin = top_pin.sort_values('transaction_amount', ascending=False).head(10)
    top_pin['amount_cr'] = top_pin['transaction_amount'] / 1e7
    fig = px.bar(
        top_pin, x='entity_name', y='amount_cr',
        color='amount_cr', color_continuous_scale='Purples',
        labels={'amount_cr': 'Amount (Cr)', 'entity_name': 'Pincode'}
    )
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    # Raw data viewer
    st.markdown("---")
    st.subheader("📋 Raw Data Viewer")
    table_choice = st.selectbox("Select Table to View", [
        "aggregated_transaction", "aggregated_user", "aggregated_insurance",
        "map_transaction", "map_user", "top_transaction", "top_user"
    ])
    table_map = {
        "aggregated_transaction": agg_trans,
        "aggregated_user": agg_user,
        "aggregated_insurance": agg_ins,
        "map_transaction": map_trans,
        "map_user": map_user,
        "top_transaction": top_trans,
        "top_user": top_user
    }
    st.dataframe(table_map[table_choice].head(100), use_container_width=True)