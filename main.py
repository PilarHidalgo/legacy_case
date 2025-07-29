# ❌ LEGACY CODE - main.py
"""
Legacy sales data analyzer - monolithic implementation
This code has multiple issues and needs refactoring
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

def analyze_sales_data(file_path, region, start_date, end_date, product_type):
    """
    Analyze sales data from CSV file
    WARNING: This function does too many things and is hard to maintain
    """
    
    # Read data - poor error handling
    try:
        df = pd.read_csv(file_path)
    except:
        return "Error reading file"
    
    # Clean data - basic cleaning only
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])
    df['revenue'] = df['price'] * df['quantity']
    
    # Filter by region - repetitive code
    if region == "north":
        df = df[df['region'] == 'North']
    elif region == "south":
        df = df[df['region'] == 'South']
    elif region == "east":
        df = df[df['region'] == 'East']
    elif region == "west":
        df = df[df['region'] == 'West']
    elif region == "all":
        pass  # No filtering
    else:
        return "Invalid region specified"
    
    # Filter by date range - no validation
    if start_date and end_date:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        df = df[(df['date'] >= start) & (df['date'] <= end)]
    
    # Filter by product type - hardcoded values
    if product_type != "all":
        df = df[df['product_type'] == product_type]
    
    # Check if data is empty after filtering
    if df.empty:
        return "No data found matching criteria"
    
    # Calculate basic metrics - no error handling
    total_revenue = df['revenue'].sum()
    avg_revenue = df['revenue'].mean()
    total_units = df['quantity'].sum()
    avg_units = df['quantity'].mean()
    
    # Monthly analysis - inefficient loop
    monthly_data = {}
    for month in range(1, 13):
        month_df = df[df['date'].dt.month == month]
        if len(month_df) > 0:
            monthly_data[month] = {
                'revenue': month_df['revenue'].sum(),
                'units': month_df['quantity'].sum(),
                'avg_price': month_df['price'].mean(),
                'transactions': len(month_df)
            }
    
    # Top products analysis - basic implementation
    top_products = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(5)
    
    # Trend analysis - naive implementation
    trend_data = []
    df_sorted = df.sort_values('date')
    for i in range(1, len(df_sorted)):
        prev_revenue = df_sorted.iloc[i-1]['revenue']
        curr_revenue = df_sorted.iloc[i]['revenue']
        if curr_revenue > prev_revenue:
            trend = "increasing"
        elif curr_revenue < prev_revenue:
            trend = "decreasing"
        else:
            trend = "stable"
        trend_data.append(trend)
    
    # Calculate trend percentages - no error handling
    if trend_data:
        increasing_pct = (trend_data.count("increasing") / len(trend_data)) * 100
        decreasing_pct = (trend_data.count("decreasing") / len(trend_data)) * 100
        stable_pct = (trend_data.count("stable") / len(trend_data)) * 100
    else:
        increasing_pct = decreasing_pct = stable_pct = 0
    
    # Generate report - hardcoded format
    report = f"""
    ========================================
    SALES ANALYSIS REPORT
    ========================================
    Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Data Period: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}
    
    SUMMARY METRICS:
    ----------------
    Total Revenue: ${total_revenue:,.2f}
    Average Revenue per Transaction: ${avg_revenue:,.2f}
    Total Units Sold: {total_units:,}
    Average Units per Transaction: {avg_units:.2f}
    Total Transactions: {len(df):,}
    
    TOP 5 PRODUCTS BY REVENUE:
    --------------------------
    """
    
    # Add top products to report
    for i, (product, revenue) in enumerate(top_products.items(), 1):
        report += f"{i}. {product}: ${revenue:,.2f}\n    "
    
    # Add monthly breakdown
    report += "\n\n    MONTHLY BREAKDOWN:\n    ------------------\n    "
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for month, data in monthly_data.items():
        month_name = month_names[month - 1]
        report += f"{month_name}: Revenue=${data['revenue']:,.2f}, Units={data['units']:,}, Transactions={data['transactions']}\n    "
    
    # Add trend analysis
    report += f"""
    
    TREND ANALYSIS:
    ---------------
    Increasing Trends: {increasing_pct:.1f}%
    Decreasing Trends: {decreasing_pct:.1f}%
    Stable Trends: {stable_pct:.1f}%
    
    ========================================
    """
    
    return report

# Main execution - no proper CLI interface
if __name__ == "__main__":
    # Hardcoded parameters for testing
    file_path = "sales_data.csv"
    region = "all"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    product_type = "all"
    
    # Run analysis
    result = analyze_sales_data(file_path, region, start_date, end_date, product_type)
    print(result)
    
    # Save to file - basic implementation
    with open("sales_report.txt", "w") as f:
        f.write(result)
    
    print("Report saved to sales_report.txt")