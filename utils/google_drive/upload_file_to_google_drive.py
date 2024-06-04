import os
import time
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.index import GOOGLE_DRIVE_CREDENTIALS_FILE
from services.slack.slack_message import send_detailed_slack_message
from utils.slack import send_slack_message


SCOPES = ['https://www.googleapis.com/auth/drive']

def remove_dublicate(file_path):
    stock = pd.read_csv(file_path, low_memory=False)
    stock.drop_duplicates(inplace=True)
    stock.to_csv(file_path, index=False)
    return stock


def upload_to_google_drive(file_path, max_trys=10, init=0):
    try:
        if (init < max_trys):
            print("UPLOADING FILE")
            time.sleep(0.1)
            remove_dublicate(file_path)
            
            creds_file = os.path.join(os.getcwd(), GOOGLE_DRIVE_CREDENTIALS_FILE)
            creds = service_account.Credentials.from_service_account_file(
                creds_file, scopes=SCOPES)

            service = build('drive', 'v3', credentials=creds)
            file_metadata = {'name': file_path}

            media = MediaFileUpload(file_path, mimetype='sheets/csv')
            file = service.files().create(body=file_metadata, supportsAllDrives=True,
                                          media_body=media,
                                          fields='id').execute()
            permission = {'type': 'anyone',
                          'value': 'anyone',
                          'role': 'reader'}
            service.permissions().create(
                fileId=file['id'], body=permission).execute()
            send_slack_message(f"c={file.get('id')}")
            return f"https://drive.google.com/open?id={file.get('id')}"
            
        else:
            send_detailed_slack_message("error occured in file uploading", "Max tries done")
            return
    except Exception as e:
        send_detailed_slack_message("EXCEPTION IN FILE UPLOADING: ", e)
        return upload_to_google_drive(file_path, max_trys, init=init+1)