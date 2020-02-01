from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
# Create your views here.

import os 

def index(request):
    return render(request,"whatsappmessageanalyzer/base.html")

def new_chat(request):
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage(location="documents/")
        fs.save(uploaded_file.name, uploaded_file)
        data = open_file(uploaded_file.name)
        file_dir = "documents/" + uploaded_file.name
        os.remove(file_dir)
        context = {'data':data}
        return render(request,'whatsappmessageanalyzer/new_chat.html',context)
    else:
        return HttpResponseRedirect(request,"base.html")
    
import re
checklist = []
lastdata = {}
contacts = []

def calc_spammer(lastdata):
    values = list(lastdata.values())
    keys = list(lastdata.keys())
    maxkey = max(values)
    index = values.index(maxkey)
    print(keys[index],"is the spammer in this group with ",values[index],"messages.")

def create_dataset(contacts,checklist):
    for elem in contacts:
        if elem in checklist and elem not in lastdata.keys():
            lastdata[elem]=1
        else:
            lastdata[elem] = lastdata[elem] + 1
    calc_spammer(lastdata)

def create_checklist(contacts):
    for i in range(10):
        for elem in contacts:
            if elem not in checklist:
                checklist.append(elem)
            else:
                pass
    create_dataset(contacts,checklist)

def filter_list(contacts):
    for i in range(3):
        for elem in contacts:
            if ':' in elem:
                contacts.remove(elem)
    create_checklist(contacts)

def flatten_list(contacts):
    contacts = [item for sublist in contacts for item in sublist]
    filter_list(contacts)

def extract_data(string):
    for i in range(len(string)):
        match = re.findall('-(.*):',string[i])
        contacts.append(match)
    flatten_list(contacts)

def open_file(file_name):
    global checklist
    global lastdata
    global contacts
    checklist = []
    lastdata = {}
    contacts = []
    file_dir = "documents/"+file_name
    file = open(file_dir,'r', encoding="utf-8")
    string = file.read()
    string = string.splitlines()
    extract_data(string)
    return lastdata
