import pandas as pd

# Load FAQ data
faq_file = 'data/faq_data.csv'
data = pd.read_csv(faq_file)

# Remove duplicates
data = data.drop_duplicates()

# Strip leading and trailing spaces
data['question'] = data['question'].str.strip()
data['answer'] = data['answer'].str.strip()

# Save cleaned CSV
data.to_csv(faq_file, index=False)

print("FAQ data cleaned successfully!")
