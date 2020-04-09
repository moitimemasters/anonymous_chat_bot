from datetime import datetime
import xlwt
import xlrd


def create_table(name):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(f"Dialog_{name}")
    ws.write(0, 0, 0)
    ws.write(0, 1, str(datetime.utcnow()))
    ws.write(0, 2, 0)
    ws.write(0, 3, 0)
    wb.save(f"dialogs/{name}.xls")


def add_info(username, content, id):
    wb = xlrd.open_workbook(f"dialogs/{id}.xls")
    ws = wb.sheet_by_index(0)
    row = int(ws.cell(0, 0).value)
    data = []
    for i in range(row + 1):
        line = []
        for j in range(4):
            line.append(ws.cell(i, j).value)
        data += [line]
    wb = xlwt.Workbook()
    data[0][0] = row + 1
    ws = wb.add_sheet(f"Dialog_{id}")
    for i in range(row + 1):
        for j in range(4):
            ws.write(i, j, data[i][j])
    row += 1
    ws.write(row, 1, username)
    ws.write(row, 2, content)
    ws.write(row, 3, str(datetime.utcnow()))
    wb.save(f"dialogs/{id}.xls")
