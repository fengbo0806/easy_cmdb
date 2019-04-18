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


class readExcel:
    def __init__(self, filepath, filename):
        self.filepath = filepath
        self.filename = filename
        self.fileType = None

    def typeOfExcel(self):
        judgeExcel = {
            'xlsx': self.readXls,
            'xls': self.readXlsx,
        }
        self.fileType = re.split('\.', self.filename)[-1]
        func = judgeExcel.get(self.fileType, 'error')
        return func()

    def readXls(self):
        xldata = xlrd.open_workbook('testfile.xls')
        xltable = xldata.sheets()[0]
        nrows = xltable.nrows
        ncols = xltable.ncols
        for i in range(nrows):
            if i == 0:
                continue
            for j in range(ncols):
                print(type(xltable.row_values(i)[j]))
            print('-----')
        print(xltable.row_values(i)[0])
        print(type(xltable.row_values(i)[0]))
        firstsell = xlrd.xldate_as_datetime(xltable.row_values(i)[0], 0)
        print(firstsell)
        secondsell = xlrd.xldate_as_datetime(xltable.row_values(i)[1], 1)
        print(secondsell)
        thirdsell = xlrd.xldate_as_datetime(xltable.row_values(i)[2].value, 1)
        fourthsell = xlrd.xldate_as_datetime(xltable.row_values(i)[3].value, 1)
        startdate = datetime.datetime(firstsell.year, firstsell.month, firstsell.day, secondsell.hour,
                                      secondsell.minute)
        enddate = datetime.datetime(thirdsell.year, thirdsell.month, thirdsell.day, fourthsell.hour,
                                    fourthsell.minute)

    def readXlsx(self):
        sheetObj = load_workbook(self.filepath).active
        maxCol = sheetObj.max_column
        maxRow = sheetObj.max_row
        excelDict = dict()
        print('tttttt')
        # Loop will print all columns name
        for row in range(2, maxRow + 1):
            for col in range(1, maxCol + 1):
                excelDict[row][col]=sheetObj.cell(row=row, column=col).value
                # cell_obj = sheetObj.cell(row=row, column=col)
                # print(cell_obj.value)
        return excelDict


if __name__ == '__main__':
    path = os.path.abspath('testfile.xlsx')
    filename = 'testfile.xlsx'
    obj = readExcel(path, filename)
    testdict = obj.fileType()
    print(testdict)

