# Qualtrics

This extracts and processes data for Stronger BC Eligibility Survey

## Setup
Run `git clone https://github.com/WillKang01/Qualtrics.git`

Inside the new folder install a virtual environment. For example `python3 -m venv env`

Activate the virtual environment such as `source env/bin/activate`

Run `pip install -r requirements.txt`

## Environment Variables
Go to your account settings in Qualtrics and inside Qualtrics IDs copy your API token and the Survey ID
into a new .env file using .env.example

For `OUTPUT_FILE_NAME=processed_data.xlsx`, change this to the path of where the UBC shared folder is, such as:
`OUTPUT_FILE_NAME=<path>/UBC/Forestry TLS Team - Micro Certificate programs - StrongerBC Grant Eligibility Data/processed_data.xlsx`

![image](https://github.com/WillKang01/Qualtrics/assets/122059045/94940668-8282-4261-a1ee-f995772b5c26)

## Run program
Run with `python import_data.py`
By default the file generated will be processed_data.xlsx, this can be changed in the environment variables.
Manually changed data in processed_data.xlsx will **not** be overwritten.

Ignore this - RuntimeWarning: invalid value encountered in minimum
  result = getattr(ufunc, method)(*inputs, **kwargs)
