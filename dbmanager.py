import requests
import os
from dotenv import load_dotenv
import sqlite3
from gdrive import GoogleDriveController
load_dotenv()


class Database:
    def __init__(self):
        self.gdrive = GoogleDriveController()
        self.cur = None
        self.conn = None

    def __enter__(self):
        self.gdrive.download_db()
        self.conn = sqlite3.connect(os.getenv("DB_NAME"))
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.conn.close()
        self.gdrive.upload_db()
        os.remove(os.getenv("DB_NAME"))


if __name__=="__main__":
    with Database() as db:
        print(type(db))
        if os.path.exists(os.getenv("DB_NAME")):
            print("DB was found")
        else:
            print("DB was not found")



