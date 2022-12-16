#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
import math
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None
from boq_checker1 import check
#from boq_calc import calculate
from boq_calc import filler
from summary_calc import summarycalc


# In[2]:


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


# In[3]:


def add_method(row):
    if any(substring in row['Remark'] for substring in ["Surprise","surprise","SURPRISE","suprise"]):
        return "Surprise duct"
    elif not pd.isnull(row['Duct_dam_punct_loc_ch_from']) or not pd.isnull(row['Duct_dam_punct_loc_ch_to']):
        return "Damaged"
    elif not pd.isnull(row['Duct_miss_ch_from']) or not pd.isnull(row['Duct_miss_ch_to']):
        return "Missing"
    else:
        return "DRT"


# In[4]:


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


# In[5]:


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


# In[6]:


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


# In[7]:


def common_area(sur_loc,mb_loc,spanid):
    global logs
    sur=survey_data(sur_loc,spanid)
    drt=clean_drt(mb_loc)
    ot=clean_ot(mb_loc)
    hdd=clean_hdd(mb_loc)
    start=-20
    end=20000
    x=0
    y=0
    S=[]
    A=[]
    B=[]
    C=[]
    S = [np.nan for i in range(start,end)]
    A = [np.nan for i in range(start,end)]
    B = [np.nan for i in range(start,end)]
    C = [np.nan for i in range(start,end)]

    df=pd.DataFrame()
    try:
        for i in (sur.index):
            x=y
            y+=int(sur['Route Length'][i])
            if sur['Yes/No'][i]=="Yes":
                for k in range(x,y):
                    S[k]=2  #Blue/ Mission Bhagiratha
            else :
                for k in range(x,y):
                    S[k]=1  #Green Field
    except:
        print("There is no survey file ")
        logs+="Maybe no survey file selected "+"\n"
        
        
    try:
        for i in (drt.index):
            
            if drt['Method'][i]=="Missing":
                for k in range(drt['ch_from'][i],drt['ch_to'][i]):
                    A[k]=4
            elif drt['Method'][i]=="Damaged":
                for k in range(drt['ch_from'][i],drt['ch_to'][i]):
                    A[k]=3
            elif drt['Method'][i]=="DRT":
                for k in range(drt['ch_from'][i],drt['ch_to'][i]):
                    A[k]=2
            elif drt['Method'][i]=="Surprise duct":
                for k in range(drt['ch_from'][i],drt['ch_to'][i]):
                    A[k]=1

    except:
        print("There is no drt:  in common area ",spanid)
        logs+="Maybe no drt file in: "+spanid+"\n"
      
    try:
        for i in (ot.index):
            if ot['Method_Execution'][i]=="OT" or ot['Method_Execution'][i]=="HDD" or ot['Method_Execution'][i]=="Clamping":
                for k in range(ot['Chainage_From'][i],ot['Chainage_To'][i]):
                    B[k]=1
                    
    except:
            print("Problem with OT in common area ",spanid)
            logs+="Maybe no ot file in: "+spanid+"\n"
    #     else :
    #         if ot['Method_Execution'][i]=="DRT":
    #         for k in range(ot['Chainage_From'][i],ot['Chainage_To'][i]):
    #             B[k]=2            

    try:
        for i in (hdd.index):
            if hdd['Method'][i]=="HDD" :
                for k in range(hdd['Chainage_From'][i],hdd['Chainage_To'][i]):
                    C[k]=1
                    
    except:
        print("Problem with HDD in common area ",spanid)
        logs+="Maybe no HDD file in: "+spanid+"\n"
    #     else :
    #         if hdd['Method'][i]=="DRT":
    #         for k in range(drt['Chainage_From'][i],hdd['Chainage_To'][i]):
    #             C[k]=2    

    df['survey']=S  
    df['drt']=A      
    df['ot']=B     
    df['hdd']=C   
    df=df.dropna(how='all')
    return df


# In[8]:


