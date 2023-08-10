import pandas as pd
import numpy as np
import os
from datetime import datetime

def add_date_to_filename(filename):
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Split the filename into name and extension
    name, extension = os.path.splitext(filename)

    # Return the filename with date appended
    return f"{name}_{date_str}{extension}"


def process_file(csv_path, output_file_name):
    df_original = pd.read_csv(csv_path)
    df = pd.read_csv(csv_path)
    
    # These are the columns to keep in this new order
    index_ordered = [0, 14, 15, 16, 17, 25, 26, 3, 4, 9, 95, 11, 97, 98, 21, 22, 23, 24] + list(range(27, 94))
    df = df[df.columns[index_ordered]]
    # Remove the row with ImportId
    df = df.drop(1)

    # Convert to number
    df.iloc[:, 11] = pd.to_numeric(df.iloc[:, 11], errors='coerce')
    df.iloc[:, 12] = pd.to_numeric(df.iloc[:, 12], errors='coerce')
    
    # Amount of grant to give them is the minimum of their current grant balance with the cost of their courses
    df.insert(loc=13, column='Grant amount to give', value=np.minimum(df.iloc[:, 12], df.iloc[:, 11]))
    cols = ['Birthday#1_1', 'Birthday#2_1', 'Birthday#3_1']
    df.insert(loc=14, column='Birthday', value=df_original[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1))
    
    df.reset_index(drop=True, inplace=True)  # Reset the index
    
    if os.path.exists(output_file_name):
        df_existing = pd.read_excel(output_file_name)
        

        df_final = pd.concat([df_existing, df])
        

        df_final.drop_duplicates(subset='ResponseID', keep='first', inplace=True)

        if 'Processed' not in df_final.columns:
            df_final.insert(loc=14, column='Processed', value='')

    else:
        df_final = df
        
        df_final.insert(loc=14, column='Processed', value='')

    df_final.to_excel(output_file_name, index=False)
    date_file_name = add_date_to_filename(output_file_name)
    print(f"ALSO SAVING TO {date_file_name} PLEASE MAKE SURE THE DATA IS SYNCED CORRECTLY")
    df_final.to_excel(date_file_name, index=False)
