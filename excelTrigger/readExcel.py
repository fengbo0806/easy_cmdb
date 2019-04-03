from openpyxl.reader.excel import load_workbook
#version 2.6.2
wb = load_workbook('dd.xlsx')
sheetnames = wb.get_sheet_names()
ws = wb.get_sheet_by_name(sheetnames[0])

data_dic = {}  # 建立存储数据的字典
# 把数据存到字典中
for rx in range(ws.get_highest_row()):
    temp_list = []
    pid = ws.cell(row=rx, column=0).value
    w1 = ws.cell(row=rx, column=1).value
    w2 = ws.cell(row=rx, column=2).value
    w3 = ws.cell(row=rx, column=3).value
    w4 = ws.cell(row=rx, column=4).value
    temp_list = [w1, w2, w3, w4]
    data_dic[pid] = temp_list

print(data_dic[10124020117])