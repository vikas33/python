from html.parser import HTMLParser
import os
import shutil
import re
import json
import sys

class MyHTMLParser(HTMLParser):

    def handle_data(self, data):
        if data.strip() and "translate" not in data.strip() and "{" not in data.strip() and not(len(data.strip()) == 1) :
            print("Encountered some data  :", data.strip())

parser = MyHTMLParser()



def getFiles(dirPath = "D:\\Codebase\\mphrx-angular\\", ext =".html"):
    fileList = [];
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dirPath):
        for file in f:
            if file[-len(ext):] == ext:
                fileList.append(os.path.join(r, file));
            if ext == '.html' and file[-4:] == '.htm':
                fileList.append(os.path.join(r, file));
    return fileList;

files = getFiles()
for html in files:
    print("\n----------------------------------\nworking for file : "+html)
    fileObj = open(html, "r", encoding = "UTF-8");
    html_doc = fileObj.read()
    parser.feed(html_doc)