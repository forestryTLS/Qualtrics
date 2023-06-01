import pandas as pd
import numpy as np
import os

def process_file(csv_path, output_file_name):
    df = pd.read_csv(csv_path)
    
    # These are the columns to keep in this new order
    index_ordered = [0, 14, 15, 16, 17, 3, 4, 9, 86, 11, 88, 89] + list(range(18, 86))
    df = df[df.columns[index_ordered]]
    # Remove the row with ImportId
    df = df.drop(1)

    # Convert to number
    df.iloc[:, 10] = pd.to_numeric(df.iloc[:, 10], errors='coerce')
    df.iloc[:, 9] = pd.to_numeric(df.iloc[:, 9], errors='coerce')
    
    # Current grant balance is 3500 - amount they claimed
    df.insert(loc=11, column='Current Grant balance', value=3500 - df.iloc[:, 10])
    # Amount of grant to give them is the minimum of their current grant balance with the cost of their courses
    df.insert(loc=12, column='Grant amount to give', value=np.minimum(df['Current Grant balance'], df.iloc[:, 9]))

    if os.path.exists(output_file_name):
        df_existing = pd.read_excel(output_file_name)

        df_final = pd.concat([df_existing, df])

        df_final.drop_duplicates(subset='ResponseID', keep='first', inplace=True)

        if 'Processed' not in df_final.columns:
            df_final.insert(loc=13, column='Processed', value='')

    else:
        df_final = df
        df_final.insert(loc=13, column='Processed', value='')

    df_final.to_excel(output_file_name, index=False)
