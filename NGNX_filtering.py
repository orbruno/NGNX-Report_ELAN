import csv
import pandas as pd
import hashlib

# function that encodes a string line into MD5
def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()

# function that splits line into items of the CSV
def line_separation (self):
    """function that splits line of a NGNX access type log into items of the CSV, takes in the line in form of a list and outputs anoter list of the fields"""
    #this list will temporary keep the row
    row=[]
    #this str var will temporary keep the word that will be appended to the temporary row[] variable
    value = ""

    #Boolean values to check wheater or not anoter space starts
    openbracket=False
    openstring=False
    separator=True
    ip=0
    #Preparation of the fields by separating the string to fields in the dataframe, in each if are the different marks to know when a new field starts
    for x in range(len(self)):
        #as per the nginx access logs this dates will be contain in brackets which will indicate when
        if self[x] == ".":
            ip = ip + 1
        if self[x] == "[":
            openbracket=True
        if self[x] == "]":
            openbracket=False
        if self[x] == '"' and openstring==False:
            openstring=True
        elif self[x] == '"' and openstring==True:
            openstring=False
        if self[x] == " " and openbracket==False and openstring==False:
            if ip==3:
                value=computeMD5hash(value)
                ip=ip+1
            if value == "-" and separator==False:
                row.append(value)
                separator=True
                value=""
            elif value!="-":
                row.append(value)
                value=""
            elif value=="\\n":
                row.append(value)
                value=""
        #This will tidy special characters
        if x==1:
            value=value+self[x]
        if self[x] != " " and self[x] != '[' and self[x] != ']' and openbracket==False and self[x] != "\\n" and x !=len(self[x]):
            value=value+self[x]
        elif self[x] != '[' and self[x] != ']' and openbracket==True and self[x] != "\\n" and x !=len(self[x]) :
            value=value+self[x]
    row.append(value)
    return row


def convert_to_csv(log_file):
    """Converts NGNX log type access file into CSV, IP address are MD5 encoded"""
    #Reads log file
    with open(log_file) as f:
        f = f.readlines()

    #Creates a list type var from the file
    log_list = []
    for line in f:
        log_list.append(line)

    #Creates a new csv fields with the required colums as per specifications
    with open('log.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['remote_addr', 'remote_user','time_local', 'request','status', 'body_bytes_sent','http_referer','http_user_agent','extra'])

    #Separates lines into fields using the line_separation function and writes the lines into the log
    for x in range(len(log_list)):
        # splits a word into character into the line_separation function and return a list of the lines
        row=line_separation(list(log_list[x]))
        with open('log.csv', 'a', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(row)

def filter_requests(csv_file):
    """Filters a CSV created with the convert_to_csv function leaving only the first requests in the form ffmpeg.*.rpm or ffmpeg.*.deb per each host """
    #filters dataframe leaving only the requests in the form ffmpeg.*.rpm or ffmpeg.*.deb
    df=pd.read_csv(csv_file)
    df = df[(df['request'].str.contains('ffmpeg')==True)]
    df=df[((df['request'].str.contains('.debH')==True)| (df['request'].str.contains('.rpmH')))]

    #filters the first request from each unique address
    df = df.groupby(['remote_addr'], sort=False,).first()

    #saves results to a csv
    df.to_csv('ffmpeg_downloads.csv', mode='a')
    print("number of hosts with a request in the form ffmpeg.*.rpm or ffmpeg.*.deb: ",df['request'].count())
