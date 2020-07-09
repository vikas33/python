import io, os , sys, shutil
import json
from collections import OrderedDict

sourceJsonFile = "D:\\Codebase\\minerva-customizations\\mphrx-angular\\themes\\languages\\el.json"
outputPath = "D:\\Codebase\\minerva-customizations\\mphrx-angular\\themes\\languages\\"

masterMap = {

}

def addNewKeysInJson(fileName, keysMap):
    with io.open(fileName, encoding='utf8') as file:
        jsonContent = json.load(file, object_pairs_hook=OrderedDict);
        jsonContent["encounters"]["list"]["duration"] = {}


        jsonContent["questionnair"]["showPatResponse"]["downloadAllLabel"] = "Κατεβάστε με επισυναπτόμενα"
        jsonContent["questionnair"]["showPatResponse"]["downloadResponseLabel"] = "Κατεβάστε απαντήσεις"
        jsonContent["encounters"]["list"]["duration"]["m"] = "Λεπτά"
        jsonContent["encounters"]["list"]["duration"]["M"] = "Λεπτά"
        jsonContent["encounters"]["list"]["duration"]["h"] = "Ώρα"
        jsonContent["encounters"]["list"]["duration"]["H"] = "Ώρα"
        jsonContent["encounters"]["list"]["durationLabel"] = "Διάρκεια"
        jsonContent["encounterCard"]["VIRTUAL"] = "Εικονικά"

    with io.open(fileName, 'w', encoding='utf8') as f:
        f.write(json.dumps(jsonContent, indent=4, ensure_ascii=False));



def createCopyOfFile(file,outputPath):
    fileName = outputPath + "output." + file.split(".")[-1]
    shutil.copyfile(file, fileName)
    if os.path.exists(fileName):
        return fileName
    else:
        return ""


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