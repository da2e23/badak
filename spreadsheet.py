import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = os.getenv('SPREAD_SHEETS_URL')
# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('Name')

column_data = worksheet.col_values(1)
print(column_data)


