#Importing all the libraries
from tkinter import *
from sys import exit
from tkinter import filedialog
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
import tkinter
import warnings
from array import *
import math
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None


def check(file1):
    counter=0
    superstring=""
    logs='Starting Checkup'+'\n'

    #Case 1: Check for already present BoQ File
    logs= logs+ "BoQ excel checking if present"  + "\n"
    mandal_file=file1+'/'
    if os.path.exists(mandal_file+"BOQ122.xlsx"):
        counter+=1
        superstring=superstring+str(counter)+". Remove the already present BoQ122.xlsx file in Mandal Folder"+"\n"

    os.chdir(mandal_file)

    for info in os.listdir():

        j=mandal_file+info
        
        ###Summary checkup
        summary=[]
        try:
            summary=pd.read_excel(j,sheet_name='Summary')
        
        except:
            if len(summary)==0:
                counter+=1
                superstring = superstring+str(counter)+". No Summary sheet found. Please make summary sheet in "+info+"\n"

        ###Missing Chainages Checkup
        missing_chainages=[]
        try:
            missing_chainages=pd.read_excel(j,sheet_name='Missing Chainages')

        except:   
            if len(missing_chainages)==0:
                counter+=1
                superstring = superstring+str(counter)+". No Missing Chainages sheet found. Please make the sheet in "+info+"\n"


        try:
            ot=Extract.extract_ot(j)
            if len(ot.columns)!=18:
                counter+=1
                superstring = superstring+str(counter)+" .Number of columns is different (Duplicate/Extra Columns found) in OT MB of "+info+". Count of columns is "+str(len(ot.columns))+"\n"
                
        except:
            counter+=1
            superstring=superstring+str(counter)+". No OT MB captured in "+info+""". Standard names are "OT","R4_OT","OT MB","R04_T&D"."""+"\n"


        try:
            blo=Extract.extract_blo(j)
            if len(blo.columns)!=18 and len(blo.columns)!=17:
                #print("Working1")
                counter+=1
                superstring = superstring+str(counter)+""". Number of columns is different (Duplicate/Extra Columns found) in Blowing MB of """+info+""". Count of columns is """+str(len(blo.columns))+"\n"
                #print(tem)
        except:
            counter+=1
            superstring=superstring+str(counter)+". No Blowing MB captured in "+info+""". Standard names are "BLOWING","blowing","R10_BLOWING","R10_Blowing"."""+"\n"
        
        try:
            drt=Extract.extract_drt(j)
            j=0
            columns_={}
            for i in drt.columns:
                if j==0:
                    columns_[i]='S_no'
                elif j==1:
                    columns_[i]='Ch1_lat'
                elif j==2:
                    columns_[i]='Ch1_long'
                elif j==3:
                    columns_[i]='Ch1_cond'
                elif j==4:
                    columns_[i]='Ch1_route_marker'
                elif j==5:
                    columns_[i]='Ch2_lat'
                elif j==6:
                    columns_[i]='Ch2_long'
                elif j==7:
                    columns_[i]='Ch2_cond'
                elif j==8:
                    columns_[i]='Ch2_route_marker'
                elif j==9:
                    columns_[i]='Ch_from'
                elif j==10:
                    columns_[i]='Ch_to'
                elif j==11:
                    columns_[i]='Len'
                elif j==12:
                    columns_[i]='Duct_dam_lat'
                elif j==13:
                    columns_[i]='Duct_dam_long'
                elif j==14:
                    columns_[i]='Duct_dam_ch_from'
                elif j==15:
                    columns_[i]='Duct_dam_ch_to'
                elif j==16:
                    columns_[i]='Duct_dam_len'
                elif j==17:
                    columns_[i]='Duct_miss_lat'
                elif j==18:
                    columns_[i]='Duct_miss_long'
                elif j==19:
                    columns_[i]='Duct_miss_ch_from'
                elif j==20:
                    columns_[i]='Duct_miss_ch_to'
                elif j==21:
                    columns_[i]='Duct_miss_len'
                elif j==22:
                    columns_[i]='Remark'
                j+=1
            drt.rename(columns=columns_,inplace=True)
            drt.reset_index(drop=True,inplace=True)
            for i in range(len(drt)):
                if type(drt.loc[i,'Duct_dam_ch_from'])==int and type(drt.loc[i,'Duct_dam_ch_to'])==int and type(drt.loc[i,'Ch_from'])==int and type(drt.loc[i,'Ch_to'])==int:
                    if drt.loc[i,'Duct_dam_ch_from']!=drt.loc[i,'Ch_from'] and drt.loc[i,'Duct_dam_ch_to']!=drt.loc[i,'Ch_to']:
                        counter+=1
                        superstring=superstring+str(counter)+". Please correct chainage error in DRT MB of "+info+"\n"

            for i in range(len(drt)):
                if type(drt.loc[i,'Duct_miss_ch_from'])==int and type(drt.loc[i,'Duct_miss_ch_to'])==int and type(drt.loc[i,'Ch_from'])==int and type(drt.loc[i,'Ch_to'])==int:
                    if drt.loc[i,'Duct_miss_ch_from']!=drt.loc[i,'Ch_from'] and drt.loc[i,'Duct_miss_ch_to']!=drt.loc[i,'Ch_to']:
                        counter+=1
                        superstring=superstring+str(counter)+". Please correct chainage error in DRT MB of "+info+"\n"


            if len(drt.columns)!=23:
                #print("Working2")
                counter+=1
                superstring = superstring+str(counter)+". Number of columns is different (Duplicate/Extra Columns found) in DRT MB of "+info+". Count of columns is "+str(len(drt.columns))+"\n"
                
        except:
            counter+=1
            superstring=superstring+str(counter)+". No DRT MB captured in "+info+""". Standard names are "DRT","R09_DRT","R09-DRT","R9_DRT"."""+"\n"
        
        

    return superstring,logs