import pandas as pd
import numpy as np

# Load the Excel sheets into DataFrames
sheet1 = pd.read_excel('processed_data.xlsx')
sheet2 = pd.read_excel('processed_data_incorrect.xlsx')

# Ensure the "Processed" column is of string type to handle potential data type differences
sheet1['Processed'] = sheet1['Processed'].astype(str)
sheet2['Processed'] = sheet2['Processed'].astype(str)

# Check if the DataFrames are equal
if sheet1.equals(sheet2):
    print("Both sheets are identical.")
else:
    # Iterate through each cell to find differences
    differences = []
    for col in sheet1.columns:
        for idx, (val1, val2) in enumerate(zip(sheet1[col], sheet2[col])):
            if val1 != val2 and not (pd.isna(val1) and pd.isna(val2)):
                differences.append((col, idx, val1, val2))

    # Print the differences
    if differences:
        print("Differences found:")
        for col, idx, val1, val2 in differences:
            print(f"Row {idx + 2}, Column '{col}': Sheet 1 value = '{val1}', Sheet 2 value = '{val2}'")
    else:
        print("No differences found.")
