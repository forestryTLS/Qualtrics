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
    
    # This row is useless information, drop it
    df = df.drop(1)

    # Convert to number
    df['Score-sum'] = pd.to_numeric(df['Score-sum'], errors='coerce')
    df['Claim balance'] = pd.to_numeric(df['Claim balance'], errors='coerce')

    # Amount of grant to give them is the minimum of their current grant balance with the cost of their courses
    df.insert(loc=13, column='Grant amount to give', value=np.minimum(df['Claim balance'], df['Score-sum']))
    cols = ['Birthday#1_1', 'Birthday#2_1', 'Birthday#3_1']

    df.insert(loc=14, column='Birthday', value=df_original[cols].apply(lambda row: '-'.join(row.dropna().values.astype(str)), axis=1))

    new_order = [
        'ResponseID', 'Q25', 'Full Name', 'Email', 'Gender', 'SIN', 'PEN',
        'StartDate', 'EndDate', 'Finished', 'Not Eligble', 'Score-sum',
        'Claim balance', 'Grant amount to give', 'Birthday',
        'Signature_FILE_ID', 'Address_1_TEXT', 'Address_2_TEXT',
        'Address_3_TEXT', 'Address_4_TEXT', 'Eligibility Check_1',
        'Eligibility Check_2', 'Eligibility Check_3', 'Eligibility Check_4',
        'Eligibility Check_5', 'Eligibility Check_6', 'Eligibility Check_7',
        'Eligibility Check_8', 'Eligibility Check_9', 'Eligibility Check_10',
        'Eligibility Check_11', 'Select Programs_5', 'Select Programs_7',
        'Select Programs_6', 'Select Programs_8', 'Select Programs_9',
        'Select Programs_10', 'Select Programs_11', 'Select Programs_12',
        'Select Programs_14', 'Select Programs_15', 'CACE_1', 'CACE_2',
        'CACE_3', 'CACE_4', 'CBBD_1', 'CBBD_2', 'CBBD_3', 'CBBD_4', 'CBBD_5',
        'CVA_1', 'CVA_2', 'CVA_3', 'CVA_4', 'CVA_5', 'CVA Elective', 'CMNR_1', 'CMNR_2',
        'CMNR_3', 'CMNR_4', 'CSRP_1', 'CSRP_2', 'CSRP_3', 'CSRP_4', 'CSRP_5',
        'EFO_1', 'EFO_2', 'EFO_3', 'EFO_4', 'FSTB_1', 'FSTB_2', 'FSTB_3',
        'FSTB_4', 'FSTB_5', 'FCM_1', 'FCM_2', 'FCM_3', 'FCM_4', 'FCM_5',
        'FHM_1', 'FHM_2', 'FHM_3', 'FHM_4', 'FHM_5', 'TWS_1', 'TWS_2',
        'TWS_3', 'TWS_4', 'TWS_5'
    ]

    df = df[new_order]

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
    
    # Update the 'Processed' column based on the 'PEN' column if 'Processed' is empty
    df_final['Processed'] = np.where((df_final['PEN'] == '900000000') & (df_final['Processed'].isnull()), 'NO PEN', df_final['Processed'])

    duplicate_emails = df_final.duplicated(subset='Email', keep=False)
    df_final.loc[duplicate_emails & df_final['Not Eligble'].isnull(), 'Not Eligble'] = 'Duplicate Email'

    df_final.to_excel(output_file_name, index=False)
    date_file_name = add_date_to_filename(output_file_name)
    print(f"ALSO SAVING TO {date_file_name} PLEASE MAKE SURE THE DATA IS SYNCED CORRECTLY")
    df_final.to_excel(date_file_name, index=False)
