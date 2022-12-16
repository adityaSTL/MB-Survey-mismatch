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


def miss(drt):
    #drt.to_csv('drtinfin.csv')
    try:
        fin5=0
        fin=0
        fin50=0
        temp=0
        s=0  
        for i in range(len(drt)):
            ch1=drt.loc[i,'Duct_miss_ch_from']
            ch2=drt.loc[i,'Duct_miss_ch_to']
            if i!=(len(drt)-1):
                ch3=drt.loc[i+1,'Duct_miss_ch_from']

            temp=(drt.loc[i,'Duct_miss_ch_Length'])
            """
            try:
                if np.isnan(drt.loc[i,'Duct_miss_ch_Length']) or temp==0:
                    temp=abs(ch2-ch1)
            except:
                print()        
            """
            if ch3==ch2:
                s+=temp  

            elif ch3!=ch2:
                s=np.nansum([s+temp])
                if(s>=50):
                    fin5+=1
                    fin50+=s
                    s-=50
                    fin+=s
                    s=0
                elif s<50:
                    fin50+=s
                    s=0
        
        if np.isnan(fin):
            fin=0   

        if np.isnan(fin50):
           fin50=0   

        miss_bill=fin
        miss_len=fin50

    except:
        miss_bill=0
        miss_len=0

    print("miss_len",miss_len," ","miss_bill",miss_bill)
    return miss_len,miss_bill            

def dam(drt):
    try:
        fin5=0
        fin=0
        fin50=0
        temp=0
        s=0  
        for i in range(len(drt)):
            ch1=drt.loc[i,'Duct_dam_punct_loc_ch_from']
            ch2=drt.loc[i,'Duct_dam_punct_loc_ch_to']
            if i!=(len(drt)-1):
                ch3=drt.loc[i+1,'Duct_dam_punct_loc_ch_from']

            temp=(drt.loc[i,'Duct_dam_punct_loc_Length'])
            """
            try:
                if np.isnan(drt.loc[i,'Duct_dam_punct_loc_Length']) or temp==0:
                    temp=abs(ch2-ch1)
            except:
                print()
            """
            if ch3==ch2:
                s+=temp  

            elif ch3!=ch2:
                s=np.nansum([s+temp])
                if(s>=50):
                    fin5+=1
                    fin50+=s
                    s-=50
                    fin+=s
                    s=0
                elif s<50:
                    fin50+=s
                    s=0
        
        if np.isnan(fin):
            fin=0   

        if np.isnan(fin50):
           fin50=0   

        dam_bill=fin
        dam_len=fin50

    except:
        dam_bill=0
        dam_len=0

    print("dam_len",dam_len," ","dam_bill",dam_bill)
    return dam_len,dam_bill 

def scope(blo):
    try:
        last_blow=blo['Chainage_To'].iloc[-1]
        print("Doing this calc. of last_blowing",last_blow)
        att=pd.isnull(last_blow)
        atp=not(isinstance(last_blow, int))
        atc=att+atp
        if (atc):
            last_blow=blo['Chainage_To'].iloc[-2]
            print("Last blow for -2 case",last_blow)
        print("Final case",last_blow)
        if np.isnan(last_blow):
            last_blow=0       
            
    except:
        last_blow=0    

    return last_blow   

def dit_len(drt):
    try:
        print("starting dit len calc function")
        a=(drt['Duct_miss_ch_Length']==0)
        b=~(drt['Duct_miss_ch_Length'].astype(str).str.isdigit())
        y=a+b

        print("Dit length only miss",drt.loc[y,'Length'].sum()/1000)
        c=(drt['Duct_dam_punct_loc_Length']==0)
        d=~(drt['Duct_dam_punct_loc_Length'].astype(str).str.isdigit())
        
        z=c+d

        print("Dit length only dam",drt.loc[z,'Length'].sum()/1000)

        e=y*z
        print("Dit length",drt.loc[e,'Length'].sum()/1000)
        dit_len=drt.loc[e,'Length'].sum()

        if np.isnan(dit_len):
            dit_len=0   
            
    except:
        dit_len=0    

    return dit_len