def plot(sur_loc,mb_loc,spanid):
    sur=survey_data(sur_loc,spanid)
    drt=clean_drt(mb_loc)
    ot=clean_ot(mb_loc)
    hdd=clean_hdd(mb_loc)
    fig=plt.figure(figsize=(10,5))
    x=0
    y=0
    
    
    try:
        for i in sur.index: 
            x=y
            y+=int(sur['Route Length'][i])
            if sur['Yes/No'][i]=="Yes":
                plt.hlines(1,x,y,colors='b', linestyles='solid', linewidth=100, label="Mission Bhagiratha")
            else:
                plt.hlines(1,x,y,colors='g', linestyles='solid', linewidth=100, label="Green Field")
    except:
        print("There is no survey file/data ")
        

    try:
        for i in drt.index:
            if drt['Method'][i]=="Missing" or drt['Method'][i]=="Damaged":
                plt.hlines(1.4,drt['ch_from'][i],drt['ch_to'][i],colors='r', linestyles='solid', linewidth=100, label="MB: Missing/Damaged")

            elif drt['Method'][i]=="DRT":
                plt.hlines(1.4,drt['ch_from'][i],drt['ch_to'][i],colors='chocolate', linestyles='solid', linewidth=100, label="MB: DRT")

            elif drt['Method'][i]=="Surprise Duct":
                plt.hlines(1.4,drt['ch_from'][i],drt['ch_to'][i],colors='magenta', linestyles='solid', linewidth=100, label="MB: Surprise Duct")
    except:
        print("There is no drt in plot: ",spanid)
            
    try:
        for i in ot.index:
            if ot['Method_Execution'][i]=="OT" or ot['Method_Execution'][i]=="HDD" or ot['Method_Execution'][i]=="Clamping":
                plt.hlines(1.8,ot['Chainage_From'][i],ot['Chainage_To'][i],colors='darkgreen', linestyles='solid', linewidth=100, label="MB: OT")     
    except:
            print("Problem with OT in plot ",spanid)

    try:   
        for i in hdd.index:
            if hdd['Method'][i]=="OT" or hdd['Method'][i]=="HDD" or hdd['Method'][i]=="Clamping":
                plt.hlines(1.8,hdd['Chainage_From'][i],hdd['Chainage_To'][i],colors='forestgreen', linestyles='solid', linewidth=100, label="MB: HDD")             
    except:
            print("Problem with OT in plot ",spanid)

    plt.title(spanid)
    fig1 = plt.gcf()
    plt.draw()
    plt.show()
    #fig1.savefig('hivro.png', dpi=300)    

    # hdd.shape


# In[9]:


def counter(c,start,end):
    global logs
    count=end-start+1
    if c=='a' and count>10:
        logs+="Case-A: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start )
    elif c=='b' and count>10:
        logs+="Case-B: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start )
        
    elif c=='c' and count>10:
        logs+="Case-C: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start )
        
    elif c=='d' and count>10:
        logs+="Case-D: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start )   
        
    elif c=='e' and count>10:
        logs+="Case-E: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start )   
       
    elif c=='f' and count>10:
        logs+="Case-F: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start )
        
    elif c=='g' and count>10:
        logs+="Case-G: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start ) 
        
    elif c=='h' and count>10:
        logs+="Case-H: Error in chainge from "+str(start)+" to "+str(end)+".\n"
#         print("count>=4 is ", count,start ) 
        
    else:
        pass
            
        


# In[10]:


#case='aaaaaaaaaaappppppppppppppppppppaa'


# In[11]:


####Add something to case at last:::::
def sound(case):
    start=''
    count=0
    i=0
    while i<len(case)-1:
        start_pos=i
        for j in range(i+1,len(case)):
            if case[start_pos]==case[j]:
                count+=1
                i+=1
            else:
                counter(case[start_pos],start_pos,j-1)
                count=0
                i=j
                break


# In[12]:


