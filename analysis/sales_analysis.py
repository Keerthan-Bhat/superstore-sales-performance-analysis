import pandas as pd
import matplotlib.pyplot as plt

# Load dataset (FIXED encoding)
df = pd.read_csv("../data/superstore.csv", encoding="latin1")

# Clean column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Convert date columns
df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])

# 1. Sales by Region
region_sales = df.groupby("region")["sales"].sum().sort_values(ascending=False)

# 2. Category Performance
category_perf = df.groupby("category")[["sales", "profit"]].sum()

# 3. Monthly Sales Trend
df["month"] = df["order_date"].dt.to_period("M")
monthly_sales = df.groupby("month")["sales"].sum()

# 4. Loss-making Products
loss_products = (
    df.groupby("product_name")["profit"]
    .sum()
    .sort_values()
    .head(10)
)

print("Sales by Region:")
print(region_sales)

print("\nCategory Performance:")
print(category_perf)

print("\nTop Loss-Making Products:")
print(loss_products)

# Visualizations
region_sales.plot(kind="bar", title="Sales by Region")
plt.show()

monthly_sales.plot(marker="o", title="Monthly Sales Trend")
plt.show()

