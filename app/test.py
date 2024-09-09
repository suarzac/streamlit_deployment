import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load CSV File
file_path = 'app/sources/Chase Activity Jan 1 to Aug 23.CSV'
df = pd.read_csv(file_path)

# Step 3: Inspect Data
print("First few rows of the DataFrame:")
print(df.head())

# Step 4: Data Cleaning (if necessary)
# Example: Fill missing values or convert data types
df.fillna(0, inplace=True)
df['Transaction Date'] = df['Transaction Date'].astype('datetime64[ns]')

# Step 5: Group Transactions
# Example: Group by 'Category' and calculate the sum of 'Amount'
grouped_df = df.groupby(['Category', 'Transaction Date'])['Amount'].sum().reset_index()

# Step 6: Analyze Data
# Example: Calculate total transactions and average amount per category
total_transactions = df['Amount'].sum()
average_amount_per_category = grouped_df['Amount'].mean()

# Step 7: Display Results
print("\nGrouped Transactions by Category:")
print(grouped_df)

print("\nTotal Transactions Amount: ", total_transactions)
print("Average Amount per Category: ", average_amount_per_category)

# Optional: Plot the results using matplotlib or seaborn

# plt.figure(figsize=(10, 6))
sns.catplot(kind='bar', data=grouped_df, x='Transaction Date', y='Amount', col='Category')
# sns.lineplot(x="Transaction Date", y="Amount",
#              hue="Category", style="Category",
#              data=grouped_df)
# sns.barplot(x='Category', y='Amount', data=grouped_df)
plt.title('Total Amount by Category')
plt.xlabel('Category')
plt.ylabel('Total Amount')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.show()