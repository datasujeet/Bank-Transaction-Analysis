# List of CSV files and their corresponding table names
csv_files = [
    ('bank transaction_data.csv', 'transaction') 
]

# Connect to the SQL database
engine = create_engine("postgresql://postgres:pwd@localhost:5432/bank_transaction")

# Folder containing the CSV files
folder_path = 'file destination link'

# Auto-scan all CSV files in the folder
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        table_name = os.path.splitext(file)[0].lower()  # Use filename (lowercase) as table name
        file_path = os.path.join(folder_path, file)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Clean column names
        df.columns = [col.strip().replace(' ', '_').replace('-', '_').replace('.', '_') for col in df.columns]

        # Handle missing values
        df = df.where(pd.notnull(df), None)

        # Write DataFrame to PostgreSQL
        df.to_sql(table_name, engine, index=False, if_exists='replace')  # 'replace' will drop+create

        print(f"✔ Imported {file} as table '{table_name}'")

print("✅ All files imported successfully!")

