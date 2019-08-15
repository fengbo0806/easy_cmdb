from .readExcel import *
from configureBaseData.models.suppliers import VideoSupplier, SupplyProgram


class syncTable(object):
    def __init__(self, filepath, filename):
        self.path = filepath
        self.filename = filename

    def writetodb(self):
        obj = readExcel(filepath=self.path, filename=self.filename, )
        objDict = obj.typeOfExcel()
        for item in objDict:
            if item == 0:
                continue
            # print(objDict[item])
            # if objDict[item].count('') > 5:
            #     continue
            # print(type(objDict[item]))
            # objlist=list(objDict[item])
            print(item)
            chinaname = objDict[item][0]
            programname = objDict[item][1]
            programtype=objDict[item][2]

            height = objDict[item][3]
            width = objDict[item][4]
            bandwidth = objDict[item][5]
            inPutType = objDict[item][6]
            inPutStream = objDict[item][7]


            'TypeError: expected string or bytes-like object'
            VideoSupplier.objects.update_or_create(chinaname=chinaname)
            SupplyProgram.objects.update_or_create(
                programname=programname,
                programtype=programtype,
                vender=VideoSupplier.objects.get(chinaname=chinaname),
                programid=None,
                height=height,
                width=width,
                bandwidth=bandwidth,
                inPutType=inPutType,
                inPutStream=inPutStream,
            )


if __name__ == '__main__':
    pass
