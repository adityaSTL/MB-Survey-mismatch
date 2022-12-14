import os


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

def check_errorsmb(df):
    case=""
    count=0
    for i in df.index:
        #OT and HDD
        if (not pd.isnull(df['hdd'][i]) and not pd.isnull(df['ot'][i])):
            case+='a'
            
        #Miss+Dam    
        elif (df['drt'][i]==4) and (df['drt'][i]==3):
            case+='b'
         
        #Miss+Sup
        elif df['drt'][i]==1 and  df['drt'][i]==4:
            case+='c'
        
        #Miss and no ot/hdd
        elif df['drt'][i]==3 and  ( (pd.isnull(df['hdd'][i]) or pd.isnull(df['ot'][i]))):
            case+='d'
         
        #Dam and no ot/hdd
        elif df['drt'][i]==4 and  ( (pd.isnull(df['hdd'][i]) or pd.isnull(df['ot'][i]))):
            case+='e'   
        
        #Proper drt and ot/hdd
        elif df['drt'][i]==2 and  ( (not pd.isnull(df['hdd'][i]) or (not pd.isnull(df['ot'][i])))):
            case+='f'
        
        #sup+ot/hdd
        elif df['drt'][i]==1 and  ( (not pd.isnull(df['hdd'][i]) or (not pd.isnull(df['ot'][i])))):
            case+='g'
            
        elif (df['drt'][i]==4) and (df['drt'][i]==3):
            case+='h'
            
        else:
            case+='p'
            pass
    
    return case  

def called_mb(file1):
    global logs
    
    for j in os.listdir(file1):
            case=""
            span_loc=os.path.join(file1,j)
            print(span_loc)
#             try:
            df1=common_area("sur_loc",span_loc,j[:-5])
            logs+="DF generated in "+j[:-5]+"\n"
            df1.to_excel('mb_final_df.xlsx')
            case+=check_errorsmb(df1)
            case+='Z'
            #print(case)
            sound(case)
            plot("sur_loc",span_loc,j[:-5])
#             except:
#                 logs+="Not able to call common_area funtion. Terminated comparison for "+j+". Report Format error."
            logs+="\n--------------------------------------------------------------------------------------\n"
    return logs       
