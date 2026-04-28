import openpyxl
from openpyxl.utils.cell import column_index_from_string

from os import listdir as ls
from os.path import exists, join

from checks import CHECKS

# If any tabs in the workbooks should be skipped, add their names to this list
SHEETS_TO_SKIP = []

# Set to first non-header row (1-indexed)
MINROW = 2

# column_index_from_string is 1-indexed, so we subtract 1 from the result
JP_COLUMN = column_index_from_string('B') - 1
TL_COLUMN = column_index_from_string('D') - 1
EDIT_COLUMN = column_index_from_string('E') - 1
QA_COLUMN = column_index_from_string('F') - 1

def trim_jp_for_BGI_script_commands(jp):
    return jp.strip(".&")

def format_error_sheet(error_worksheet):
    error_worksheet.title = "Errors"
    error_worksheet.column_dimensions['A'].width = 16
    error_worksheet.column_dimensions['C'].width = 60
    error_worksheet.column_dimensions['D'].width = 60
    
    header = ["Script", "Row", "Line", "Error"]
    error_worksheet.append(header)


def check_line(error_worksheet, script_name, script_row, jp, tl, edit, qa):
    if jp is None:
        return
    
    jp = trim_jp_for_BGI_script_commands(jp)
    
    en = qa or edit or tl
    
    for check in CHECKS:
        error = check(en, jp)
        if error is not None:
            error_row = [script_name, script_row, en, error]
            error_worksheet.append(error_row)


def main():
    error_workbook = openpyxl.Workbook()
    error_worksheet = error_workbook.active
    format_error_sheet(error_worksheet)

    if not exists('sheets'):
        print('Could not find `sheets` folder. Is the program being run from the correct folder?')
    
    for filename in ls('sheets'):
        # Ignore hidden files
        if filename.startswith('.'):
            continue
        
        workbook = openpyxl.load_workbook(join('sheets', filename))
        for sheet_name in workbook.sheetnames:
            if sheet_name in SHEETS_TO_SKIP:
                continue
            sheet = workbook[sheet_name]
            for idx, row in enumerate(sheet.iter_rows(min_row=MINROW, values_only=True)):
                jp = row[JP_COLUMN]
                tl = row[TL_COLUMN]
                edit = row[EDIT_COLUMN]
                qa = row[QA_COLUMN]
                check_line(error_worksheet, sheet_name, idx + MINROW, jp, tl, edit, qa)

    error_workbook.save("errors_and_warnings.xlsx")
    print("Done.")


main()