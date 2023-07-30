import os
from dotenv import load_dotenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

load_dotenv()


class GoogleDriveController:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.drive = self.authorize_google_drive()
        self.db_file_id = None

    def authorize_google_drive(self):
        self.gauth.LoadCredentialsFile(os.getenv("CREDENTIALS_PATH"))

        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()

        self.gauth.SaveCredentialsFile(os.getenv("CREDENTIALS_PATH"))
        self.gauth.Authorize()
        return GoogleDrive(self.gauth)

    def download_db(self):
        self.db_file_id = self.get_file_id(os.getenv("DB_FOLDER_ID"), os.getenv("DB_NAME"))
        self.drive.CreateFile({'id': self.db_file_id }).GetContentFile(os.getenv("DB_NAME"))

    def get_file_id(self, folder_id: str, filename: str):
        return self.drive.ListFile({'q': f"'{folder_id}' in parents and title ='{filename}'"}).GetList()[0]['id']

    def upload_db(self):
        upload_file = self.drive.CreateFile({"id": self.db_file_id})
        upload_file.SetContentFile(os.getenv("DB_NAME"))
        upload_file.Upload({'convert': True})



