import os
import re
#from master_maps import triggerNameMapping;
triggerNameMapping = {
    "Appointment_CREATE_PrescriptionUpload_ReminderNotification.groovy" :"AppointmentManagement_PrescriptionUploadReminder_Appointment_CREATE.groovy",
}

filePath = "D:\\testingFolder"
entryFile = "D:\\testingFolder\\Entries.txt"


def main():
    print("**************  SCRIPT START ************");
    print("Size of triggerNameMapping : ", len(triggerNameMapping));
    print("File Path : ",filePath);

    for key, value in triggerNameMapping.items():
        replaceSubStringInFileName(key, value, True)


def createEntryInFile(file, triggerName):
    print("Opening File : ", file);
    triggerType = ""
    isEnabled = ""
    resource = ""
    description = ""

    with open(filePath+"\\"+file) as f:
        datafile = f.readlines()
        for line in datafile:
            lineInLower = line.strip().lower()
            if lineInLower.startswith("resource :"):
                pattern = re.compile("resource :", re.IGNORECASE)
                resource = pattern.sub("",line).strip()
            elif lineInLower.startswith("type :"):
                pattern = re.compile("type :", re.IGNORECASE)
                triggerType = pattern.sub("", line).strip()
            elif lineInLower.startswith("trigger enabled status :"):
                pattern = re.compile("trigger enabled status :", re.IGNORECASE)
                isEnabled = pattern.sub("", line).strip()
            elif lineInLower.startswith("description :"):
                pattern = re.compile("description :", re.IGNORECASE)
                description = pattern.sub("", line).strip()

    triggerName = triggerName.replace(".groovy","");
    triggerType = triggerName.split("_")[-1] if not triggerType else triggerType.upper();
    isEnabled = isEnabled.lower();
    resource = triggerName.split("_")[-2] if not resource else resource[0].upper()+resource[1:];

    textToWrite = triggerName +" | "+ resource +" | "+ triggerType +" | "+ isEnabled +" | "+ "Action_"+triggerName+".groovy" +" | "+ "Condition_"+triggerName+".groovy" +" | "+ description+"\n"
    with open(entryFile, "a") as f:
        f.write(textToWrite)

def replaceSubStringInFileName(search, replace, createEntry = False):
    counter = 0;
    for file in os.listdir(filePath):
        if file.endswith(".groovy"):
            if file.find(search) > 0:
                counter += 1
                print("\nOld name:" + file)
                newFileName = file.replace(search, replace)
                os.rename(os.path.join(filePath, file), os.path.join(filePath, newFileName))
                print("New name:" + newFileName)
                if createEntry and newFileName.startswith("Condition_"):
                    createEntryInFile(newFileName, replace)
    if counter == 0:
        print("NO_FILE_FOUND\n\n")






if __name__ == '__main__':
    main()