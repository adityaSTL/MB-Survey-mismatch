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

def summarycalc(file1):
    logs='Starting Summary Filling'+'\n'
    mandal_file=file1+'/'
    #no=0
    for info in sorted(os.listdir(mandal_file)):
        try:
            logs+='Opened the '+(mandal_file+info)+'\n'
            j=mandal_file+info
            span_file=j
            columns_ot=['prikey', 'Key', 'Survey Duration', 'User', 'Upload Time','Survey Name', '_scheduled_start', 
                        'Version', 'Complete','Survey Notes', 'Location Trigger', 'Instance Name', '_start', '_end',
                        '_device', 'instanceid', 'Package_Name', 'Zone_Name', 'District_Name','Mandal_Name', 
                        'From_GP', 'To_GP', 'Span_ID', 'Chainage_From','Chainage_To', 'Length', 'n1', 'Location', 
                        'From_Location','From_Location_Latitude_Manual', 'From_Location_Longitude_Manual','Offset', 
                        'Depth', 'Trench_Side', 'Duct_Laid', 'Method_Execution','Crossing', 'Strata_Type', 'Protection', 
                        'Protect_Dwc', 'Protect_Gi','Protect_Rcc', 'Protect_Pcc', 'Rcc_Chamber', 'Rcc_Marker', 'Remark']
            df1_ot=pd.DataFrame(columns=columns_ot)
            column_hdd=['prikey', 'Key', 'Survey Duration', 'User', 'Upload Time',
                'Survey Name', '_scheduled_start', 'Version', 'Complete',
                'Survey Notes', 'Location Trigger', 'Instance Name', '_start', '_end',
                '_device', 'instanceid', 'Package_Name', 'Zone_Name', 'District_Name',
                'Mandal_Name', 'From_GP', 'To_GP', 'Span_ID','Side_of_the_road', 'Chainage_From',
                'Chainage_To', 'Length', 'Start_Point_Location','Start_Point' ,
                'Start_Point_Manual_Latitude', 'Start_Point_Manual_Longitude',
                'Graph_as_built_made', 'Depth', 'Bore_reamer_diameter', 'Ducts'
                , 'End_Point_Location','End_Point' ,
                'End_Point_Manual_Latitude', 'End_Point_Manual_Longitude', 'Remark']

            column_drt=['prikey', 'Key', 'Survey Duration', 'User', 'Upload Time',
                'Survey Name', '_scheduled_start', 'Version', 'Complete',
                'Survey Notes', 'Location Trigger', 'Instance Name', '_start', '_end',
                '_device', 'instanceid', 'Package_Name', 'Zone_Name', 'District_Name',
                'Mandal_Name', 'From_GP', 'To_GP', 'Span_ID', 'Chamber1_Location',
                'Chamber1_Location_Point', 'Chamber1_Manual_Latitude',
                'Chamber1_Manual_Longitude', 'Chamber1_condition',
                'Chamber1_route_marker', 'Chamber2_Location', 'Chamber2_location_Point',
                'Chamber2_Manual_Latitude', 'Chamber2_Manual_Longitude',
                'Chamber2_condition', 'Chambe2_route_marker', 'ch_from', 'ch_to',
                'Length', 'Duct_dam_punct_loc', 'Duct_dam_punct_loc_point',
                'Duct_dam_punct_loc_Manual_Latitude',
                'Duct_dam_punct_loc_Manual_Longitude', 'Duct_dam_punct_loc_ch_from',
                'Duct_dam_punct_loc_ch_to', 'Duct_dam_punct_loc_Length',
                'Duct_miss_loc', 'Duct_miss_loc_pt', 'Duct_miss_loc_Manual_Latitude',
                'Duct_miss_loc_Manual_Longitude', 'Duct_miss_ch_from',
                'Duct_miss_ch_to', 'Duct_miss_ch_Length', 'Remark']
            df1_hdd=pd.DataFrame(columns=column_hdd)
            df1_drt=pd.DataFrame(columns=column_drt)


            blo=Extract.extract_blo(j)
            ot=Extract.extract_ot(j)
            if len(ot)!=0:
                ot=Create_table.create_ot(ot)
                df1_ot=pd.concat([df1_ot,ot])
            hdd=Extract.extract_hdd(j)
            if len(hdd)!=0:
                hdd=Create_table.create_hdd(hdd)
                df1_hdd=pd.concat([df1_hdd,hdd])
            drt=Extract.extract_drt(j)
            if len(drt)!=0:
                drt=Create_table.create_drt(drt)
                df1_drt=pd.concat([df1_drt,drt])

            df1_ot=df1_ot[['Zone_Name','Mandal_Name','To_GP','Span_ID',
                            'Chainage_From','Chainage_To', 'Length',
                            'Offset','Depth', 'Trench_Side', 'Duct_Laid', 'Method_Execution','Crossing', 
                            'Strata_Type','Protect_Dwc', 'Protect_Gi','Protect_Rcc', 'Protect_Pcc', 'Rcc_Chamber',
                            'Rcc_Marker', 'Remark']]

            df1_hdd['Duct_Laid']=df1_hdd['Length']

            df1_hdd['Method_Execution']='HDD'

            df1_hdd[['Crossing','Offset','Strata_Type','Protect_Dwc', 'Protect_Gi','Protect_Rcc', 'Protect_Pcc', 'Rcc_Chamber',
                    'Rcc_Marker']]=''
            df1_hdd.rename(columns={'Side_of_the_road':'Trench_Side'},inplace=True)

            df1_hdd=df1_hdd[['Zone_Name','Mandal_Name','To_GP','Span_ID',
                            'Chainage_From','Chainage_To', 'Length',
                            'Offset','Depth', 'Trench_Side', 'Duct_Laid', 'Method_Execution','Crossing', 
                            'Strata_Type','Protect_Dwc', 'Protect_Gi','Protect_Rcc', 'Protect_Pcc', 'Rcc_Chamber',
                            'Rcc_Marker', 'Remark']]


            df1_drt.reset_index(drop=True,inplace=True)
            df1_drt['Method_Execution']=''
            missing=[]
            for i in range(len(df1_drt)):
                if type(df1_drt.loc[i,'Duct_miss_ch_from'])==int and type(df1_drt.loc[i,'Duct_miss_ch_to'])==int:
                    missing.append([df1_drt.loc[i,'Duct_miss_ch_from'],df1_drt.loc[i,'Duct_miss_ch_to'],i])
                    df1_drt.loc[i,'Method_Execution']='Missing'
                else:
                    df1_drt.loc[i,'Method_Execution']='DRT'


            df1=pd.concat([df1_ot,df1_hdd])
            df1.sort_values(by=['Chainage_From'],inplace=True)
            df1.reset_index(drop=True,inplace=True)
            dr_ind=[]
            for i in range(len(df1)):
                ch1=df1.loc[i,'Chainage_From']
                ch2=df1.loc[i,'Chainage_To']
                for j in missing:
                    try:
                        if ch1<j[0] or ch2>j[1]:
                            continue
                    except:
                        print('Some_problem in Chainage')
                    try:
                        if ch1>=j[0] and ch2<=j[1]:
                            df1.loc[i,'Method_Execution']='Missing'
                            dr_ind.append(j[2])
                    except:
                        print('Some prob in Chainage')

            df1_drt.drop(dr_ind,inplace=True)
            df1_drt.rename(columns={'ch_from':'Chainage_From','ch_to':'Chainage_To'},inplace=True)
            df1_drt['Duct_Laid']=df1_drt['Length']
            df1_drt[['Offset','Depth','Trench_Side','Crossing','Strata_Type','Protect_Dwc', 'Protect_Gi','Protect_Rcc', 'Protect_Pcc', 'Rcc_Chamber','Rcc_Marker']]=''

            df1_drt=df1_drt[['Zone_Name','Mandal_Name','To_GP','Span_ID',
                            'Chainage_From','Chainage_To', 'Length',
                            'Offset','Depth', 'Trench_Side', 'Duct_Laid', 'Method_Execution','Crossing', 
                            'Strata_Type','Protect_Dwc', 'Protect_Gi','Protect_Rcc', 'Protect_Pcc', 'Rcc_Chamber',
                            'Rcc_Marker', 'Remark']]
            print(len(df1))
            print(len(df1_drt))
            df1=pd.concat([df1,df1_drt])
            print(len(df1))

            df1.sort_values(by=['Chainage_From'],inplace=True)

            temp=0
            miss_df=df1[df1['Method_Execution']=='Missing']
            miss_df.reset_index(drop=True,inplace=True)
            miss=[]
            for i in range(len(miss_df)-1):
                if miss_df.loc[i+1,'Chainage_From']==miss_df.loc[i,'Chainage_To']:
                    temp+=miss_df.loc[i,'Length']
                    print('temp- ',temp)
                    
                else:
                    if temp>50:
                        leng=temp-50
                        miss.append([miss_df.loc[i,'Chainage_To']-temp,miss_df.loc[i,'Chainage_To'],leng])
                    temp=0
            if temp>50:
                leng=temp-50
                miss.append([miss_df.loc[i,'Chainage_To']-temp,miss_df.loc[i,'Chainage_To'],leng])
                temp=0
            print(miss)
            df1.to_csv('mix_mb.csv')
            df_miss=df1[df1['Method_Execution']=='Missing'].reset_index()
            miss_lst=[]
            st=0
            for i in range(len(df_miss)):
                if st==0:
                    ch_from=df_miss.loc[i,'Chainage_From']
                    ch_to=df_miss.loc[i,'Chainage_To']
                    st=1
                else:
                    if ch_to==df_miss.loc[i,'Chainage_From']:
                        ch_to=df_miss.loc[i,'Chainage_To']
                    else:
                        miss_lst.append((ch_from,ch_to,ch_to-ch_from))
                        st=0
                if st==0:
                    ch_from=df_miss.loc[i,'Chainage_From']
                    ch_to=df_miss.loc[i,'Chainage_To']
                    st=1
                if i==len(df_miss)-1:
                    miss_lst.append((ch_from,ch_to,ch_to-ch_from))
            

            values={'Strata_Type':'NORMAL','Depth':1.4}

            df1.fillna(value=values,inplace=True)

            df1['Depth']=df1['Depth'].apply(lambda x: 1.4 if type(x) is str else x)
            df1['Strata_Type']=df1['Strata_Type'].apply(lambda x: 'Normal' if len(x)==0 else x)
            df1['Strata_Type']=df1['Strata_Type'].str.lower()
            df1['Depth']=df1['Depth'].astype(float)
            df1['Protect_Gi']=df1['Protect_Gi'].apply(lambda x: 0 if type(x)!= int else x)
            df1['Protect_Dwc']=df1['Protect_Dwc'].apply(lambda x: 0 if type(x)!= int else x)
            df1['Protect_Rcc']=df1['Protect_Rcc'].apply(lambda x: 0 if type(x)!= int else x)
            df1['Protect_Pcc']=df1['Protect_Pcc'].apply(lambda x: 0 if type(x)!= int else x)
            df1.reset_index(drop=True,inplace=True)
            def method_sum_fun(lst):
                if len(lst)==3:
                    if len(lst[-1])==1:
                        if lst[-1][0]==1.4:
                            return df1[df1['Depth']>=1.4][df1['Method_Execution']==lst[0]][df1['Strata_Type']==lst[1]]['Length'].sum()
                        else:
                            return df1[df1['Depth']<0.6][df1['Method_Execution']==lst[0]][df1['Strata_Type']==lst[1]]['Length'].sum()
                    else:
                        return df1[(df1['Depth']<lst[-1][0]) & (df1['Depth']>=lst[-1][1])][df1['Method_Execution']==lst[0]][df1['Strata_Type']==lst[1]]['Length'].sum()
                elif len(lst)==1:
                    return df1[df1['Method_Execution']==lst[0]]['Length'].sum()

            def gi_sum_fun(lst):
                if len(lst)==3:
                    if len(lst[-1])==1:
                        if lst[-1][0]==1.4:
                            return df1[df1['Depth']>=1.4]['Protect_Gi'].sum()
                        else:
                            return df1[df1['Depth']<0.6]['Protect_Gi'].sum()
                    else:
                        return df1[(df1['Depth']<lst[-1][0]) & (df1['Depth']>=lst[-1][1])]['Protect_Gi'].sum()
                elif len(lst)==1:
                    return df1['Protect_Gi'].sum()
                    
            def dwc_sum_fun(lst):
                if len(lst)==3:
                    if len(lst[-1])==1:
                        if lst[-1][0]==1.4:
                            return df1[df1['Depth']>=1.4]['Protect_Dwc'].sum()
                        else:
                            return df1[df1['Depth']<0.6]['Protect_Dwc'].sum()
                    else:
                        return df1[(df1['Depth']<lst[-1][0]) & (df1['Depth']>=lst[-1][1])]['Protect_Dwc'].sum()
                elif len(lst)==1:
                    return df1['Protect_Dwc'].sum()



            final_depth_criteria=[]#7X6
            depth_criteria=[]
            method=['OT','Missing',]
            strata=['normal','hard']
            depth=[[1.4],[1.4,1.3],[1.3,1.2],[1.2,1.1],[1.1,1.0],[1.0,0.6],[0.6]]
            for k in depth:
                for i in method:
                    for j in strata:
                        depth_criteria.append(method_sum_fun([i,j,k]))
                depth_criteria.append(gi_sum_fun(['xx','yy',k]))
                depth_criteria.append(dwc_sum_fun(['xx','yy',k]))
                final_depth_criteria.append(depth_criteria)
                # print(final_depth_criteria)
                depth_criteria=[]

            method_exec=[]#3X2
            non_bill=0
            for i in miss_lst:
                if i[-1]<50:
                    non_bill+=i[-1]
                else:
                    non_bill+=50
            method_exec.append([method_sum_fun(['OT']),0])
            method_exec.append([method_sum_fun(['DRT']),0])
            method_exec.append([method_sum_fun(['Missing'])-non_bill,non_bill])

            def check_if_in_missing_fift(ch_from,ch_to,miss_lst):
                for miss_lst_ in miss_lst:
                    if (ch_from>=miss_lst_[0] and ch_to<miss_lst_[1]) or (ch_from>=miss_lst_[0] and ch_from<miss_lst_[1]) or (ch_to>=miss_lst_[0] and ch_to<miss_lst_[1]):
                        return True
                return False

            protection=[]#3X2
            def check_if_in_missing_fift(ch_from,ch_to,miss_lst):
                for miss_lst_ in miss_lst:
                    if (ch_from>=miss_lst_[0] and ch_to<miss_lst_[1]) or (ch_from>=miss_lst_[0] and ch_from<miss_lst_[1]) or (ch_to>=miss_lst_[0] and ch_to<miss_lst_[1]):
                        return True
                return False
            dwc_bill=0
            dwc_no_bill=0
            dwc_lst=list(df1[df1['Protect_Dwc']>0]['Protect_Dwc'])
            ch_f_lst=list(df1[df1['Protect_Dwc']>0]['Chainage_From'])
            ch_t_lst=list(df1[df1['Protect_Dwc']>0]['Chainage_To'])
            for i in range(len(ch_f_lst)):
                if check_if_in_missing_fift(ch_f_lst[i],ch_t_lst[i],miss_lst) is True:
                    dwc_no_bill+=dwc_lst[i]
                else:
                    dwc_bill+=dwc_lst[i]
            gi_bill=0
            gi_no_bill=0
            gi_lst=list(df1[df1['Protect_Gi']>0]['Protect_Gi'])
            ch_f_lst=list(df1[df1['Protect_Gi']>0]['Chainage_From'])
            ch_t_lst=list(df1[df1['Protect_Gi']>0]['Chainage_To'])
            for i in range(len(ch_f_lst)):
                if check_if_in_missing_fift(ch_f_lst[i],ch_t_lst[i],miss_lst) is True:
                    gi_no_bill+=gi_lst[i]
                else:
                    gi_bill+=gi_lst[i]
            rcc_bill=0
            rcc_no_bill=0
            rcc_lst=list(df1[df1['Protect_Rcc']>0]['Protect_Rcc'])
            ch_f_lst=list(df1[df1['Protect_Rcc']>0]['Chainage_From'])
            ch_t_lst=list(df1[df1['Protect_Rcc']>0]['Chainage_To'])
            for i in range(len(ch_f_lst)):
                if check_if_in_missing_fift(ch_f_lst[i],ch_t_lst[i],miss_lst) is True:
                    rcc_no_bill+=rcc_lst[i]
                else:
                    rcc_bill+=rcc_lst[i]
            protection.append([dwc_bill,dwc_no_bill])
            protection.append([gi_no_bill,gi_bill])
            protection.append([rcc_no_bill,rcc_bill])

            jc=[]#2X2



            cable=[]#4X1
            fdms=[] # 4X1   
            ###
            jc=[]#2X2

            blo=Extract.extract_blo(j)
            column_blo=['prikey', 'Key', 'Survey Duration', 'User', 'Upload Time',
                'Survey Name', '_scheduled_start', 'Version', 'Complete',
                'Survey Notes', 'Location Trigger', 'Instance Name', '_start', '_end',
                '_device', 'instanceid', 'Package_Name', 'Zone_Name', 'District_Name',
                'Mandal_Name', 'From_GP', 'To_GP', 'Span_ID', 'Chainage_From',
                'Chainage_To', 'Length', 'chamber_from', 'chamber_to', 'size_of_ofc',
                'ofc_cable_id', 'cable_len_start', 'cable_len_end',
                'Total_cable_length', 'chamber_a_end_reading',
                'chamber_a_entry_reading', 'chamber_a_end_slack_loop_length',
                'chamber_b_entry_reading', 'chamber_b_end_reading',
                'chamber_b_end_slack_loop_length', 'Remarks']
            df1_blo=pd.DataFrame(columns=column_blo)
            if len(blo)!=0:
                blo,jc=Create_table.create_blo(blo)
                df1_blo=pd.concat([df1_blo,blo])

            drt_ch_from=list(df1[df1['Method_Execution'].isin( ['DRT','Missing'])]['Chainage_From'])
            drt_ch_to=list(df1[df1['Method_Execution'].isin( ['DRT','Missing'])]['Chainage_To'])

            ch_from_lst=list(df1_blo['Chainage_From'])
            ch_to_lst=list(df1_blo['Chainage_To'])
            chmb_from_lst=list(df1_blo['chamber_from'])
            chmb_to_lst=list(df1_blo['chamber_to'])
            jc_bill=0
            jc_no_bill=0

            def check_in_drt(x,lst_from,lst_to):
                if type(x) is int:
                    for i in range(len(lst_to)):
                        if x>=lst_from[i] and x<lst_to[i]:
                            return True
                return False
            for i in range(len(ch_from_lst)):
                if i==0:
                    if check_in_drt(ch_from_lst[i],drt_ch_from,drt_ch_to):
                        if 'HH' in chmb_from_lst[i] or 'MH' in chmb_from_lst[i]:
                            jc_no_bill+=1
                    else:
                        if 'HH' in chmb_from_lst[i] or 'MH' in chmb_from_lst[i]:
                            jc_bill+=1
                if check_in_drt(ch_to_lst[i],drt_ch_from,drt_ch_to):
                    if 'HH' in chmb_to_lst[i] or 'MH' in chmb_to_lst[i]:
                        jc_no_bill+=1

                else:
                    if 'HH' in chmb_to_lst[i] or 'MH' in chmb_to_lst[i]:
                        jc_bill+=1

            jc.append([jc_bill,jc_no_bill])
            jc.append([jc_bill,jc_no_bill])

            ####

            print(final_depth_criteria)
            print(method_exec)
            print(protection)


            ############################DATA FILLING###############################################3
            print("Started Writing in excel")
            #j='WRG-ZAF-5706-M-01-GR01-02.xlsx'
            xfile = openpyxl.load_workbook(span_file)
            sheet1=xfile['Summary']

            row=3
            no=48
            for i in final_depth_criteria:
                first=math.floor((no+row-48)/10)
                temp=(chr(no+first))+ chr((no+row-48)%10+48)
                sheet1['B'+temp]=i[0]
                sheet1['C'+temp]=i[1]
                sheet1['D'+temp]=i[2]
                sheet1['E'+temp]=i[3]
                sheet1['F'+temp]=i[4]
                sheet1['G'+temp]=i[5]
                row+=1
                


            row=11
            no=48
            for i in method_exec:
                first=math.floor((no+row-48)/10)
                temp=(chr(no+first))+ chr((no+row-48)%10+48)
                sheet1['C'+temp]=i[0]
                sheet1['D'+temp]=i[1]
                row+=1
            


            row=15
            no=48
            for i in protection:
                first=math.floor((no+row-48)/10)
                temp=(chr(no+first))+ chr((no+row-48)%10+48)
                sheet1['B'+temp]=i[0]
                sheet1['C'+temp]=i[1]
                row+=1
                    

            row=19
            no=48
            for i in jc:
                first=math.floor((no+row-48)/10)
                temp=(chr(no+first))+ chr((no+row-48)%10+48)
                sheet1['B'+temp]=i[0]
                sheet1['C'+temp]=i[1]
                row+=1         

            sheet2=xfile['Missing Chainages']

            row=2
            no=48
            for i in miss_lst:
                first=math.floor((no+row-48)/10)
                temp=(chr(no+first))+ chr((no+row-48)%10+48)
                sheet2['B'+temp]=i[0]
                sheet2['C'+temp]=i[1]
                sheet2['D'+temp]=i[2]
                row+=1

            print(miss_lst)

            xfile.save(filename=span_file)
            logs+='Successfully closed the '+(mandal_file+info)+'\n'
        
        except:
            logs+='Problem in the '+(mandal_file+info)+'\n'        

    return logs