import numpy as np
import pandas as pd
from tkinter import messagebox






class Create_table:
    def create_ot(ot):
        zone=''
        mandal=''
        to_gp=''
        span_id=''

        
        ot.reset_index(drop=True,inplace=True)
        j=0
        columns_={}
        for i in ot.columns:
                if j==0:
                    columns_[i]='S_no'
                elif j==1:
                    columns_[i]='Ch_from'
                elif j==2:
                    columns_[i]='Ch_to'
                elif j==3:
                    columns_[i]='Length'
                elif j==4:
                    columns_[i]='Offset'
                elif j==5:
                    columns_[i]='Depth'
                elif j==6:
                    columns_[i]='Trench side'
                elif j==7:
                    columns_[i]='Duct Laid'
                elif j==8:
                    columns_[i]='Exec'
                elif j==9:
                    columns_[i]='Crossing'
                elif j==10:
                    columns_[i]='strata'
                elif j==11:
                    columns_[i]='dwc'
                elif j==12:
                    columns_[i]='gi'
                elif j==13:
                    columns_[i]='rcc'
                elif j==14:
                    columns_[i]='pcc'
                elif j==15:
                    columns_[i]='rcc_ch'
                elif j==16:
                    columns_[i]='rcc_route'
                elif j==17:
                    columns_[i]='remark'
                j+=1
        ot.rename(columns=columns_,inplace=True)
        #ot.to_csv('otinintal.csv')
        def remove_noise(ot):
            ot.reset_index(drop=True,inplace=True)
            
            index=[]
            for i in range(len(ot)):
                if (type(ot.loc[i,'S_no'])==int or type(ot.loc[i,'dwc'])==int or type(ot.loc[i,'gi'])==int or type(ot.loc[i,'rcc_ch'])==int or type(ot.loc[i,'rcc_route'])==int):
                    #print(ot.loc[ot[i,]])
                    ot.at[i,'S_no']=80
            #ot.to_csv('otafterputting80.csv')
            for i in range(len(ot)):
                

                if type(ot.loc[i,'S_no'])!=int:
                    index.append(i)
                    """
                elif ot.loc[i,'Ch_from'] is np.nan:
                    index.append(i)
                    """
            return ot.drop(index,axis=0)
        # 
        
        ot=remove_noise(ot)    
        #ot.to_csv('otafternoise.csv')
        df1=pd.DataFrame(columns=columns_)
        # 
        df1['Chainage_From']=ot['Ch_from']
        df1['Chainage_To']=ot['Ch_to']
        df1['Length']=ot['Length']
        df1['Offset']=ot['Offset']
        df1['Depth']=ot['Depth']
        df1['Trench_Side']=ot['Trench side']
        df1['Duct_Laid']=ot['Duct Laid']
        df1['Method_Execution']=ot['Exec']
        df1['Crossing']=ot['Crossing']
        df1['Strata_Type']=ot['strata']
        df1['Protect_Dwc']=ot['dwc']
        df1['Protect_Gi']=ot['gi']
        df1['Protect_Rcc']=ot['rcc']
        df1['Protect_Pcc']=ot['pcc']
        df1['Rcc_Chamber']=ot['rcc_ch']
        df1['Rcc_Marker']=ot['rcc_route']
        df1['Remark']=ot['remark']
        # df1['Zone_Name']
        df1['Zone_Name']=zone
        df1['Mandal_Name']=mandal
        df1['To_GP']=to_gp
        df1['Span_ID']=span_id  
        #print(df1)
        df1.reset_index(drop=True,inplace=True)

        try:
            for i in range(len(df1)):
                if pd.isnull(df1.loc[i,'Length']) or df1.loc[i,'Length']==0:
                    if type(df1.loc[i,'Chainage_To'])==int and type(df1.loc[i,'Chainage_From'])==int:
                        df1.loc[i,'Length']=abs(df1.loc[i,'Chainage_To']-df1.loc[i,'Chainage_From'])
        except:
            print("Error in correction of OT")                
        
        return df1


    def create_hdd(hdd):
        zone=''
        mandal=''
        to_gp=''
        span_id=''
        """
        for i in range(4,12):
            if len(hdd.columns)<i:
                break
            zone_mandal=hdd.loc[4,hdd.columns[i]]
            # print(zone_mandal)
            try:
                zone=zone_mandal.split('/')[0]
                mandal=zone_mandal.split('/')[1]
                to_gp=zone_mandal.split('/')[2]
            # 
                # 
            except:
                print('Something')
            
            try:
                span_id=hdd.loc[6,hdd.columns[i]]
            except:
                print('Problem in SpanID')
            if len(zone)>0:
                break
        
        
        hdd=hdd[10:]
        """
        j=0
        columns_={}
        for i in hdd.columns:
            if j==0:
                columns_[i]='S_no'
            elif j==1:
                columns_[i]='Side'
            elif j==2:
                columns_[i]='Ch_from'
            elif j==3:
                columns_[i]='Ch_to'
            elif j==4:
                columns_[i]='Len'
            elif j==5:
                columns_[i]='Graph'
            elif j==6:
                columns_[i]='Depth'
            elif j==7:
                columns_[i]='Dia'
            elif j==8:
                columns_[i]='Duct'
            elif j==9:
                columns_[i]='Remark'
            
            j+=1
        hdd.rename(columns=columns_,inplace=True)
        def remove_noise(hdd):
            hdd.reset_index(drop=True,inplace=True)
            index=[]
            for i in range(len(hdd)):
                if type(hdd.loc[i,'S_no'])!=int:
                    index.append(i)
                elif type(hdd.loc[i,'Ch_from']) is not int:
                    index.append(i)
            return hdd.drop(index,axis=0)
        
        hdd=remove_noise(hdd)    
        
        df1=pd.DataFrame(columns=['prikey', 'Key', 'Survey Duration', 'User', 'Upload Time',
               'Survey Name', '_scheduled_start', 'Version', 'Complete',
               'Survey Notes', 'Location Trigger', 'Instance Name', '_start', '_end',
               '_device', 'instanceid', 'Package_Name', 'Zone_Name', 'District_Name',
               'Mandal_Name', 'From_GP', 'To_GP', 'Span_ID','Side_of_the_road', 'Chainage_From',
               'Chainage_To', 'Length', 'Start_Point_Location','Start_Point' ,
               'Start_Point_Manual_Latitude', 'Start_Point_Manual_Longitude',
               'Graph_as_built_made', 'Depth', 'Bore_reamer_diameter', 'Ducts'
                , 'End_Point_Location','End_Point' ,
               'End_Point_Manual_Latitude', 'End_Point_Manual_Longitude', 'Remark'])
        
        df1['Chainage_From']=hdd['Ch_from']
        df1['Chainage_To']=hdd['Ch_to']
        df1['Length']=hdd['Len']
        df1['Depth']=hdd['Depth']
        df1['Side_of_the_road']=hdd['Side']
        df1['Ducts']=hdd['Duct']
        df1['Bore_reamer_diameter']=hdd['Dia']
        df1['Graph_as_built_made']=hdd['Graph']
        
        df1['Remark']=hdd['Remark']
        #df1['Zone_Name']
        df1['Zone_Name']=zone
        df1['Mandal_Name']=mandal
        df1['To_GP']=to_gp
        df1['Span_ID']=span_id
        #df1=corrector(df1,'Chainage_From','Chainage_To','Length')

        df1.reset_index(drop=True,inplace=True)
        
        try:
            for i in range(len(df1)):
                if pd.isnull(df1.loc[i,'Length']) or df1.loc[i,'Length']==0:
                    if type(df1.loc[i,'Chainage_To'])==int and type(df1.loc[i,'Chainage_From'])==int:
                        df1.loc[i,'Length']=abs(df1.loc[i,'Chainage_To']-df1.loc[i,'Chainage_From'])

        except:
            print("Problems in correction of HDD")                
        
        return df1

    def create_drt(drt):
        zone=''
        mandal=''
        to_gp=''
        span_id=''

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
        
        #drt.to_csv("drt0.csv")

        def remove_noise(drt):
            drt.reset_index(drop=True,inplace=True)
            index=[]
            for i in range(len(drt)):
                if type(drt.loc[i,'Ch_from'])==int or type(drt.loc[i,'Ch_to'])==int or type(drt.loc[i,'Len'])==int or type(drt.loc[i,'Duct_dam_len'])==int or type(drt.loc[i,'Duct_miss_len'])==int:
                    drt.at[i,'S_no']=81
                    #drt.loc[i,'Duct_miss_ch_from']=drt.loc[i,'Duct_miss_len']

                if type(drt.loc[i,'S_no'])!=int:
                    index.append(i)

                
            return drt.drop(index,axis=0)
        
        
        drt.reset_index(drop=True,inplace=True)
        for i in range(len(drt)):
            if type(drt.loc[i,'Duct_dam_ch_from'])==int and type(drt.loc[i,'Duct_dam_ch_to'])==int:
                drt.loc[i,'Ch_from']=drt.loc[i,'Duct_dam_ch_from']
                drt.loc[i,'Ch_to']=drt.loc[i,'Duct_dam_ch_to']
                drt.loc[i,'Len']=abs(drt.loc[i,'Duct_dam_ch_from']-drt.loc[i,'Duct_dam_ch_to'])
                drt.loc[i,'Duct_dam_len']=abs(drt.loc[i,'Duct_dam_ch_from']-drt.loc[i,'Duct_dam_ch_to'])

        drt.reset_index(drop=True,inplace=True)
        for i in range(len(drt)):
            if type(drt.loc[i,'Duct_miss_ch_from'])==int and type(drt.loc[i,'Duct_miss_ch_to'])==int:
                drt.loc[i,'Ch_from']=drt.loc[i,'Duct_miss_ch_from']
                drt.loc[i,'Ch_to']=drt.loc[i,'Duct_miss_ch_to']
                drt.loc[i,'Len']=abs(drt.loc[i,'Duct_miss_ch_from']-drt.loc[i,'Duct_miss_ch_to'])
                drt.loc[i,'Duct_miss_len']=abs(drt.loc[i,'Duct_miss_ch_from']-drt.loc[i,'Duct_miss_ch_to'])

        drt=remove_noise(drt)        
            

        df1=pd.DataFrame(columns=['prikey', 'Key', 'Survey Duration', 'User', 'Upload Time',
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
               'Duct_miss_ch_to', 'Duct_miss_ch_Length', 'Remark'])
        df1['Chamber1_Manual_Latitude']=drt['Ch1_lat']
        df1['Chamber1_Manual_Longitude']=drt['Ch1_long']
        df1['Chamber1_condition']=drt['Ch1_cond']
        df1['Chamber1_route_marker']=drt['Ch1_route_marker']
        df1['Chamber2_Manual_Latitude']=drt['Ch2_lat']
        df1['Chamber2_Manual_Longitude']=drt['Ch2_long']
        df1['Chamber2_condition']=drt['Ch2_cond']
        df1['Chambe2_route_marker']=drt['Ch2_route_marker']
        df1['ch_from']=drt['Ch_from']
        df1['ch_to']=drt['Ch_to']
        df1['Length']=drt['Len']
        df1['Duct_dam_punct_loc_Manual_Latitude']=drt['Duct_dam_lat']
        df1['Duct_dam_punct_loc_Manual_Longitude']=drt['Duct_dam_long']
        df1['Duct_dam_punct_loc_ch_from']=drt['Duct_dam_ch_from']
        df1['Duct_dam_punct_loc_ch_to']=drt['Duct_dam_ch_to']
        df1['Duct_dam_punct_loc_Length']=drt['Duct_dam_len']
        df1['Duct_miss_loc_Manual_Latitude']=drt['Duct_miss_lat']
        df1['Duct_miss_loc_Manual_Longitude']=drt['Duct_miss_long']
        df1['Duct_miss_ch_from']=drt['Duct_miss_ch_from']
        df1['Duct_miss_ch_to']=drt['Duct_miss_ch_to']
        df1['Duct_miss_ch_Length']=drt['Duct_miss_len']
        df1['Remark']=drt['Remark']
        df1['Zone_Name']=zone
        df1['Mandal_Name']=mandal
        df1['To_GP']=to_gp
        df1['Span_ID']=span_id

        df1.reset_index(drop=True,inplace=True)

        try:
            for i in range(len(df1)):
                if pd.isnull(df1.loc[i,'Length']) or df1.loc[i,'Length']==0:
                    if type(df1.loc[i,'ch_to'])==int and type(df1.loc[i,'ch_from'])==int:
                        df1.loc[i,'Length']=abs(df1.loc[i,'ch_to']-df1.loc[i,'ch_from'])

        except:
            print("Problem in correction of DRT")                
       
        return df1

    def create_blo(blo):
        zone=''
        mandal=''
        to_gp=''
        span_id=''
        """
        for i in range(4,12):
            if len(blo.columns)<i:
                break
            zone_mandal=blo.loc[4,blo.columns[i]]
            # print(zone_mandal)
            try:
                zone=zone_mandal.split('/')[0]
                mandal=zone_mandal.split('/')[1]
                to_gp=zone_mandal.split('/')[2]
            # 
                # 
            except:
                print('Something')
            
            try:
                span_id=blo.loc[6,blo.columns[i]]
            except:
                print('Problem in SpanID')
            if len(zone)>0:
                break
        
        blo=blo[12:]
        """
        j=0
        columns_={}
        for i in blo.columns:
            if j==0:
                columns_[i]='S_no'
            elif j==1:
                columns_[i]='Ch_from'
            elif j==2:
                columns_[i]='Ch_to'
            elif j==3:
                columns_[i]='Chb_from'
            elif j==4:
                columns_[i]='Chb_to'
            elif j==5:
                columns_[i]='len'
            elif j==6:
                columns_[i]='size'
            elif j==7:
                columns_[i]='cab_id'
            elif j==8:
                columns_[i]='cab_st'
            elif j==9:
                columns_[i]='cab_end'
            elif j==10:
                columns_[i]='cab_len'
            elif j==11:
                columns_[i]='cha_st'
            elif j==12:
                columns_[i]='cha_end'
            elif j==13:
                columns_[i]='cha_loop'
            elif j==14:
                columns_[i]='chb_st'
            elif j==15:
                columns_[i]='chb_end'
            elif j==16:
                columns_[i]='chb_loop'
            # elif j==17:
            #     columns_[i]='Remark'
            
            j+=1
           
        # print(blo.columns[17])
        blo.rename(columns=columns_,inplace=True)
        #blo.to_csv("Blow after col naming.csv")
        blow=blo[:]
        def remove_noise(blo):
            blo.reset_index(drop=True,inplace=True)
            index=[]
            for i in range(len(blo)):
                if type(blo.loc[i,'Ch_from'])==int or type(blo.loc[i,'Ch_to'])==int or type(blo.loc[i,'len'])==int or type(blo.loc[i,'cab_end'])==int:
                    blo.at[i,'S_no']=88 


                if type(blo.loc[i,'S_no'])!=int or (pd.isna(blo.loc[i,'size'])) or type(blo.loc[i,'cab_end'])!=int:
                    index.append(i)
                # elif type(blo.loc[i,'Ch_from'])!=int and type(drt.loc[i,'Duct_miss_ch_from'])!=int and type(drt.loc[i,'Duct_dam_ch_from'])!=int:
                #     index.append(i)
            return blo.drop(index,axis=0)
        
        blo=remove_noise(blo)  
        #blo.to_csv("Blow after noise removal.csv")
        df1=pd.DataFrame(columns=['prikey', 'Key', 'Survey Duration', 'User', 'Upload Time',
        'Survey Name', '_scheduled_start', 'Version', 'Complete',
       'Survey Notes', 'Location Trigger', 'Instance Name', '_start', '_end',
       '_device', 'instanceid', 'Package_Name', 'Zone_Name', 'District_Name',
       'Mandal_Name', 'From_GP', 'To_GP', 'Span_ID', 'Chainage_From',
       'Chainage_To', 'Length', 'chamber_from', 'chamber_to', 'size_of_ofc',
       'ofc_cable_id', 'cable_len_start', 'cable_len_end',
       'Total_cable_length', 'chamber_a_end_reading',
       'chamber_a_entry_reading', 'chamber_a_end_slack_loop_length',
       'chamber_b_entry_reading', 'chamber_b_end_reading',
       'chamber_b_end_slack_loop_length', 'Remarks'])
        df1['Chainage_From']=blo['Ch_from']
        df1['Chainage_To']=blo['Ch_to']       
        df1['chamber_from']=blo['Chb_from']
        df1['chamber_to']=blo['Chb_to']
        df1['Length']=blo['len']
        df1['size_of_ofc']=blo['size']
        df1['ofc_cable_id']=blo['cab_id']
        df1['cable_len_start']=blo['cab_st']
        df1['cable_len_end']=blo['cab_end']
        df1['Total_cable_length']=blo['cab_len']
        df1['chamber_a_end_reading']=blo['cha_st']
        df1['chamber_a_entry_reading']=blo['cha_end']
        df1['chamber_a_end_slack_loop_length']=blo['cha_loop']
        df1['chamber_b_entry_reading']=blo['chb_st']
        df1['chamber_b_end_reading']=blo['chb_end']
        df1['chamber_b_end_slack_loop_length']=blo['chb_loop']
        # df1['Remarks']=blo['Remark']
        df1['Zone_Name']=zone
        df1['Mandal_Name']=mandal
        df1['To_GP']=to_gp
        df1['Span_ID']=span_id
        #df1['size_of_ofc']=df1['size_of_ofc'].str.replace(' ','')
        #blo.to_csv('blo123.csv')
        #df1=corrector(df1,'Chainage_From','Chainage_To','Length')
        #df1=corrector(df1,'cable_len_start','cable_len_end','Total_cable_length')
        df1.reset_index(drop=True,inplace=True)
        for i in range(len(df1)):
            if (pd.isnull(df1.loc[i,'Length'])) or (df1.loc[i,'Length']==0):
                if type(df1.loc[i,'Chainage_To'])==int and type(df1.loc[i,'Chainage_From'])==int:
                    df1.loc[i,'Length']=abs(df1.loc[i,'Chainage_To']-df1.loc[i,'Chainage_From'])
        df1.reset_index(drop=True,inplace=True)
        #df1.to_csv("blo_c.csv")

        try:
            for i in range(len(df1)):
                if (pd.isnull(df1.loc[i,'Total_cable_length'])) or (df1.loc[i,'Total_cable_length']==0):
                    if type(df1.loc[i,'cab_st'])==int and type(df1.loc[i,'cab_end'])==int:
                        df1.loc[i,'Total_cable_length']=abs(df1.loc[i,'cab_end']-df1.loc[i,'cab_st'])            

        except:
            print("problems in correction of blowing")                
        df1.reset_index(drop=True,inplace=True)

        def generate_joint_closer(blow):
            joint_closer=[]
            blow=blow.reset_index(drop=True)   
            x=blow.apply(lambda row: row.astype(str).str.lower().str.replace(' ','').str.contains('jointclosure').any(),axis=0)
            
            
            col=False
            j=0
            for i in x:
                
                if i is True and j>1:
            #         print(1)
                    col=i
                j+=1
                if col:
                    col=x.index[j]
                    joint_closer=blow[blow.apply(lambda row: row.astype(str).str.lower().str.replace(' ','').str.contains('jointclosure').any(),axis=1)][blow.columns[j:]]
            #         print(joint_closer)
                    break
            return joint_closer        
        joint_closer=generate_joint_closer(blow)

        return (df1,joint_closer)