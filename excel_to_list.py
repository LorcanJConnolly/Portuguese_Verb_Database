""" Extracts a column of verbs as a list. """
import openpyxl

def extract(path):
    list = []
    wb_obj = openpyxl.load_workbook(path)
    ws_obj = wb_obj.active
    for row in ws_obj.iter_rows(max_col=1):
        try:
            for cell in row:
                if not isinstance(cell.value, str):
                    raise ValueError(f"\nERROR: Verbs must be strings.\n---DEBUG INFO:\n------Wrong input: '{cell.value}'\n")
                else: 
                    list.append(cell.value)
        except ValueError as e:
            print(e)
            continue 
    return list