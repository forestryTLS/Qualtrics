import requests
import zipfile
import io
import os
from datetime import datetime
from dotenv import load_dotenv
import process_data

load_dotenv()

# Code based: https://gist.github.com/FedericoTartarini/9496282b4b2f508c0ab2da96f4955397
def get_qualtrics_survey(dir_save_survey, survey_id):
    # Setting user Parameters
    api_token = os.environ.get("API_TOKEN")
    file_format = "csv"
    data_center = os.environ.get("DATA_CENTER")
    # Setting static parameters
    request_check_progress = 0
    progress_status = "in progress"
    base_url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
    headers = {
        "content-type": "application/json",
        "x-api-token": api_token,
    }

    # Step 1: Creating Data Export
    download_request_url = base_url
    download_request_payload = '{"format":"' + file_format + '","surveyId":"' + survey_id + '"}'
    download_request_response = requests.request("POST", download_request_url, data=download_request_payload, headers=headers)
    if download_request_response.status_code != 200:
        exit(f"DOWNLOAD REQUEST RESPONSE STATUS IS NOT 200, EXITING {download_request_response}")

    progress_id = download_request_response.json()["result"]["id"]

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while request_check_progress < 100 and progress_status != "complete":
        request_check_url = base_url + progress_id
        request_check_response = requests.request("GET", request_check_url, headers=headers)
        if request_check_response.status_code != 200:
            exit(f"REQUEST CHECK RESPONSE STATUS IS NOT 200, EXITING {request_check_response}")
        request_check_progress = request_check_response.json()["result"]["percentComplete"]

    # Step 3: Downloading file
    request_download_url = base_url + progress_id + '/file'
    request_download = requests.request("GET", request_download_url, headers=headers, stream=True)
    if request_download.status_code != 200:
            exit(f"REQUEST DOWNLOAD RESPONSE STATUS IS NOT 200, EXITING {request_download}")

    # Extracting and renaming the files in the zipped file
    with zipfile.ZipFile(io.BytesIO(request_download.content)) as zipped_file:
        for file_info in zipped_file.infolist():
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            new_file_name = file_info.filename.rsplit('.', 1)[0] + '_' + current_time + '.' + file_info.filename.rsplit('.', 1)[1]
            zipped_file.extract(file_info, dir_save_survey)
            new_path = os.path.join(dir_save_survey, new_file_name)
            os.rename(os.path.join(dir_save_survey, file_info.filename), new_path)
            print('Downloaded qualtrics survey to path', new_path)
            return new_path

if __name__ == "__main__":
    path = os.path.abspath(os.getcwd()) + "/Surveys" # Surveys directory
    new_file_path = get_qualtrics_survey(dir_save_survey = path, survey_id = os.environ.get("SURVEY_ID"))
    # Process data
    process_data.process_file(new_file_path, os.environ.get("OUTPUT_FILE_NAME"))
