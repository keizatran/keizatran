import gspread
from oauth2client.service_account import ServiceAccountCredentials

def gsheet_open(file_id, worksheet_name, service_account_file):
    """
    Function to load df to a worksheet file
    """
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, scope)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(file_id)
    ws = sheet.worksheet(worksheet_name)

    return ws