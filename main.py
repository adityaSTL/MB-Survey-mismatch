#Importing all the libraries
from tkinter import *
from tkinter import filedialog
from sys import exit
import pandas as pd
import numpy as np
import os
from extract import Extract
from create_table1 import Create_table
import openpyxl
import matplotlib.pyplot as plt
from openpyxl_image_loader import SheetImageLoader
import os
import os.path
import warnings
from array import *
from mb_check import *
from sur_mb_check import *
from plot_func import *
import math
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None





def survey_data(survey_loc,spanid):
    try:
        df=pd.read_excel(survey_loc,sheet_name='3.OFC UG Survey Report',skiprows=6)
        df1=df.loc[df['SPAN ID']==spanid]
        df1.reset_index(inplace=True)
        sur=df1[['SPAN ID','Route Length','Yes/No']]
    except:
        sur=[]
        print("No survey file")
        
    return sur
    
#     sur.head(15)

def add_method(row):
    if any(substring in row['Remark'] for substring in ["Surprise","surprise","SURPRISE","suprise"]):
        return "Surprise duct"
    elif not pd.isnull(row['Duct_dam_punct_loc_ch_from']) or not pd.isnull(row['Duct_dam_punct_loc_ch_to']):
        return "Damaged"
    elif not pd.isnull(row['Duct_miss_ch_from']) or not pd.isnull(row['Duct_miss_ch_to']):
        return "Missing"
    else:
        return "DRT"

def clean_drt(mb_loc):
    drt=Extract.extract_drt(mb_loc)
    if len(drt)!=0:
        drt=Create_table.create_drt(drt)
        drt.reset_index(drop=True,inplace=True)
        drt = drt.dropna(subset=['ch_from'])
        drt.reset_index(drop=True,inplace=True)
        try:
            drt['Method']= drt.apply(add_method, axis=1)
            drt=drt[['ch_from','ch_to','Method','Remark']]
        except:
                drt=drt[['ch_from','ch_to','Remark']]
    return drt

def clean_ot(mb_loc):
    #Getting drt mb report
    ot=Extract.extract_ot(mb_loc)
    if len(ot)!=0:
        ot=Create_table.create_ot(ot)
        ot.reset_index(drop=True,inplace=True)
        ot = ot.dropna(subset=['Chainage_From'])
        ot.reset_index(drop=True,inplace=True)
        #ot['Method']= ot.apply(add_method, axis=1)
        ot=ot[['Chainage_From','Chainage_To','Method_Execution','Remark']]
#         print(ot.head())
        return ot

def clean_hdd(mb_loc):
    #Getting drt mb report
    hdd=Extract.extract_hdd(mb_loc)
    if len(hdd)!=0:
        hdd=Create_table.create_hdd(hdd)
        hdd.reset_index(drop=True,inplace=True)
        hdd = hdd.dropna(subset=['Chainage_From'])
        hdd.reset_index(drop=True,inplace=True)
        hdd['Method']= "HDD"
        hdd=hdd[['Chainage_From','Chainage_To','Method','Remark']]
#         print(hdd.head())
        return hdd











global errors,threshold1,threshold2,logs,temp_logs,temp_logs2
global spans
spans=[]
errors=0
threshold1=5
threshold2=50
logs=""
temp_logs=""
temp_logs2=""

file_format=""
file_mandal=""

logs= logs+"Starting"+"\n"
popupRoot = Tk()
#popupRoot2 = Tk()
popupRoot.title('BoQ Generator A')    


def boq_format():
    global file_format
    t=filedialog.askopenfilename(initialdir="C:/")
    file_format=file_format+t
    #global logs
    #logs= logs+ "Captured BoQ Format Folder " + file_format + "\n"

def mandal_folder(): 
    global file_mandal   
    t=filedialog.askdirectory()
    file_mandal=file_mandal+t
    #global logs
    #logs= logs + "Captured BoQ Mandal Folder " + file_mandal + "\n"


