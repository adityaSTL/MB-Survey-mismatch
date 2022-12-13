import pandas as pd
from tkinter import messagebox
import openpyxl

class Extract:


    
    def extract_ot(path):
        ot=[]
        try:

            ot=pd.read_excel(path,sheet_name='R4_OT')
            ot.dropna(how='all', inplace=True,axis=0)
            ot.dropna(how='all', inplace=True,axis=1)
        except:
            print('No file R4_OT1')
        
        if len(ot)==0:
            try:
                ot=pd.read_excel(path,sheet_name='OT')
                ot.dropna(how='all', inplace=True,axis=0)
                ot.dropna(how='all', inplace=True,axis=1)
                #ot.to_csv('ot12223.csv')
            except:
                print('No file R4_OT2')
        
        if len(ot)==0:
            try:
                ot=pd.read_excel(path,sheet_name='OT MB')
                ot.dropna(how='all', inplace=True,axis=0)
                ot.dropna(how='all', inplace=True,axis=1)
            except:
                print('No file R4_OT3')
        
        if len(ot)==0:
            try:
                ot=pd.read_excel(path,sheet_name='R04_T&D')
                ot.dropna(how='all', inplace=True,axis=0)
                ot.dropna(how='all', inplace=True,axis=1)
            except:
                #messagebox.showerror("Extract Error", "Sheet name should be 'OT' "+path)
                print('No file R4_OT4')

        
        return ot

    def extract_hdd(path):
        hdd=[]
        try:
            hdd=pd.read_excel(path,sheet_name='R8_HDD')
            hdd.dropna(how='all', inplace=True,axis=0)
            hdd.dropna(how='all', inplace=True,axis=1)
        except:
            print('No file R8_HDD1')
        
        if len(hdd)==0:
            try:
                hdd=pd.read_excel(path,sheet_name='HDD')
                hdd.dropna(how='all', inplace=True,axis=0)
                hdd.dropna(how='all', inplace=True,axis=1)
            except:
                print('No file HDD2')
        
        if len(hdd)==0:
            try:
                hdd=pd.read_excel(path,sheet_name='R08_HDD')
                hdd.dropna(how='all', inplace=True,axis=0)
                hdd.dropna(how='all', inplace=True,axis=1)
            except:
                #messagebox.showerror("Extract Error", "Sheet name should be 'HDD' "+path)
                print('No file R4_OT3')
        
        
        return hdd    
    
    def extract_drt(path):
        drt=[]
        try:
            drt=pd.read_excel(path,sheet_name='R9_DRT')
            drt.dropna(how='all', inplace=True,axis=0)
            drt.dropna(how='all', inplace=True,axis=1)
        except:
            print('No file R9_DRT1')
        
        if len(drt)==0:
            try:
                drt=pd.read_excel(path,sheet_name='DRT')
                drt.dropna(how='all', inplace=True,axis=0)
                drt.dropna(how='all', inplace=True,axis=1)
            except:
                print('No file DRT2')
        
        if len(drt)==0:
            try:
                drt=pd.read_excel(path,sheet_name='R09_DRT')
                drt.dropna(how='all', inplace=True,axis=0)
                drt.dropna(how='all', inplace=True,axis=1)
            except:
                print('No file R9_DRT3')
        
        if len(drt)==0:
            try:
                drt=pd.read_excel(path,sheet_name='R09-DRT ')
                drt.dropna(how='all', inplace=True,axis=0)
                drt.dropna(how='all', inplace=True,axis=1)
            except:
                #messagebox.showerror("Extract Error", "Sheet name should be 'DRT' "+path)
                print('No file R9_DRT4')
        
        
        return drt    

    def extract_blo(path):
        blo=[]
        try:
            blo=pd.read_excel(path,sheet_name='R10_Blowing')
            blo.dropna(how='all', inplace=True,axis=0)
            blo.dropna(how='all', inplace=True,axis=1)
        except:
            print('No file R10_Blowing1')
        
        if len(blo)==0:
            try:
                xfile = openpyxl.load_workbook(path, data_only=True)
                sheet1=xfile['BLOWING']
                data = sheet1.values
                blo = pd.DataFrame(data)
                #blo=pd.read_excel(path,sheet_name='BLOWING')
                blo.dropna(how='all', inplace=True,axis=0)
                blo.dropna(how='all', inplace=True,axis=1)
            except:
                print('No file BLOWING2')
        
        if len(blo)==0:
            try:
                #print("1")
                blo=pd.read_excel(path,sheet_name='Blowing')
                print("2")
                blo.dropna(how='all', inplace=True,axis=0)
                print("3")
                blo.dropna(how='all', inplace=True,axis=1)
                print("4")
                #print("Print blo",blo)
            except:
                print('No file Blowing3')

        if len(blo)==0:
            try:
                blo=pd.read_excel(path,sheet_name='R10_BLOWING')
                blo.dropna(how='all', inplace=True,axis=0)
                blo.dropna(how='all', inplace=True,axis=1)
            except:
                #messagebox.showerror("Extract Error", "Sheet name should be 'BLOWING' "+path)
                print('No file Blowing4')
        #blo.to_csv("blow_init.csv")
        
        return blo        