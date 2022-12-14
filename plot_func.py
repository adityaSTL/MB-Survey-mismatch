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