def drt_len(drt):
    try:

        drt_len=drt['Length'].sum()
        if np.isnan(drt_len):
            drt_len=drt['ch_to'].sum()-drt['ch_from'].sum()

        print("drt_len: ",drt_len)
        if np.isnan(drt_len):
           drt_len=0   
        
    except:
        drt_len=0    

    return drt_len    

def filler(file1,file2):
    logs='Starting calculate function.'+'\n'
    print("starting filler function")
    xfile = openpyxl.load_workbook(file2)
    sheet1=xfile['GP-Wise BOQ']
    mandal_file=file1+'/'

    no=0
    for info in sorted(os.listdir(mandal_file)):
        logs+='Opened the '+(mandal_file+info)+'\n'
        try:
            j=mandal_file+info
            print(j)

            blo=Extract.extract_blo(j)
            #blo.to_csv("blo1.csv")
            if len(blo)!=0:
                (blo,joint_closer)=Create_table.create_blo(blo)
                blo.to_csv("blo.csv")
                
            drt=Extract.extract_drt(j)
            if len(drt)!=0:
                drt=Create_table.create_drt(drt)
                drt.reset_index(drop=True,inplace=True)
                drt.to_csv("drt.csv")

            ot=Extract.extract_ot(j)
            if len(ot)!=0:
                ot=Create_table.create_ot(ot)
                ot.to_csv("ot.csv")   

            hdd=Extract.extract_hdd(j)
            if len(hdd)!=0:
                hdd=Create_table.create_hdd(hdd)
                hdd.to_csv("hdd.csv") 

            var='F'
            if no<=10:
                var=chr(ord(var)+2*no)
            elif no>10:
                var='A'+chr(ord(var)+2*no-26)

            try:
                sheet1[var+'3']=info[:-5]
                #sheet1[var1+'4']='STATE'
                #sheet1[var+'4']='BBNL'
                len_288=(blo.loc[blo['size_of_ofc'].isin(['288F','288 F','288']),'Total_cable_length'].sum())
                """
                try:
                    if np.isnan(len_288) or len_288==0:
                        len_288=(blo.loc[blo['size_of_ofc'].isin(['288F','288 F','288']),'cable_len_end'].sum())-(blo.loc[blo['size_of_ofc'].isin(['288F','288 F','288']),'cable_len_start'].sum())
                except:
                    print()
                """    
                len_144=(blo.loc[blo['size_of_ofc'].isin(['144F','144 F','144']),'Total_cable_length'].sum())
                """
                try:
                    if np.isnan(len_144) or len_144==0:
                        len_144=(blo.loc[blo['size_of_ofc'].isin(['144F','144 F','144']),'cable_len_end'].sum())-(blo.loc[blo['size_of_ofc'].isin(['144F','144 F','144']),'cable_len_start'].sum())
                except:
                    print()
                """    
                len_96=(blo.loc[blo['size_of_ofc'].isin(['96F','96 F','96']),'Total_cable_length'].sum())
                """
                print("Keep eyes wide shut:",len_96,"np.isnan(len_96):",np.isnan(len_96))
                try:
                    if np.isnan(len_96) or len_96==0:
                        len_96=(blo.loc[blo['size_of_ofc'].isin(['96F','96 F','96']),'cable_len_end'].sum())-(blo.loc[blo['size_of_ofc'].isin(['96F','96 F','96']),'cable_len_start'].sum())
                except:
                    print()
                """    
                len_48=(blo.loc[blo['size_of_ofc'].isin(['48F','48 F','48']),'Total_cable_length'].sum())
                """
                try:
                    if np.isnan(len_48) or len_48==0:
                        len_48=(blo.loc[blo['size_of_ofc'].isin(['48F','48 F','48']),'cable_len_end'].sum())-(blo.loc[blo['size_of_ofc'].isin(['48F','48 F','48']),'cable_len_start'].sum())
                except:
                    print()
                """    

                sheet1[var+'11']=(len_288)/1000
                sheet1[var+'14']=(len_144)/1000
                sheet1[var+'17']=(len_96)/1000
                sheet1[var+'18']=(len_48)/1000


            except:
                print("No such Blowing files..")

            try:                
                sheet1[var+'29']=(joint_closer.loc[joint_closer['cha_loop'].isin(['288F','288 F','288']),'chb_end'].sum())
                sheet1[var+'32']=(joint_closer.loc[joint_closer['cha_loop'].isin(['144F','144 F','144']),'chb_end'].sum())
                sheet1[var+'35']=(joint_closer.loc[joint_closer['cha_loop'].isin(['96F','96 F','96']),'chb_end'].sum())
                sheet1[var+'36']=(joint_closer.loc[joint_closer['cha_loop'].isin(['48F','48 F','48']),'chb_end'].sum())

                
            except:
                print("No such Joint Closure files..")  

            try:     
                sheet1[var+'23']=(ot['Protect_Dwc'].sum())/1000
                sheet1[var+'24']=(ot['Protect_Gi'].sum())/1000
                sheet1[var+'25']=(ot['Rcc_Marker'].sum())
                sheet1[var+'26']=(ot['Rcc_Chamber'].sum())
    

            except:
                print("No such OT files..")  

            try:     
                sheet1[var+'22']=(scope(blo)-drt_len(drt))/1000
                sheet1[var+'99']=(dit_len(drt))/1000
                miss_tot,miss_bill=miss(drt)
                dam_tot,dam_bill=dam(drt)
                sheet1[var+'137']=(miss_tot+dam_tot)/1000
                sheet1[var+'138']=(miss_bill+dam_bill)/1000
    

            except:
                print("No such DRTT files..")           

            xfile.save(filename="BOQ122.xlsx")
            no+=1        
            logs+='Successfully closed the '+(mandal_file+info)+'\n'
        
        except:
            logs+='Problem in the '+(mandal_file+info)+'\n'
            #print("mandal_file+info")
    
    
    return logs

