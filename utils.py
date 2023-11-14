### GOOGLE SHEETS API ###

# Required functions :
# - authorization

# Useful APIs :
# - retrieve all sheets > .worksheets()
# - get sheet records > .get_all_records()
# - update summary sheet (.acell/.arange: notation) (.cell/.range: row, col)
# - .

from oauth2client.service_account import ServiceAccountCredentials
from cryptography.fernet import Fernet
import gspread
import json
import os

### CONSTANTS ###
SHEET_COLUMNS = ['number', 'physical', 'hostname', 'address', 'last ping', 'status']
SHEET_NUM_ROWS = 2
SHEET_NUM_COLS = 6
SHEET_PING_TIMEOUT = 2

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
        [number, physical+'   ', hostname+'   ', address, now, f'=if(E{SHEET_NUM_ROWS} > now()-time(0, {SHEET_PING_TIMEOUT}, 0), "ok", "no")']
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

def checkRequiredConditionalFormat(wb):
    summarySheet = next(filter(lambda x: x['properties']['title'] == 'Summary', wb.fetch_sheet_metadata()['sheets']))
    if 'conditionalFormats' in summarySheet:
        checkValues = [conditonalFormat['booleanRule']['condition']['values'][0]['userEnteredValue'] for conditonalFormat in summarySheet['conditionalFormats']]
        if {'no', 'ok'} == set(checkValues):
            return True
    return False

def addConditionalFormatting(wb, sheet):
    formatRange = {
        "sheetId": sheet._properties['sheetId'],
        "startRowIndex": 1,
        "endRowIndex": 100,
        "startColumnIndex": 5,
        "endColumnIndex": 6,
    }
    # check if conditional format exists
    if checkRequiredConditionalFormat(wb):
        print('no need to add conditional formatting')
        return
    print('adding conditional formatting')
    wb.batch_update({
        "requests": [{
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [formatRange],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_EQ",
                            "values": [
                                {
                                    "userEnteredValue": "ok"
                                }
                            ]
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 0.4,
                                "green": 1,
                                "blue": 0.4,
                            }
                        }
                    }
                },
                "index": 0
            }
        }, {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [formatRange],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_EQ",
                            "values": [
                                {
                                    "userEnteredValue": "no"
                                }
                            ],
                        },
                        "format": {
                            "backgroundColor": {
                                "red": 1,
                                "green": 0.4,
                                "blue": 0.4,
                            }
                        }
                    }
                },
                "index": 1
            }
        }]
    })

# update A2-F2
def updateSummary(wb, name):
    summarySheet = newWorksheet(wb, 'Summary')
    # check for existing entries
    records = summarySheet.get_all_records()
    if len(records):
        if name in map(lambda x: x['physical'].strip(), records):
            print(f'record exists for {name}')
            return summarySheet
        cellRange = f'A{SHEET_NUM_ROWS+1}:F{SHEET_NUM_ROWS+1}'
    else:
        cellRange = f'A{SHEET_NUM_ROWS}:F{SHEET_NUM_ROWS}'
    print(f'creating new record for {name}')
    cells = summarySheet.range(cellRange)
    for cell in cells:
        cell.value = f"=OFFSET('{name}'!{cell.address}, -{len(records)}, 0)"
    summarySheet.update_cells(cells, value_input_option='USER_ENTERED')
    return summarySheet