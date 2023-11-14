from utils import getDecrypted, spreadSheetClient, openWorkbookByName, newWorksheet, generatePayload, autoResizeColumn, updateSummary, addConditionalFormatting
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('incorrect number of arguments, aborting...')
        sys.exit()
    uid, now = sys.argv[1:]
    # now = re.sub(r'\.[^+]*', '', str(pendulum.now()))   # '2023-11-14T01:48:16+08:00'

    workbookName = 'Raspi_Status'
    client = spreadSheetClient(getDecrypted('SECRET_GOOGLE_JSON'))
    workbook = openWorkbookByName(client, workbookName)

    physical = uid.split('_')[1]
    sheet = newWorksheet(workbook, physical)
    sheet.update(generatePayload(sheet._properties['index'], uid, now), value_input_option='USER_ENTERED')
    
    summarySheet = updateSummary(workbook, physical)

    autoResizeColumn(workbook, sheet)
    autoResizeColumn(workbook, summarySheet)
    addConditionalFormatting(workbook, summarySheet)