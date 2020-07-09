import os
import shutil
import re
import json
import sys
from datetime import datetime

# --- Variables Assignment ---
count = 0;
def commonVariables(baseDir):
    angularFilePath = []
    angularFilePath.append(baseDir + "/apps/angular/angular/themes/");

    angularJsonFilePath = []
    angularJsonFilePath.append(baseDir + "/apps/angular/angular/themes/languages/en.json");
    angularJsonFilePath.append(baseDir + "/apps/angular/angular/themes/languages/en_signup.json");

    skynetFilePath = []
    skynetFilePath.append(baseDir + "/data/app_configs/configuration/conf");
    skynetFilePath.append(baseDir + "/data/app_configs/configuration/latestExternalConfig");

    skynetJsonFilePath = []
    skynetJsonFilePath.append(baseDir + "/apps/skynet/skynet/skynet/languages/en.json");

    returnMap = {}
    returnMap["angularFilePath"] = angularFilePath;
    returnMap["angularJsonFilePath"] = angularJsonFilePath;
    returnMap["skynetFilePath"] = skynetFilePath;
    returnMap["skynetJsonFilePath"] = skynetJsonFilePath;
    returnMap["backupFilePath"] = baseDir + "/data/missingLabelUtility/jsonBackup/";
    returnMap["saveDir"] = baseDir + "/data/missingLabelUtility/";

    return returnMap;

def createNewOutputFile(filePath,lang):
    saveDir = filePath.get("saveDir");
    if not os.path.exists(saveDir):
        os.makedirs(saveDir);
    saveDir = saveDir+"missingLabels_"+ datetime.now().strftime("_%Y%m%d%H%M%S_")+lang+".csv";
    f = open(saveDir, "w+");
    f.write("SNo,Category,Label,Avl Status,Occurrence,File\n");
    f.close();
    return saveDir

def backupFile(dir,files):
    if not os.path.exists(dir):
        os.makedirs(dir);
    for f in files:
        shutil.copy(f, dir)
    print("\nBackup has been created for following file at directory : "+ dir);
    print(files);

def getHTMLLabels(saveDir, filePath):
    category = "html";
    dirPathList = filePath.get("angularFilePath")
    jsonFilesPath = filePath.get("angularJsonFilePath")
    regexList = []
    regexList.append(re.compile(r'ng\s*-\s*bind\s*=\s*"\s*["\']([ \w\\\/\-\.]+)["\']\s*\|\s*translate"'));
    regexList.append(re.compile(r'{{["\']([ \w\\\/\-\.]+)["\']\s*\|\s*translate}}'));

    missingLabelUtility(category, dirPathList, jsonFilesPath, saveDir, regexList);


def getJSLabels(saveDir, filePath):
    category = "js";
    dirPathList = filePath.get("angularFilePath")
    jsonFilesPath = filePath.get("angularJsonFilePath")
    regexList = []
    regexList.append(re.compile(r'\$filter\s*\(\s*["\']translate["\']\s*\)\s*\(\s*["\']([ \w\\\/\-\.]+)["\']\s*\)'));

    missingLabelUtility(category, dirPathList, jsonFilesPath, saveDir, regexList);


def getNotificationLabels(saveDir, filePath):
    category = "notification";
    dirPathList = filePath.get("skynetFilePath")
    for jsonFile in filePath.get("angularJsonFilePath"):
        if os.path.exists(jsonFile):
            print("File exists at : "+jsonFile);
            jsonFilesPath = filePath.get("angularJsonFilePath");
        else:
            jsonFilesPath = getFiles(filePath.get("backupFilePath"), ".json");
            print("File exists at : "+str(jsonFilesPath));
            break;

    regexList = []
    regexList.append(re.compile(r'\.returnLanguageMapValue\s*\(\s*["\']([ \w\\\/\-\.]+)["\']\s*[,\)]'));

    missingLabelUtility(category, dirPathList, jsonFilesPath, saveDir, regexList);


def getSkynetConfigLabels(saveDir, filePath):
    category = "skynetTag";
    dirPathList = filePath.get("skynetFilePath");
    jsonFilesPath = filePath.get("skynetJsonFilePath");
    regexList = []
    regexList.append(re.compile(r'\/\/\@Taglist\s*\-\s*[ \w\\\/\-\.]+\>([ \w\\\/\-\.]+)\n'));
    regexList.append(re.compile(r'\/\/\@Taglist\s*\-\s*([ \w\\\/\-\.]+)\n'));
    missingLabelUtility(category, dirPathList, jsonFilesPath, saveDir, regexList);

    category = "skynetLabel";
    regexList = []
    regexList.append(re.compile(r'\@\@(\w+)\n\/\/\@(\w+)\s*\-\s*(.+?)\n'));

    missingLabelUtility(category, dirPathList, jsonFilesPath, saveDir, regexList);


# --- Main Method  ---
def main():
    workspace = sys.argv[1];
    applicationList = sys.argv[2] if len(sys.argv) > 2 else "ALL";
    filePath = commonVariables(workspace);
    print("Active services : "+applicationList)

    applicationList = applicationList.split(',');
    saveDir = createNewOutputFile(filePath, "en");

    if "MINERVA" in applicationList or "ALL" in applicationList :
        backupFile(filePath.get("backupFilePath"),filePath.get("angularJsonFilePath"));
        getHTMLLabels(saveDir, filePath);
        getJSLabels(saveDir, filePath);

    if "SKYNETSERVER" in applicationList or "ALL" in applicationList:
        getNotificationLabels(saveDir, filePath);
        getSkynetConfigLabels(saveDir, filePath);

    print("\nOutput has been saved to Dir : " + saveDir)


