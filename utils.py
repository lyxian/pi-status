### GOOGLE SHEETS API ###

# Required functions :
# - authorization

# Useful APIs :
# - retrieve all sheets > .worksheets()
# - get sheet records > .get_all_records()
# - update summary sheet
# - .

from oauth2client.service_account import ServiceAccountCredentials
from cryptography.fernet import Fernet
import gspread
import json
import os

### CONSTANTS ###
SHEET_COLUMNS = ['number', 'physical', 'hostname', 'address', 'last ping', 'status']
SHEET_NUM_ROWS = 20
SHEET_NUM_COLS = 60

def getDecrypted(secretKey):
    # check if secretKey exists
    key = bytes(os.getenv('KEY'), 'utf-8')
    if os.getenv(secretKey):
        encrypted = bytes(os.getenv(secretKey), 'utf-8')
    else:
        raise Exception(f'Secret:{secretKey} not found in env')
    # load as json or string
    try:
        return json.loads(Fernet(key).decrypt(encrypted))
    except ValueError:
        return Fernet(key).decrypt(encrypted).decode()
    except Exception as err:
        raise err

def spreadSheetClient(googleCredentials):
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        googleCredentials, scope)
    client = gspread.authorize(creds)
    return client

def openWorkbookByName(client, name):
    return client.open(name)

def newWorksheet(wb, name):
    if checkWorksheetExists(wb, name):
        print(f'returning existing worksheet - {name}')
        return next(filter(lambda x: x.title == name, wb.worksheets()))
    else:
        print(f'creating new worksheet - {name}')
        return wb.add_worksheet(name, rows=SHEET_NUM_ROWS, cols=SHEET_NUM_COLS)
    # last = len(wb.worksheets())
    # try:
    #     return wb.duplicate_sheet(source_sheet_id=wb.sheet1.id, insert_sheet_index=last, new_sheet_name=name)
    # except:
    #     sheet = [i for i in wb.worksheets() if i.title.lower()
    #              == name.lower()][0]
    #     if sheet.get_all_records() == []:
    #         wb.del_worksheet(sheet)
    #         return wb.duplicate_sheet(source_sheet_id=wb.sheet1.id, insert_sheet_index=last, new_sheet_name=name)
    #     else:
    #         return sheet

def getWorksheetTitles(wb):
    return [i.title for i in wb.worksheets()]

def checkWorksheetExists(wb, name):
    return name in getWorksheetTitles(wb)

def generatePayload(number, name, now):
    hostname, physical, address = name.split('_')
    return [
        SHEET_COLUMNS,
        [number, physical+'   ', hostname+'   ', address, now, 'ok']
    ]

def autoResizeColumn(wb, sheet):
    wb.batch_update({
        "requests": [{
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet._properties['sheetId'],
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": SHEET_NUM_COLS
                }
            }
        }]
    })