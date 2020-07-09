import csv
import io, os , sys, shutil
import json
from collections import OrderedDict

def createCopyOfFile(file,outputPath):
    fileName = outputPath + "output." + file.split(".")[-1]
    shutil.copyfile(file, fileName)
    if os.path.exists(fileName):
        return fileName
    else:
        return ""

def readCsv(csvFile):
    translationDict = {}
    with open(csvFile, encoding="utf8") as file:
        csv_reader = csv.reader(file, delimiter=',')

        rowNumber = 0
        for row in csv_reader:
            if rowNumber == 0:
                rowNumber += 1
                continue
            print("Row Number : ", rowNumber, " | Key : ", row[0])
            translationDict[row[0]] = {}
            translationDict[row[0]]['value'] = row[1]
            translationDict[row[0]]['status'] = 'FAILED'
            rowNumber += 1

        print("Read rows : ", rowNumber)

    return translationDict


def iterateDict(dictionary, translationDict):
    for key, value in dictionary.items():
        oldKey.append(key)
        if not isinstance(value, str):
            iterateDict(value, translationDict)
            continue
        else:
            if translationDict.get(value):
                dictionary[key] = translationDict.get(value).get('value')
                jsonKeys = ('.'.join(oldKey))
                translationDict[value]['status'] = 'SUCCESS'
                translationDict[value]['jsonKeys'] = translationDict[value].get('jsonKeys')+"\n"+ jsonKeys if translationDict[value].get('jsonKeys') else jsonKeys

            oldKey.pop()
    if len(oldKey):
        oldKey.pop()
    return dictionary


def updateLanguageJson(jsonFile,translationDict, changeLog):
    with io.open(jsonFile, encoding='utf8') as file:
        jsonContent = json.load(file, object_pairs_hook=OrderedDict);

        global oldKey
        oldKey = []
        jsonContent = iterateDict(jsonContent, translationDict)

    with open(changeLog, 'w', encoding="utf8") as f:
        f.write("S No.,Value,New Value,Status,JSON Keys\n")
        sNo =  1
        for key, value in translationDict.items():
            jsonKeys = value.get('jsonKeys') if value.get('jsonKeys') else ""
            status = value.get('status')
            newValue = value.get('value')
            writeValue = str(sNo)+',"'+key+'","'+newValue+'","'+status+'","'+jsonKeys+'"\n'
            f.write(writeValue)

            sNo += 1


    with io.open(jsonFile, 'w', encoding='utf8') as f:
        f.write(json.dumps(jsonContent, indent=4, ensure_ascii=False));




def main():
    print("**START : CSV TO LANGUAGE JSON**\n");

    csvFile = str(sys.argv[0]) if len(sys.argv) > 3 else "D:\\Aster\\csvToJson\\TranslatedLanguage.csv";
    jsonFile = str(sys.argv[1]) if len(sys.argv) > 4 else "D:\\Codebase\\UHG\\minerva-customizations\\mphrx-angular\\themes\\languages\\ml.json";
    outputDir = str(sys.argv[2]) if len(sys.argv) > 5 else "D:\\Aster\\csvToJson\\";
    changeLog = str(sys.argv[2]) if len(sys.argv) > 5 else "D:\\Aster\\\csvToJson\\changeLog.csv";
    newfile = createCopyOfFile(jsonFile, outputDir)

    if not newfile:
        print("File not exists : ",newfile)
        return 0

    translationDict = readCsv(csvFile)
    updateLanguageJson(newfile, translationDict, changeLog)

    print("**END : CSV TO LANGUAGE JSON**\n");

if __name__ == '__main__':
    main()