"""
    --- missingLabelUtility ---
    @category : String
    @dirPathList : List<String>
    @jsonFilesPath : List<String>
    @saveDir : String
    @regexList : List<re.compile>
"""


def missingLabelUtility(category, dirPathList, jsonFilesPath, saveDir, regexList):
    print("------------------------------------------------------------");
    extensionMap = {'js': '.js',
                    'html': '.html',
                    'skynetTag': '.groovy',
                    'skynetLabel': '.groovy',
                    'notification': '.groovy'}
    for dirPath in dirPathList:
        print("BEGAN : MissingLabelUtility for %s files at path %s.\n" % (category,dirPath));
        try:
            fileList = getFiles(dirPath, extensionMap.get(category));
            print("Number of %s files received : %d ." % (extensionMap.get(category), len(fileList)));

            matchesDict = getMatches(fileList, regexList, category, dirPath);
            print("Number of labels found in %s files : %d ." % (category, len(matchesDict)));

            missingLabelsDict = getMissingLabels(jsonFilesPath, matchesDict)
            print("Number of labels traced: %d ." % len(missingLabelsDict));

            cnt = generateOutput(missingLabelsDict, saveDir);
            print("Total entries in csv are %d after inserting labels for %s files." % (cnt, category));
        except:
            print("Got exception getting missing labels for %s files." % category);
            print(sys.exc_info()[1]);

        print("\nENDS : MissingLabelUtility for %s files." % category);
    print("------------------------------------------------------------");


"""
    --- getFiles ---
    @dirPath : String
    @ext : String
    return : List<String>
"""


def getFiles(dirPath, ext):
    fileList = [];
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dirPath):
        for file in f:
            if file[-len(ext):] == ext:
                fileList.append(os.path.join(r, file));
            if ext == '.html' and file[-4:] == '.htm':
                fileList.append(os.path.join(r, file));
    return fileList;


"""
    --- getMatches ---
    @fileList : List<String>
    @regexList : List<re.compile>
    @category : String
    @dirPath : String
    return : Dictionary   
"""


def getMatches(fileList, regexList, category, dirPath):
    matchesDict = {}
    workingFile = "";

    for f in fileList:
        workingFile = f;
        matches = [];
        try:
            fileObj = open(f, "r");
            fileString = fileObj.read()
            fileObj.close()
            if category == 'skynetLabel':
                groupedMatches = []
                for reg in regexList:
                    groupedMatches.extend(reg.findall(fileString));

                groupLabel = "";
                for mch in groupedMatches:
                    componentLabel = "";
                    if (len(mch) >= 3 and mch[0] == 'Group' and mch[1] == 'Name'):
                        groupLabel = "component." + str(mch[2]);
                    elif (len(mch) >= 3 and mch[0] == 'Component' and mch[1] == 'Name'):
                        componentLabel = str(mch[2]) + ".name"
                    else:
                        print("Unable to find group or component from skynetLabel refValue :  ");
                        print(mch);
                        groupLabel = "";

                    if (groupLabel != "" and componentLabel != ""):
                        matches.append(groupLabel + "." + componentLabel)

            elif category == 'skynetTag':
                for reg in regexList:
                    matches.extend(reg.findall(fileString));
            else:
                if f[-5:] == '.html' or f[-4:] == '.htm':
                    commentReg = re.compile(r'(?s)\<\s*\!\-\-.*?\-\-\s*\>')
                    fileString = re.sub(commentReg, "", fileString);
                elif f[-3:] == '.js' or f[-7:] == '.groovy':
                    commentReg = re.compile(r'(?s)\/\*.*?\*\/')
                    fileString = re.sub(commentReg, "", fileString);
                    commentReg = re.compile(r'(?s)\/\/.*?\n')
                    fileString = re.sub(commentReg, "", fileString);
                for reg in regexList:
                    matches.extend(reg.findall(fileString));
        except:
            print("exception Occuered while working for file : " + workingFile);
            print(sys.exc_info()[1]);

        for mch in matches:
            if category == "skynetTag":
                mch = 'tagName.' + mch;
            if not matchesDict.get(mch):
                matchesDict[mch] = {};
            matchesDict[mch]['category'] = category;
            matchesDict[mch]['status'] = False;
            matchesDict[mch]['occurrence'] = matchesDict[mch].get('occurrence') + 1 if matchesDict[mch].get(
                'occurrence') else 1;
            fname = f.replace(dirPath, "");
            if matchesDict[mch].get('fname'):
                if fname not in matchesDict[mch].get('fname'):
                    matchesDict[mch].get('fname').append(fname);
            else:
                matchesDict[mch]['fname'] = [fname];

    return matchesDict;


"""
    --- getMissingLabels ---
    @jsonFilesPath : List<String>
    @matchesDict : Dictionary
    return : Dictionary
"""


def getMissingLabels(jsonFilesPath, matchesDict):
    for jsonFile in jsonFilesPath:
        with open(jsonFile) as json_file:
            jsonObj = json.load(json_file);
            jsonObj = flatten_json(jsonObj)
            for k in matchesDict:
                if matchesDict[k]['status'] == False and k in jsonObj:
                    matchesDict[k]['status'] = True;

    return matchesDict;


"""
    --- generateOutput ---
    @jsonFilesPath : List<String>
    @matchesDict : Dictionary
    return : Dictionary
"""


def generateOutput(labelDict, saveDir):
    global count
    f = open(saveDir, "a+")
    for key, val in labelDict.items():
        if val['status'] == False:
            count += 1
            f.write(str(count) + "," + str(val['category']) + "," + str(key) + "," + str(val['status']) + "," + str(
                val['occurrence']) + "," + str('|'.join(val['fname'])) + "\n");
    f.close()

    return count;


"""
    --- flatten_json ---
    @y : String
    return : Dictionary
"""


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


if __name__ == '__main__':
    main()
