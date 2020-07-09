import sys
import os.path
import json
import os, shutil
import io
from jsonmerge import merge
from collections import OrderedDict
import tkinter as tk
import logging

#1. CUSTID, 2. Langauge file Name 3. backup Path 4. oldFile path, 5. newFile Path 6. output Path

def main():
    logging.basicConfig(filename='jsonMerger.log',
                        level=logging.INFO)
    logging.info("**MERGE UTILITY BEGINS**\n");

    custId = str(sys.argv[1]) if len(sys.argv) > 1 else "Test";
    lang = str(sys.argv[2]) if len(sys.argv) > 2 else "en";
    backupDir = str(sys.argv[3]) if len(sys.argv) > 3 else "backup\\";
    oldFileDir = str(sys.argv[4]) if len(sys.argv) > 4 else "old.json";
    newFileDir = str(sys.argv[5]) if len(sys.argv) > 5 else "new.json";
    outputDir = str(sys.argv[6]) if len(sys.argv) > 6 else "output\\";
    isDiffRequired = True;

    if custId:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir);
        if os.path.exists(oldFileDir) and os.path.exists(newFileDir) :
            mergeUtility(lang+".json", backupDir, oldFileDir, newFileDir, outputDir,isDiffRequired);
            mergeUtility(lang+"_signup.json", backupDir, oldFileDir, newFileDir, outputDir,isDiffRequired);
            logging.info("Please find merged file at : "+ outputDir)
        else:
            logging.info("Unable to find directory : "+newFileDir+" or "+oldFileDir);

    else:
        logging.info("CUSTID is missing in First argument which is used for defining file path"+custId);


    logging.info("\n\n**MERGE UTILITY ENDS**");

def mergeUtility(lang, backupDir, oldFileDir, newFileDir, outputDir, isDiffRequired = False):
    logging.info("\nWorking for language : "+lang);
    logging.info("Looking for json file at path : "+oldFileDir);

    file_list = getFiles(oldFileDir, lang);
    if len(file_list):
        backupFile(backupDir, file_list);
        for file in file_list:

            if newFileDir[-5:] == ".json":
                newFile = newFileDir;
                fileName = file.rsplit("\\", 1)[-1];
            else:
                fileName = file.rsplit("\\", 1)[-1];
                newFile = newFileDir + fileName;

            if os.path.exists(newFile) :
                outputFile = outputDir + fileName;
                mergeFiles(newFile, file, outputFile);
                if isDiffRequired:
                    findDiff(outputDir,fileName,file);

            else :
                logging.info("No file found for update with name : "+newFile);
                continue;

    else:
        logging.info("No file found with name : "+lang)


def mergeFiles(newFile, oldFile, outputFile) :
    try:
        logging.info("Loading file : " + newFile);
        with io.open(newFile, encoding='utf8') as data_file1:
            content1 = json.load(data_file1, object_pairs_hook=OrderedDict);

        logging.info("Loading file : " + oldFile);
        with io.open(oldFile, encoding='utf8') as data_file2:
            content2 = json.load(data_file2, object_pairs_hook=OrderedDict);

        output = merge(content1, content2);
        #content1.update(content2)

        with io.open(outputFile, 'w', encoding='utf8') as f:
            f.write(json.dumps(output, indent=4, ensure_ascii=False));

        logging.info("Merged SUCCESSFULLY ");

    except :
        logging.info("Merging FAILED");
        logging.info(sys.exc_info());


def backupFile(dir,files):
    if not os.path.exists(dir):
        os.makedirs(dir);
    for f in files:
        shutil.copy(f, dir)
    logging.info("Backup has been created for following file at directory : "+ dir);
    logging.info(files);

def findDiff(outputDir,fileName,oldFile):
    diffFile = outputDir + "diff_"+fileName;
    newFile = outputDir + fileName;

    with io.open(newFile, encoding='utf8') as fileObj:
        a = flatten_json(json.load(fileObj));

    with io.open(oldFile, encoding='utf8') as fileObj:
        b = flatten_json(json.load(fileObj));

    with io.open(diffFile, 'w', encoding = 'utf8') as f:
        for key in [comm for comm in a if not (comm in b)]:
            f.write(key+" : "+a[key]+"\n");


def getFiles(dirPath, ext):
    fileList = [];
    # r=root, d=directories, f = files
    if dirPath[-5:] != ".json":
        for r, d, f in os.walk(dirPath):
            for file in f:
                if file == ext:
                    fileList.append(os.path.join(r, file));
    else:
        fileList.append(dirPath)
    return fileList;

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
    root = tk.Tk()
    root.title("JSON Merger")

    canvas1 = tk.Canvas(root, width=300, height=300)
    canvas1.pack()

    label1 = tk.Label(root, text='NOTE :  There should be two files on same directory: \n1. new.json, which represent latest JSON file.\n2. old.json, which represent old JSON file.', fg='green', font=('helvetica', 8 ))
    canvas1.create_window(150, 100, window=label1)

    button1 = tk.Button(text='Run', command=main, bg='brown', fg='white')
    canvas1.create_window(150, 150, window=button1)

    root.mainloop()

