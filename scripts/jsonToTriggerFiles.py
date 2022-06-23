import os
import re
from master_maps import triggerNameMapping;

filePath = "D:\\testingFolder\\"
entryFile = "D:\\testingFolder\\Entries.txt"


def main():
    print("**************  SCRIPT START ************");
    print("Size of triggerNameMapping : ", len(triggerNameMapping));
    print("File Path : ",filePath);

    for triggerMap in triggerNameMapping:
        createNewFile(triggerMap);


def createNewFile(triggerMap):
    print("Working for trigger Name : "+triggerMap['triggerName']);
    fileName = getFileName("Action", triggerMap )
    updateFileContent(fileName, triggerMap, filePath)
    fileName = getFileName("Condition", triggerMap)
    updateFileContent(fileName, triggerMap, filePath)

    createEntryInFile(triggerMap, fileName)



def getFileName(code, triggerMap ):
    fileName = code+"_"+triggerMap['triggerName']+"_"+triggerMap['triggerResource']+"_"+triggerMap['triggerType']+".groovy";
    return fileName

def updateFileContent(fileName, triggerMap, path=""):
    code = fileName.split('_')[0]
    fileName = path + fileName;
    with open(fileName, "w") as f:
        if(code=="Condition"):
            f.write(triggerMap['condition'])
        else:
            f.write(triggerMap['actionCode'])



def createEntryInFile(triggerMap, triggerName):
    print("Opening File : ", triggerName);
    triggerType = triggerMap['triggerType']
    isEnabled = "true" if triggerMap['enabled'] else "false"
    resource = triggerMap['triggerResource']
    description = triggerMap['description']

    triggerName = triggerName.replace(".groovy","");
    triggerType = triggerName.split("_")[-1] if not triggerType else triggerType.upper();
    isEnabled = isEnabled.lower();
    resource = triggerName.split("_")[-2] if not resource else resource[0].upper()+resource[1:];

    textToWrite = triggerName +" | "+ resource +" | "+ triggerType +" | "+ isEnabled +" | "+ "Action_"+triggerName+".groovy" +" | "+ "Condition_"+triggerName+".groovy" +" | "+ description+"\n"
    with open(entryFile, "a") as f:
        f.write(textToWrite)


if __name__ == '__main__':
    main()