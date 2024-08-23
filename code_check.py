import pandas as pd 

# df1 = pd.read_csv(r"C:\Users\Acer\Desktop\esework_user_solution\python_agent\csv_agent\data\catalog_Contract_PO_Data.csv")


# List suppliers and their associated spend amounts
suppliers_spend = df1.groupby('Supplier Name')['TotalCost'].sum().reset_index()

# Calculate total spend for each supplier
suppliers_spend = suppliers_spend.sort_values(by='TotalCost', ascending=False)

# Calculate total spend percentage
total_spend = suppliers_spend['TotalCost'].sum()
cutoff_percentage = 0.8
print("total_spend :",total_spend)

cumulative_spend = 0
main_suppliers = []
tail_suppliers = []

# Identify main suppliers and tail spend
for index, row in suppliers_spend.iterrows():
    if cumulative_spend / total_spend < cutoff_percentage and row['TotalCost'] < 100000:
        main_suppliers.append(row['Supplier Name'])
    else:
        tail_suppliers.append(row['Supplier Name'])
    cumulative_spend += row['TotalCost']
print(" \n Cumulative spend",cumulative_spend )
tail_spend = suppliers_spend[suppliers_spend['Supplier Name'].isin(tail_suppliers)]['TotalCost'].sum()

print(" \n tail_spend",tail_spend )