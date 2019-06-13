import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('googlesheet.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Tsuki").sheet1
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
