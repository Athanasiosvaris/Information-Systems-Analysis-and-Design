import pandas as pd

# Read the CSV file into a pandas DataFrame
#df = pd.read_csv('data_4GB.csv', header=None)

# Rename the columns for clarity
#df.columns = ['A', 'B', 'C', 'D']

# Reshape the DataFrame by stacking the columns
#stacked = df.stack().reset_index(level=1, drop=True)

# Create a new DataFrame with two columns (X, Y)
#new_df = pd.DataFrame({'X': stacked[::2].values, 'Y': stacked[1::2].values})

# Save the new DataFrame to a new CSV file
#new_df.to_csv('new_file_4GB.csv', index=False)

#print("New file saved successfully.")

# Define chunk size based on available memory
chunk_size = 1000000  # Adjust as needed based on your system's memory capacity

# Initialize an empty DataFrame to store the result
result_df = pd.DataFrame(columns=['X', 'Y'])

# Read the CSV file in chunks
for chunk in pd.read_csv('data.csv', header=None, chunksize=chunk_size):
    # Reshape the chunk by stacking the columns
    stacked = chunk.stack().reset_index(level=1, drop=True)

    # Create a DataFrame with two columns (X, Y) from stacked data
    chunk_df = pd.DataFrame({'X': stacked[::2].values, 'Y': stacked[1::2].values})

    # Append the chunk DataFrame to the result DataFrame
    result_df = pd.concat([result_df, chunk_df], ignore_index=True)

# Save the result DataFrame to a new CSV file
result_df.to_csv('new_data.csv', index=False)

print("New file saved successfully.")