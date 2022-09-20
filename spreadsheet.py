import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
CREDENTIALS = {
    "type": "service_account",
    "project_id": "secret-antonym-362720",
    "private_key_id": os.environ["PRIVATE_KEY_ID"],
    "private_key": os.environ["PRIVATE_KEY"],
    "client_email": os.environ["CLIENT_EMAIL"],
    "client_id": os.environ["CLIENT_ID"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ["CLIENT_X509_CERT_URL"]
}

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = os.environ('SPREAD_SHEETS_URL')
# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('Name')

column_data = worksheet.col_values(1)
print(column_data)


