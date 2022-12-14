


def check_errors(df):
    #errors=0
    case=""
    count=0
    for i in df.index:
        if df['survey'][i]==1 and pd.isnull(df['drt'][i]) and (pd.isnull(df['hdd'][i]) or pd.isnull(df['ot'][i])):
            case+='a'
            
        elif (df['survey'][i]==1) and (df['drt'][i]>=3):
            case+='b'
            
        elif df['survey'][i]==1 and  df['drt'][i]==2:
            case+='c'
        
        elif df['survey'][i]==2 and  pd.isnull(df['drt'][i]) and (pd.isnull(df['hdd'][i]) or pd.isnull(df['ot'][i])):
            case+='d'
            
        elif df['survey'][i]==2 and df['drt'][i]>=3 and (pd.isnull(df['hdd'][i]) or pd.isnull(df['ot'][i])):
               case+='e'    
        
        elif df['survey'][i]==2 and df['drt'][i]==2 and (df['hdd'][i]==1 or df['ot'][i]==1):
            case+='f'
            
        elif df['survey'][i]==2 and df['drt'][i]==1:
            case+='g'   
            
        elif pd.isnull(df['survey'][i]) and ((not pd.isnull(df['drt'][i])) or (not pd.isnull(df['ot'][i])) or (not pd.isnull(df['hdd'][i]))):
            case+='h'
            
        else:
            case+='p'
            pass
    
    return case    

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