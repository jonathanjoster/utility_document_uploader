import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dateutil.relativedelta import relativedelta
import argparse
import json
import os

def upload_to_google_drive(file_path: str, new_filename: str, type: str) -> None:
    """upload the document to the drive
    Args:
        file_path (str): file path to be uploaded
        new_filename (str): new filename on the drive
    """
    # Google authentication
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

    # upload destination setting
    drive = GoogleDrive(gauth)
    try:
        with open('directory_id.json') as f:
            _dir_id = json.load(f)[type]
    except:
        print('[Warning] directory_id file not found. The file will be uploaded to the root.')
        _dir_id = ''

    # upload the file
    file = drive.CreateFile({'title': new_filename, 'parents': [{'id': _dir_id}]})
    file.SetContentFile(os.path.abspath(file_path))
    file.Upload()
    print(f'[Success] {new_filename} was uploaded correctly. (File ID: {file["id"]})')
    print(f'To check the result, visit https://drive.google.com/drive/u/0/folders/{_dir_id}')

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(usage='python main.py [image path] [type]',
        description='upload the specified png to the drive')
    parser.add_argument('path', type=str, help='path to the document')
    parser.add_argument('type', type=str, help='what the bill for, water or gas')
    args = parser.parse_args()

    # name the file
    _today = datetime.date.today()
    if args.type == 'water':
        _2month_before = _today - relativedelta(months=2)
        upload_filename = f'水道料金_{_today.year}_{_2month_before.month}-{_today.month}.png'
    elif args.type == 'gas':
        upload_filename = f'ガス料金領収書_{_today.year}-{str(_today.month).zfill(2)}.png'
    else:
        raise KeyError(args.type)

    # upload
    upload_to_google_drive(args.path, new_filename=upload_filename, type=args.type)