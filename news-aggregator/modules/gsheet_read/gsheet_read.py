import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def gsheet_read(file_id, worksheet_name, service_account_file, range):
    """
    Function to load df to a worksheet file
    """
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, scope)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(file_id)
    ws = sheet.worksheet(worksheet_name)
    data = ws.get(range)
    df = pd.DataFrame(data)

    return df