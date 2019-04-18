import datetime
from openpyxl.reader.excel import load_workbook
from datetime import datetime
import xlrd
import os
import re

# version 2.6.2

# path = "C:\\Users\\Admin\\Desktop\\demo.xlsx"
'''
openpyxl.utils.exceptions.InvalidFileException: openpyxl does not support the old .xls file format, please use xlrd to read this file, or convert it to the more recent .xlsx file format.

'''


class readExcel(object):
    def __init__(self, filepath, filename):
        self.filepath = filepath
        self.filename = filename
        self.fileType = None
        self.excelDict = dict()

    def typeOfExcel(self):
        judgeExcel = {
            'xlsx': self.readXls,
            'xls': self.readXlsx,
        }
        self.fileType = re.split('\.', self.filename)[-1]
        print(self.fileType)
        func = judgeExcel.get(self.fileType, 'error')
        return func()

    def readXls(self):
        xldata = xlrd.open_workbook(self.filepath)
        xltable = xldata.sheets()[0]
        nrows = xltable.nrows
        ncols = xltable.ncols
        for row in range(nrows):
            if row == 0:
                continue
            for col in range(ncols):
                self.excelDict[row][col] = xltable.row_values(row)[col]
        return self.excelDict

    def readXlsx(self):
        print(self.filepath)
        workBooktObj = load_workbook(self.filepath)
        sheetNames = workBooktObj.get_sheet_names()
        sheetObj = workBooktObj.get_sheet_by_name(sheetNames[0])
        maxCol = sheetObj.max_column
        maxRow = sheetObj.max_row

        # Loop will print all columns name
        for row in range(2, maxRow + 1):
            for col in range(1, maxCol + 1):
                self.excelDict[row][col] = sheetObj.cell(row=row, column=col).value
                # cell_obj = sheetObj.cell(row=row, column=col)
                # print(cell_obj.value)
        return self.excelDict


if __name__ == '__main__':
    # path = os.path.abspath('testfile.xlsx')
    # print(path)
    # filename = 'testfile.xlsx'
    # obj = readExcel(path, filename)
    # testdict = obj.typeOfExcel()
    # print(testdict)
    a = {1: 2, 3: 4, 5: 6}
    for i in a:
        print(i)