def check_errors(df):
    #errors=0
    case=""
    count=0
    for i in df.index:
        #Survey ➤ Green  &   DRT ➤ NAN                &          OT/HDD ➤ NAN
        if df['survey'][i]==1 and pd.isnull(df['drt'][i]) and ( (pd.isnull(df['hdd'][i]) and pd.isnull(df['ot'][i]))):
            case+='a'
        #Survey ➤ Green  &   DRT ➤ Miss/Dam 
        elif (df['survey'][i]==1) and (df['drt'][i]>=3):
            case+='b'
        #Survey ➤ Green  &   DRT ➤ Proper DRT 
        elif df['survey'][i]==1 and  df['drt'][i]==2:
            case+='c'
        #Survey ➤ Blue     &   DRT ➤ NAN                &         OT/HDD ➤ NAN 
        elif df['survey'][i]==2 and  pd.isnull(df['drt'][i]) and ( (pd.isnull(df['hdd'][i]) and pd.isnull(df['ot'][i]))):
            case+='d'
        #Survey ➤ Blue     &   DRT ➤ Miss/Dam        &         OT/HDD ➤ NAN 
        elif df['survey'][i]==2 and df['drt'][i]>=3 and ( (pd.isnull(df['hdd'][i]) and pd.isnull(df['ot'][i]))):
               case+='e'    
        #Survey ➤ Blue     &   DRT ➤ Proper DRT     &         OT/HDD ➤ 1
        elif df['survey'][i]==2 and df['drt'][i]==2 and (df['hdd'][i]==1 or df['ot'][i]==1):
            case+='f'
        #Survey ➤ Blue     &   DRT ➤ Sup. Duct 
        elif df['survey'][i]==2 and df['drt'][i]==1:
            case+='g'   
        #Survey ➤ NAN     &   DRT ➤ Not NAN        OR       OT/HDD ➤ Not NAN 
        elif pd.isnull(df['survey'][i]) and ((not pd.isnull(df['drt'][i])) or (not pd.isnull(df['ot'][i])) or (not pd.isnull(df['hdd'][i]))):
            case+='h'
            
        else:
            case+='p'
            pass
    
    return case    
        


# In[13]:


def check_errorsmb(df):
    case=""
    count=0
    for i in df.index:
        #OT and HDD
        if not( pd.isnull(df['hdd'][i]) or ( pd.isnull(df['ot'][i]))):
            case+='a'
            
        #Miss+Dam    
        elif (df['drt'][i]==3) and (df['drt'][i]==4):
            case+='b'
         
        #Miss+Sup
        elif df['drt'][i]==3 and  df['drt'][i]==1:
            case+='c'
        
        #Miss and no ot/hdd
        elif df['drt'][i]==3 and  ( (pd.isnull(df['hdd'][i]) and pd.isnull(df['ot'][i]))):
            case+='d'
         
        #Dam and no ot/hdd
        elif df['drt'][i]==4 and  ( (pd.isnull(df['hdd'][i]) and pd.isnull(df['ot'][i]))):
            case+='e'   
        
        #Proper drt and ot/hdd
        elif df['drt'][i]==2 and  not( (pd.isnull(df['hdd'][i]) and pd.isnull(df['ot'][i]))):
            case+='f'
        
        #sup+ot/hdd
        elif df['drt'][i]==1 and  not( (pd.isnull(df['hdd'][i]) and pd.isnull(df['ot'][i]))):
            case+='g'
            
        #Repeat case    
        elif (df['drt'][i]==4) and (df['drt'][i]==3):
            case+='h'
            
        else:
            case+='p'
            pass
    
    return case   


# In[14]:


def called_final(sur_loc,file1):
    #print(file1)
    global logs
    case=""
    df=pd.read_excel(sur_loc,sheet_name='3.OFC UG Survey Report',skiprows=6)
    span_list=df['SPAN ID'].unique()
    logs+="Survey contains folowing spans:"+"\n"+str(df['SPAN ID'].unique())+"\n"
    #plot(sur_loc,mb_loc)
    term=0
    for i in span_list:
        logs+="Checking for span ID:"+str(i)+"\n"
        mandal_file=file1
        for j in os.listdir(file1):
#             print(j)
            case=""
            span_loc=os.path.join(file1,j)
#             print(str(i)," in ",j)
            if str(i) in j:
                term+=1
                logs+="""\n✅✅✅✅✅✅✅✅✅✅✅✅✅✅   Found!!!"""+"\n"+"Comaparing between:"+str(i)+" & "+str(j)+":::::::\n"
                try:
                    df=common_area(sur_loc,span_loc,str(i))
