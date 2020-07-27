import io, os , sys, shutil
import json
import csv
from collections import OrderedDict

sourceJsonFile = "D:\\Codebase\\minerva-customizations\\mphrx-angular\\themes\\languages\\en.json"
outputPath = "D:\\Codebase\\minerva-customizations\\mphrx-angular\\themes\\languages\\"
csvFileName = "translation.csv"
newValuesInRow = 1

masterMap = {

}

def addNewKeysInJson( fileName, keysMap):

    with io.open(fileName, encoding='utf8') as file:
        jsonContent = json.load(file, object_pairs_hook=OrderedDict);

        with open(csvFileName, encoding="utf8") as file:
            csv_reader = csv.reader(file, delimiter=',')

            rowNumber = 0
            for row in csv_reader:
                if rowNumber == 0:
                    rowNumber += 1
                    continue
                print("Row Number : ", rowNumber, " | Value : ", row[0]," : ",row[newValuesInRow]);
                updatekey(jsonContent,row[0].split("."),row[newValuesInRow]);
                rowNumber += 1

    with io.open(fileName, 'w', encoding='utf8') as f:
        f.write(json.dumps(jsonContent, indent=4, ensure_ascii=False));



def createCopyOfFile(file,outputPath):
    fileName = outputPath + "output." + file.split(".")[-1]
    shutil.copyfile(file, fileName)
    if os.path.exists(fileName):
        return fileName
    else:
        return ""


def updatekey(dict, keyList, value, index=-1):
    index += 1;
    if index < len(keyList) - 1:
        if (not dict or (dict and keyList[index] not in dict)):
            dict[keyList[index]] = {};

        updatekey(dict[keyList[index]], keyList, value, index)
    if index == len(keyList) - 1:
        dict[keyList[index]] = value

def main():
    print("**START : ADD NEW KEYS TO JSON**\n");
    newFile = createCopyOfFile(sourceJsonFile, outputPath)
    addNewKeysInJson(newFile, masterMap)

    if not newFile:
        print("File not exists : ", newFile)
        return 0

    print("**END : ADD NEW KEYS TO JSON**\n");

if __name__ == '__main__':
    main()