def called_A():
    global logs,temp_logs
    logs=""
    logs+="Different Cases:\n"+"Case-1:Survey=>MB Section, DRT MB=>Only Drt(No missing/damaged), Error=>OT/HDD Found \nCase-2:Survey=>MB Section, DRT MB=>Found surprise  \nCase-3:Survey=>Green Field, DRT MB=> Miss/Dam case found\n"
    top= Toplevel(popupRoot)
    top.geometry("1000x600")
    l = Label(top, text = "Here is a list of Errors!!")
    l.config(font =("Courier", 14))
    b2 = Button(top, text = "Exit",command = top.destroy)
    top.title("Error Check-up Window")
    text_box = Text(top,height=50,width=200)
    text_box.pack(expand=True)
    print(file_format,file_mandal)
#     try:
    temp_logs+=called_final(file_format,file_mandal)    
    text_box.insert('end', temp_logs)
#     except:
#         temp_logs+="\nNot able to run fully. Report error."
#         text_box.insert('end', temp_logs)
        
    text_box.config(state='disabled')
    l.pack()
    b2.pack()
    #logs= logs + "Work in BoQ Checkup function done. Closed! "  + "\n"
    #popupRoot.destroy()

def called_B():
    global logs,temp_logs2
    logs=""
    #logs+="Different Cases:\n"+"Case-1:Survey=>MB Section, DRT MB=>Only Drt(No missing/damaged), Error=>OT/HDD Found \nCase-2:Survey=>MB Section, DRT MB=>Found surprise  \nCase-3:Survey=>Green Field, DRT MB=> Miss/Dam case found\n"
    top= Toplevel(popupRoot)
    top.geometry("1000x600")
    l = Label(top, text = "Here is a list of Errors!!")
    l.config(font =("Courier", 14))
    b2 = Button(top, text = "Exit",command = top.destroy)
    top.title("Error Check-up Window")
    text_box = Text(top,height=50,width=200)
    text_box.pack(expand=True)
    print(file_format,file_mandal)
#     try:
    temp_logs2+=str(called_mb(file_mandal))    
    text_box.insert('end', temp_logs2)
#     except:
#         temp_logs+="\nNot able to run fully. Report error."
#         text_box.insert('end', temp_logs)
        
    text_box.config(state='disabled')
    l.pack()
    b2.pack()

#     popupRoot.destroy()
def called_C():
    popupRoot.destroy()


popuplabel = Label(popupRoot, text = 'BoQer Checker V2',font = ("Times New Roman", 11)).grid(row=0,column=2)
popupButton = Label(popupRoot, text = 'STL',bg='white',fg='blue',font = ("Times New Roman", 13,'bold'), anchor="e",justify=RIGHT).grid(row=0,column=3)
popuplabel = Label(popupRoot, text = ' ',font = ("Times New Roman", 12)).grid(row=1,column=1)
popuplabel = Label(popupRoot, text = 'Select the Survey file',font = ("Times New Roman", 12)).grid(row=2,column=1)
popupButton = Button(popupRoot, text = 'Survey File', font = ("Times New Roman", 12), command = boq_format,width = 20).grid(row=2,column=2)
popuplabel = Label(popupRoot, font = ("Times New Roman", 12),text = 'Select Mandal Folder').grid(row=3,column=1)
popupButton = Button(popupRoot, text = 'Mandal Folder', font = ("Times New Roman", 12), command = mandal_folder,width = 20).grid(row=3,column=2)
popuplabel = Label(popupRoot, text = ' ',font = ("Times New Roman", 12)).grid(row=4,column=1)
popupButton = Button(popupRoot, text = 'Sur-MB mismatch', bg='orange',font = ("Times New Roman", 15), command = called_A,width = 15).grid(row=5,column=2)
popupButton = Button(popupRoot, text = 'MB mismatch', bg='light blue',font = ("Times New Roman", 15), command = called_B,width = 12).grid(row=5,column=1)
popupButton = Button(popupRoot, text = 'X', bg='#f70d1a',font = ("Times New Roman", 12), command = called_C,width = 3).grid(row=5,column=3)

popupRoot.geometry('390x200')
mainloop()