#                     df.to_excel('final_df.xlsx')
                    case+=check_errors(df)
                    case+='Z'
                    #print(case)
                    sound(case)
                    plot(sur_loc,span_loc,str(i))
                except:
                    logs+="Not able to call common_area funtion. Terminated comparison for "+str(i)+". Report Format error."
                logs+="\n--------------------------------------------------------------------------------------\n"
                break

        if term==0:
            logs+="No match for this Span-ID: "+str(i)+" in "+"Mandal Folder"+"\n"
            logs+="\n--------------------------------------------------------------------------------------\n"

        term=0

    return logs
#check(df)


# In[15]:


def called_mb(file1):
    global logs
    case=""
    for j in os.listdir(file1):
            span_loc=os.path.join(file1,j)
            print(span_loc)
#             try:
            case=""
            df1=common_area("sur_loc",span_loc,j[:-5])
            logs+="DF successfully generated in "+j[:-5]+"\n"
#             df1.to_excel('mb_final_df.xlsx')
            case+=check_errorsmb(df1)
            case+='Z'
            #print(case)
            sound(case)
            plot("sur_loc",span_loc,j[:-5])
#             except:
#                 logs+="Not able to call common_area funtion. Terminated comparison for "+j+". Report Format error."
            logs+="\n--------------------------------------------------------------------------------------\n"
    return logs       


# In[16]:


def boq_checkup():
    global logs
    logs= logs + "Called BoQ Checkup Function "  + "\n"
    top= Toplevel(popupRoot)
    top.geometry("980x550")
    l = Label(top, text = "Here is a list of Errors!!")
    l.config(font =("Courier", 14))
    b2 = Button(top, text = "Exit",command = top.destroy)
    top.title("Error Check-up Window")
    text_box = Text(top,height=50,width=200)
    text_box.pack(expand=True)



    
    try:
        temp_logs=''
        superstring,temp_logs=check(file_mandal)
        logs= logs + temp_logs  + "\n" 
    except:
        logs= logs + "Red Flag: Could not complete BoQ Checker Function. Issues Found!!"  + "\n" 
        superstring="Not able to do a BoQ Checkup on given Mandal!!"   
    
    text_box.insert('end', superstring)
    text_box.config(state='disabled')
    l.pack()
    b2.pack()
    logs= logs + "Work in BoQ Checkup function done. Closed! "  + "\n"


# In[19]:


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


popuplabel = Label(popupRoot, text = 'BoQer Checker V2',font = ("Times New Roman", 13)).grid(row=0,column=2)
popupButton = Label(popupRoot, text = 'STL',bg='white',fg='blue',font = ("Times New Roman", 15,'bold'), anchor="e",justify=RIGHT).grid(row=0,column=3)
popuplabel = Label(popupRoot, text = ' ',font = ("Times New Roman", 12)).grid(row=1,column=1)
popuplabel = Label(popupRoot, text = 'Select the Survey file',font = ("Times New Roman", 12)).grid(row=2,column=1)
popupButton = Button(popupRoot, text = 'Survey File', font = ("Times New Roman", 12), command = boq_format,width = 15).grid(row=2,column=2)
popuplabel = Label(popupRoot, font = ("Times New Roman", 12),text = 'Select Mandal Folder').grid(row=3,column=1)
popupButton = Button(popupRoot, text = 'Mandal Folder', font = ("Times New Roman", 12), command = mandal_folder,width = 15).grid(row=3,column=2)
popuplabel = Label(popupRoot, text = ' ',font = ("Times New Roman", 12)).grid(row=4,column=1)
popupButton = Button(popupRoot, text = 'Sur-MB mismatch', bg='orange',font = ("Times New Roman", 12), command = called_A,width = 15).grid(row=5,column=2)
popupButton = Button(popupRoot, text = 'MB mismatch', bg='light blue',font = ("Times New Roman", 12), command = called_B,width = 15).grid(row=5,column=1)
popupButton = Button(popupRoot, text = 'C', bg='#00FF00',font = ("Times New Roman", 12), command = boq_checkup,width = 3).grid(row=3,column=3)
popupButton = Button(popupRoot, text = 'X', bg='#f70d1a',font = ("Times New Roman", 12), command = called_C,width = 3).grid(row=5,column=3)

popupRoot.geometry('390x200')
mainloop()


# In[18]:


errors


# In[ ]:




