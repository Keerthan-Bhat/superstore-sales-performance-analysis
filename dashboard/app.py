import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Superstore Sales Performance Dashboard",
    layout="wide"
)

# -------------------------------
# Load data (IMPORTANT: encoding)
# -------------------------------
df = pd.read_csv("superstore.csv", encoding="latin1")

# Clean columns
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Convert dates
df["order_date"] = pd.to_datetime(df["order_date"])

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

# Region filter
regions = ["All"] + sorted(df["region"].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Category filter
categories = ["All"] + sorted(df["category"].unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Date range filter
min_date = df["order_date"].min()
max_date = df["order_date"].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# -------------------------------
# Apply filters
# -------------------------------
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

filtered_df = filtered_df[
    (filtered_df["order_date"] >= pd.to_datetime(start_date)) &
    (filtered_df["order_date"] <= pd.to_datetime(end_date))
]

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 Superstore Sales Performance Dashboard")

# -------------------------------
# KPIs
# -------------------------------
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Total Profit", f"${total_profit:,.0f}")
c3.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# -------------------------------
# Sales by Region
# -------------------------------
region_sales = (
    filtered_df.groupby("region")["sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    region_sales,
    x="region",
    y="sales",
    title="Sales by Region"
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# Category-wise Sales & Profit
# -------------------------------
category_perf = (
    filtered_df.groupby("category")[["sales", "profit"]]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    category_perf,
    x="category",
    y=["sales", "profit"],
    barmode="group",
    title="Category-wise Sales & Profit"
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Monthly Sales Trend
# -------------------------------
filtered_df["month"] = filtered_df["order_date"].dt.to_period("M").astype(str)
monthly_sales = (
    filtered_df.groupby("month")["sales"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x="month",
    y="sales",
    markers=True,
    title="Monthly Sales Trend"
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ======================================================
# 🔥 OPTION 2: DISCOUNT vs PROFIT ANALYSIS
# ======================================================
st.subheader("📉 Discount vs Profit Analysis")

fig4 = px.scatter(
    filtered_df,
    x="discount",
    y="profit",
    color="category",
    title="Discount vs Profit",
    hover_data=["product_name", "sales"]
)
st.plotly_chart(fig4, use_container_width=True)

st.info(
    "📌 Insight: Higher discounts often lead to lower or negative profit. "
    "This helps identify over-discounted products."
)

st.divider()

# ======================================================
# 🔥 OPTION 3: TOP / BOTTOM PRODUCTS
# ======================================================
st.subheader("🏆 Top & Bottom Products by Profit")

col1, col2 = st.columns(2)

# Top 10 profitable products
top_products = (
    filtered_df.groupby("product_name")["profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

col1.markdown("### ✅ Top 10 Profitable Products")
col1.dataframe(top_products, use_container_width=True)

# Top 10 loss-making products
loss_products = (
    filtered_df.groupby("product_name")["profit"]
    .sum()
    .sort_values()
    .head(10)
    .reset_index()
)

col2.markdown("### ❌ Top 10 Loss-Making Products")
col2.dataframe(loss_products, use_container_width=True)
