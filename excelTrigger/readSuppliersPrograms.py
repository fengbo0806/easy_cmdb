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
            programName = objDict[item][4]
            if len(programName) < 5:
                continue
            print(objDict[item])
            chinaname = objDict[item],
            programname = objDict[item],
            note = objDict[item],
            height = objDict[item],
            width = objDict[item],
            bandwidth = objDict[item],
            inPutType = objDict[item],
            inPutStream = objDict[item],
            VideoSupplier.objects.update_or_create(chinaname=chinaname)
            SupplyProgram.objects.update_or_create(
                programname=programname,
                vender=VideoSupplier.objects.get(chinaname=chinaname),
                note=note,
                height=height,
                width=width,
                bandwidth=bandwidth,
                inPutType=inPutType,
                inPutStream=inPutStream,
            )


if __name__ == '__main__':
    pass
