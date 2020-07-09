#!/usr/bin/python

# NEED VARIABLES FROM EXTERNAL SHELL SCRIPT

import os
from datetime import datetime, timedelta
import MySQLdb
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


def main():
    filename = exportRecords();
    sendmail(filename);


def exportRecords():

    print("GOING_EXPORTED_RECORDS\n");
    conn = MySQLdb.Connection(host = os.environ['MYSQL_HOST'], port = int(os.environ['MYSQL_PORT']), user = os.environ['MYSQL_USER'], passwd = os.environ['MYSQL_PASSWD'], db = os.environ['MYSQL_DB']);
    filePath = os.environ['OUTPUT_PATH'];
    fileName = os.environ['FILE_NAME']+"_";
    tableName = os.environ['MYSQL_TABLE']

    if not os.path.exists(filePath):
        os.makedirs(filePath);
        os.chmod(filePath,777)


    startDate = datetime.strftime(datetime.now(), '%Y-%m-%d 00:00:00');
    endDate = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d 00:00:00');
    date = datetime.strftime(datetime.now(), '%Y%m%d');
    filePath = filePath+fileName+date+".csv";

    if os.path.exists(filePath):
        os.remove(filePath);

    print("Going to extract metric report from date %s to %s into file %s."%(startDate,endDate,filePath));

    cursor = conn.cursor()
    sql0 = "SELECT * FROM "+tableName+" WHERE createdDateTime>='"+startDate+"' AND createdDateTime<'"+endDate+"' INTO OUTFILE '" + filePath + "'  FIELDS ENCLOSED BY ''  TERMINATED BY ','  ESCAPED BY '\"'  LINES TERMINATED BY '\r\n';"
    cursor.execute(sql0)
    conn.close();

    line_prepender(filePath,"id,action,criteria,device,gender,ageGroup,transactionTimeOfDay,metricsTimeOfDay,isReturnedPatient,rowCreatedDateTime,transactionDate,previousMetricsDate,metricsDate,location,userGroup,specialty,transactionStatus,paymentMethod,totalAmount,count");

    print("SUCCESSFULLY_EXPORTED_RECORDS\n");
    return filePath;

def sendmail(fileName):

    print("GOING_TO_SEND_MAIL\n");

    emailfrom = os.environ['MAIL_FROM'];
    emailto = (os.environ['MAIL_TO']).split(',');
    fileToSend = fileName
    username = os.environ['SMTP_USER'];
    password = os.environ['SMTP_PASSWD'];
    smtphost = os.environ['SMTP_HOST']

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ", ".join(emailto)
    msg["Subject"] = "PEP || Metrics Daily Report";
    body = """\
        <html>
        <head></head>
        <body>
        <p>Hi,<br><br>
           Please find attached Metric Report for date : <b><span style="background-color:yellow;"> %s </span></b>
         <br>
         <br>  
        </p>
        Thanks and Regards,<br><br>
        <b>MphRx </b><br>
        Breaking Barriers in Healthcare
        </body>
        </html>
        """ % (datetime.strftime(datetime.now(), '%Y-%m-%d'))

    msg.attach( MIMEText(body, 'html'));

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1);
    attachment = MIMEBase(maintype, subtype)
    if fileToSend[-4:] == ".csv":
        fp = open(fileToSend, "rb")
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    else:
        print("ERROR : File doesn't belong to MIMEBase.");

    attachment.add_header("Content-Disposition", "attachment", filename=fileName.split('/')[-1])
    msg.attach(attachment)

    server = smtplib.SMTP(smtphost)
    server.starttls()
    server.login(username, password)
    print("Going to send mail from : %s, to : %s" % (str(emailfrom), str(emailto)));
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()

    print("SUCCESSFULLY_SENT_MAIL\n");

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        content = content.replace('\"N',"NULL")
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

if __name__ =="__main__":
    main()




# export MYSQL_HOST='127.0.0.1'
# export MYSQL_PORT=3307
# export MYSQL_USER='root'
# export MYSQL_PASSWD='password'
# export MYSQL_DB='mirth_testdb'
# export MYSQL_TABLE='testTable'
# export OUTPUT_PATH='/tmp/metricReport/'
# export FILE_NAME='metricReport'
# export MAIL_TO='vsamota@mphrx.com'
# export MAIL_FROM='servicedesk@mphrx.com'
# export SMTP_USER='servicedesk@mphrx.com'
# export SMTP_PASSWD='MphRx@2011'
# export SMTP_HOST='smtp.office365.com:587'


