# Following graphs are created to visualize the BigMart Sales data

import pandas as pd
import matplotlib.pyplot as plt


# Load Data

file_path = "BigMartSalesData.csv"   
df = pd.read_csv(file_path)

# Ensure Year is integer
df['Year'] = df['Year'].astype(int)


# Filter for Year 2011

df_2011 = df[df['Year'] == 2011]


# 1. Total Sales Per Month (Line Plot)

monthly_sales = df_2011.groupby('Month')['Amount'].sum()

plt.figure(figsize=(10,6))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linestyle='-', color='b')
plt.title("Total Sales Per Month (2011)", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Sales", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

print(f"Lowest Sales Month: {monthly_sales.idxmin()}")


# 2. Total Sales Per Month (Bar Chart)

plt.figure(figsize=(10,6))
bars = plt.bar(monthly_sales.index, monthly_sales.values, color='skyblue', edgecolor='black')

# Enhancement: Show values on bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01*yval, f"{int(yval)}",
             ha='center', va='bottom', fontsize=9)

plt.title("Total Sales Per Month (2011) - Bar Chart", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Sales", fontsize=12)
plt.show()


# 3. Pie Chart Country Wise

country_sales = df_2011.groupby('Country')['Amount'].sum()

plt.figure(figsize=(8,8))
plt.pie(country_sales.values, labels=country_sales.index, autopct='%1.1f%%',
        shadow=True, startangle=90)  # Enhancements
plt.title("Country-wise Sales Contribution (2011)", fontsize=14)
plt.show()

print(f"Top Country by Sales: {country_sales.idxmax()}")


# 4. Scatter Plot of Invoice Amounts

invoice_amounts = df_2011.groupby('InvoiceNo')['Amount'].sum()

plt.figure(figsize=(10,6))
plt.scatter(invoice_amounts.index, invoice_amounts.values, alpha=0.5, color='green') # Enhancement: custom color
plt.title("Scatter Plot of Invoice Amounts (2011)", fontsize=14)
plt.xlabel("Invoice Number", fontsize=12)
plt.ylabel("Invoice Amount", fontsize=12)
plt.show()

print("\nInvoice Amount Concentration:")
print(invoice_amounts.describe())