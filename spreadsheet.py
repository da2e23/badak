# import gspread
# import os
# from oauth2client.service_account import ServiceAccountCredentials
# scope = [
# 'https://spreadsheets.google.com/feeds',
# 'https://www.googleapis.com/auth/drive',
# ]
# CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS, scope)
# gc = gspread.authorize(credentials)
# spreadsheet_url = os.environ.get("SPREAD_SHEETS_URL")
# # 스프레스시트 문서 가져오기 
# doc = gc.open_by_url(spreadsheet_url)
# # 시트 선택하기
# worksheet = doc.worksheet('Name')

# column_data = worksheet.col_values(1)
# print(column_data)


