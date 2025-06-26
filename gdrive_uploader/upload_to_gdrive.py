from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime

def upload_to_drive(output_path):
    # Authenticate using service account
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("creds/service_account.json", scope)
    drive = GoogleDrive(gauth)

    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID", "1Ta4nURyHfJzu7qXM5__K3UBL2mgjo9Xm")

    filename = os.path.basename(output_path)
    file_drive = drive.CreateFile({'title': filename, 'parents': [{"id": folder_id}]})
    file_drive.SetContentFile(output_path)
    file_drive.Upload()

    print(f"[✔] Uploaded '{filename}' to Google Drive")