"""
def calculate(file1,file2):
    logs='Starting calculate function.'+'\n'

    xfile = openpyxl.load_workbook(file2)
    sheet1=xfile['GP-Wise BOQ']
    mandal_file=file1+'/'
    no=0
    for info in sorted(os.listdir(mandal_file)):

        j=mandal_file+info
        print(j)

        blo=Extract.extract_blo(j)
        #blo.to_csv("blo1.csv")
        if len(blo)!=0:
            (blo,joint_closer)=Create_table.create_blo(blo)
            
        drt=Extract.extract_drt(j)
        if len(drt)!=0:
            drt=Create_table.create_drt(drt)
            drt.reset_index(drop=True,inplace=True)

        ot=Extract.extract_ot(j)
        if len(ot)!=0:
            ot=Create_table.create_ot(ot)   

        hdd=Extract.extract_hdd(j)
        if len(hdd)!=0:
            hdd=Create_table.create_hdd(hdd)  
  
        
        s=0 #no idea!
        fin=0 #Missing section sum
        fin1=0  #Damaged section sum
        fin50=0
        fin5=0
        fintot=0
        temp=0  #Temp no imp value

        try:
            sum=0
            drt=drt.reset_index(drop=True)
            for i in range(len(drt)):
                ch1=drt.loc[i,'ch_from']
                ch2=drt.loc[i,'ch_to']
                if i!=(len(drt)-1):
                    ch3=drt.loc[i+1,'ch_from']
                    if(ch3!=ch2):
                        sum+=ch3-ch2
            
            if np.isnan(sum):
                sum=0

            print("sum after chaining",sum)
            
        ##Case 2: SUM From missing section
            ##For missing case -50 agreement  
            temp=0
            s=0  
            for i in range(len(drt)):
                ch1=drt.loc[i,'Duct_miss_ch_from']
                ch2=drt.loc[i,'Duct_miss_ch_to']
                if i!=(len(drt)-1):
                    ch3=drt.loc[i+1,'Duct_miss_ch_from']

                temp=(drt.loc[i,'Duct_miss_ch_Length'])

                if ch3==ch2:
                    s+=temp  

                elif ch3!=ch2:
                    #print("got it")
                    s=np.nansum([s+temp])
                    #print(temp,"s is",s,"done")
                    #print(s)
                    if(s>=50):
                        fin5+=1
                        fin50+=s
                        s-=50
                        fin+=s
                        s=0
                    elif s<50:
                        fintot+=s
                        s=0
            ##Case 3: SUM From damaged section
            ##For damaged case -50 Agreement
            temp=0
            s=0
            for i in range(len(drt)):
                ch1=drt.loc[i,'Duct_dam_ch_from']
                ch2=drt.loc[i,'Duct_dam_ch_to']
                if i!=(len(drt)-1):
                    ch3=drt.loc[i+1,'Duct_dam_ch_from']

                temp=(drt.loc[i,'Duct_dam_ch_Length'])

                if ch3==ch2:
                    s+=temp  

                elif ch3!=ch2:
                    #print("got it")
                    s=np.nansum([s+temp])
                    #print(temp,"s is",s,"done")
                    #print(s)
                    if(s>=50):
                        s-=50
                        fin1+=s
                        s=0
                    elif s<50:
                        s=0
                #print(temp," ",s," ",fin," ",ch1," ",ch2," ",ch3)       

            if np.isnan(sum):
                sum=0  


        except:
            print("Something Wrong in missing calculation")
        #print("Sum after missing")
        if np.isnan(fin):
            fin=0   

        if np.isnan(fin1):
           fin1=0           
        
        sum+=fin1
        print("Present value of sum after Chainaing && (mis+dam) case",sum)

        print("Missing case",fin,"Dam case",fin1)                

        try:
            blo=blo.reset_index(drop=True)
            start_drt=drt['ch_from'].iloc[0]
            sum+=(start_drt-0)
            print("Sum before starting 0 is ",start_drt-0)
            print("Present value of sum after Chaining && starting case and after (mis+dam) case",sum)

            #####################Calculation Last Blow########################################
            ##Case 4: SUM From lat blowing and DRT reading mismatch section
            last_blow=blo['Chainage_To'].iloc[-1]
            print("Doing this calc. of last_blowing",last_blow)
            att=pd.isnull(last_blow)
            #print(att)
            atp=not(isinstance(last_blow, int))
            #print(atp)
            atc=att+atp
            #print(atc)
            #np.isnan(last_blow) or
            if (atc):
                last_blow=blo['Chainage_To'].iloc[-2]
                print("Last blow for -2 case",last_blow)
            print("Final case",last_blow)
            if np.isnan(last_blow):
                last_blow=0    
            ##############################Last BLow Calculation################################

            ###################Last DRT Calculation#####################           
            last_drt=drt['ch_to'].iloc[-1]
            att1=pd.isnull(last_drt)
            #print(att)
            atp1=not(isinstance(last_drt, int))
            #print(atp)
            atc1=att1+atp1
            #print(atc1)
            #np.isnan(last_blow) or
            if (atc1):
                last_drt=drt['Ch_to'].iloc[-2]
                print("Last drt for -2 case",last_drt)
            
            ##########Last DRT CAlculation########################

            if np.isnan(last_drt):
                last_drt=0           
            print("Doing last cal of last drt",last_drt)
            sum+=last_blow-last_drt
            print("Final Sum is ",sum)    
            
        
        except:
            print('Something wrong in blowing gap calculation or drt file')    
        
        ##DRT Calculation over!!!!!!
        ######################################################################################################################################
        ######################################################################################################################################
            

        ###Feeeding the data starts!!!    
        #no=0
        var='F'
        if no<=10:
            var=chr(ord(var)+2*no)
        elif no>10:
            var='A'+chr(ord(var)+2*no-26)
        try:
            sheet1[var+'3']=info[:-5]
            #sheet1[var1+'4']='STATE'
            #sheet1[var+'4']='BBNL'
            sheet1[var+'11']=(blo.loc[blo['size_of_ofc'].isin(['288F','288 F','288']),'Total_cable_length'].sum())/1000
            sheet1[var+'14']=(blo.loc[blo['size_of_ofc'].isin(['144F','144 F','144']),'Total_cable_length'].sum())/1000
            sheet1[var+'17']=(blo.loc[blo['size_of_ofc'].isin(['96F','96 F','96']),'Total_cable_length'].sum())/1000
            sheet1[var+'18']=(blo.loc[blo['size_of_ofc'].isin(['48F','48 F','48']),'Total_cable_length'].sum())/1000
   

        except:
            print("No such Blowing files..")

        try:                
            sheet1[var+'29']=(joint_closer.loc[joint_closer['cha_loop'].isin(['288F','288 F','288']),'chb_end'].sum())
            sheet1[var+'32']=(joint_closer.loc[joint_closer['cha_loop'].isin(['144F','144 F','144']),'chb_end'].sum())
            sheet1[var+'35']=(joint_closer.loc[joint_closer['cha_loop'].isin(['96F','96 F','96']),'chb_end'].sum())
            sheet1[var+'36']=(joint_closer.loc[joint_closer['cha_loop'].isin(['48F','48 F','48']),'chb_end'].sum())

            
        except:
            print("No such Joint Closure files..")  

        try:
            if len(drt)!=0 and sum==0:
                sheet1[var+'22']=sum/1000
                #sheet1[var+'139']=fin/1000
                sheet1[var+'137']=(fin50 + fintot)/1000
                sheet1[var+'138']=(fin5*50)/1000
                
                a=(drt['Duct_miss_ch_Length']==0)
                b=~(drt['Duct_miss_ch_Length'].astype(str).str.isdigit())
                y=a+b
                print("Dit length only miss",drt.loc[y,'Length'].sum()/1000)
                c=(drt['Duct_dam_punct_loc_Length']==0)
                d=~(drt['Duct_dam_punct_loc_Length'].astype(str).str.isdigit())
                #print(c+d)
                z=c+d
                
                print("Dit length only dam",drt.loc[z,'Length'].sum()/1000)

                e=y*z
                print("Dit length",drt.loc[e,'Length'].sum()/1000)
                sheet1[var+'98']=drt.loc[e,'Length'].sum()/1000
                #sheet1[var+'21']=sum/1000
                print("Duct laid",sum)

            elif len(drt)==0 and sum==0:
                print("No DRT File case triggered,dit=0, duct laid=sum(blowing)")
                sum=(blo['Length'].sum())
                print("No drt case+no sum case",sum)
                sheet1[var+'99']=0
                sheet1[var+'22']=sum/1000
                sheet1[var+'138']=(fin5*50)/1000
                sheet1[var+'137']=(fin50 + fintot)/1000
                #sheet1[var+'138']=(fin5*50)/1000

            else:    
                a=(drt['Duct_miss_ch_Length']==0)
                b=~(drt['Duct_miss_ch_Length'].astype(str).str.isdigit())
                y=a+b
                #print(a+b)
                print("Dit length only miss",drt.loc[y,'Length'].sum()/1000)
                c=(drt['Duct_dam_punct_loc_Length']==0)
                d=~(drt['Duct_dam_punct_loc_Length'].astype(str).str.isdigit())
                #print(c+d)
                z=c+d
                #tim=(drt.loc[z,'Length'])
                #print(tim.loc['Length'].sum())
                #print(drt.loc[z,'Length'].sum())
                print("Dit length only dam",drt.loc[z,'Length'].sum()/1000)

                e=y*z
                print("Dit length",drt.loc[e,'Length'].sum()/1000)
                sheet1[var+'99']=drt.loc[e,'Length'].sum()/1000
                sheet1[var+'22']=sum/1000
                sheet1[var+'138']=(fin5*50)/1000
                sheet1[var+'137']=(fin50 + fintot)/1000
                #sheet1[var+'138']=(fin5*50)/1000
                print("Duct laid",sum)
        except:
            print("No such DRT files..")


        try:     
            sheet1[var+'23']=(ot['Protect_Dwc'].sum())/1000
            sheet1[var+'24']=(ot['Protect_Gi'].sum())/1000
            sheet1[var+'25']=(ot['Rcc_Marker'].sum())
            sheet1[var+'26']=(ot['Rcc_Chamber'].sum())
   

        except:
            print("No such OT files..")    

        xfile.save(filename="BOQ122.xlsx")
        ##print(duct_laid,dwc_pipe,gi_pipe,route_indicators,joint_chambers)
        no+=1
    return logs

"""    