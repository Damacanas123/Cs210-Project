from scipy.stats.stats import pearsonr
import numpy as np
from math import sqrt


def CopyList(Original):
    Copy = []
    for i in Original:
        temp = []
        for j in i:
            ElmTemp = j
            temp.append(ElmTemp)
        Copy.append(temp)
    return Copy

def MultipleCorrCoef(*args): # args is a list of arguements
    # first enter dependent variable and then independent variables
    clist = [] # correlation coeffs between dependent variable and independent variables
    x = []
    for i in range(len(args)-1) : 
        x.append(args[i+1]) # since dependent variable is the first element we are creating ceofficientt matrix from the rest
        clist.append(pearsonr(args[0], args[i+1])[0])
        
    CnpArray = np.array(clist)
    CtransPose = CnpArray.reshape(len(CnpArray),1)
    R = (np.corrcoef(x))
    Rinverse = np.linalg.inv(R)
    Rinv_times_C = np.dot(Rinverse,CtransPose)
    Ctrans_times_Rinv_times_C = np.dot(CnpArray,Rinv_times_C)   # CT*Rinv*C = correlation_coefficient^2
    return sqrt(Ctrans_times_Rinv_times_C[0])

##################
import os

ApplicationPath = os.getcwd()
ApplicationPath = ApplicationPath[:(len(ApplicationPath)-7)]#since len("modules") = 7 we substract 7

DataPath = ApplicationPath + "Data\\"

################## this block is for to determine the data path in the project folder

import pandas as pd

##################   SEAT BELT   #########################
DataBelt = pd.read_csv(DataPath+"US Seat Belt Usage 2003-2010 v2.csv")
BeltHeader = DataBelt.columns
States = DataBelt[BeltHeader[0]].tolist()

BeltRatio = [DataBelt[BeltHeader[3]].tolist(), DataBelt[BeltHeader[4]].tolist(),DataBelt[BeltHeader[5]].tolist(), DataBelt[BeltHeader[6]].tolist(),DataBelt[BeltHeader[7]].tolist(),DataBelt[BeltHeader[8]].tolist()]
BeltRatioFixed = [[100 - i for i in BeltRatio[j]] for j in range(6)] #Ratio of passengers that do not use seat belt


##################   CRASH   #########################
DataCrash = pd.read_csv(DataPath+"death_crash 2005 - 2010.csv",sep=';')
CrashHeader = DataCrash.columns

Population = [DataCrash[CrashHeader[16]].tolist(),DataCrash[CrashHeader[13]].tolist(),DataCrash[CrashHeader[10]].tolist(),DataCrash[CrashHeader[7]].tolist(),DataCrash[CrashHeader[4]].tolist(),DataCrash[CrashHeader[1]].tolist()]
Death = [DataCrash[CrashHeader[18]].tolist(),DataCrash[CrashHeader[15]].tolist(),DataCrash[CrashHeader[12]].tolist(),DataCrash[CrashHeader[9]].tolist(),DataCrash[CrashHeader[6]].tolist(),DataCrash[CrashHeader[3]].tolist()]
DeathRatio = [[100*Death[j][i]/Population[j][i] for i in range(len(Population[j]))] for j in range(6)]
################## TEMPERATURE ########################
DataWeather = pd.read_csv(DataPath +"temp_rain_new.csv")
WeatherHeader = DataWeather.columns

Precipitation = [DataWeather[WeatherHeader[1]].tolist(),DataWeather[WeatherHeader[2]].tolist(),DataWeather[WeatherHeader[3]].tolist(),DataWeather[WeatherHeader[4]].tolist(),DataWeather[WeatherHeader[5]].tolist(),DataWeather[WeatherHeader[6]].tolist()]
Temperature = [DataWeather[WeatherHeader[7]].tolist(),DataWeather[WeatherHeader[8]].tolist(),DataWeather[WeatherHeader[9]].tolist(),DataWeather[WeatherHeader[10]].tolist(),DataWeather[WeatherHeader[11]].tolist(),DataWeather[WeatherHeader[12]].tolist()]

import matplotlib.pyplot as plt
fEstimation = open('Estimations.csv', 'w')
fEstimation.write('Year,') 
fErrorPercent = open('ErrorPercentage.csv','w')
fErrorPercent.write('Year,') 
for i in range(len(States)):
    fEstimation.write(States[i])
    fErrorPercent.write(States[i])
    if i !=48:
        fEstimation.write(',')
        fErrorPercent.write(',')

for i in range(6):
    
    year = str(2005+i)
    fEstimation.write('\n'+year+',')
    fErrorPercent.write('\n'+year+',')
    print(len(States))
    for j in range(len(States)):
        print(j)
        print(i)
        StateParams = [BeltRatioFixed[i][j],Temperature[i][j],Precipitation[i][j],DeathRatio[i][j]]
        print(len(Temperature[i]))
        LoopBeltRatioFixed = []
        LoopTemperature = []
        LoopPrecipitation = []
        LoopDeathRatio = []
        
        LoopBeltRatioFixed = CopyList(BeltRatioFixed)
        LoopTemperature = CopyList(Temperature)
        LoopPrecipitation = CopyList(Precipitation)
        LoopDeathRatio = CopyList(DeathRatio)
        del LoopBeltRatioFixed[i][j]
        del LoopTemperature[i][j]
        del LoopPrecipitation[i][j]
        del LoopDeathRatio[i][j]
        print(LoopTemperature[i])
        
        
        print("#correlation coefficient and confidence interval of BeltRatio"+year+" and DeathRatio"+year+" : " )
        print(pearsonr(LoopBeltRatioFixed[i],LoopDeathRatio[i]))
        print("Correlation coefficient and confidence interval of Temperature"+year+" and DeathRatio"+year+" : ")
        print(pearsonr(LoopTemperature[i],LoopDeathRatio[i]))
        print("Correlation coefficient and confidence interval of Precipitation"+year+" and Death"+year+" : ")
        print(pearsonr(LoopPrecipitation[i],LoopDeathRatio[i]))
        print("Death estimation with population and beltratiofixed : ",year," " ,MultipleCorrCoef(LoopDeathRatio[i],LoopTemperature[i],LoopBeltRatioFixed[i],LoopPrecipitation[i]))
        
        X = np.column_stack([LoopBeltRatioFixed[i],LoopTemperature[i],LoopPrecipitation[i]]+[[1]*len([LoopBeltRatioFixed[i],LoopTemperature[i],LoopPrecipitation[i]][0])])
        RegCoefs = np.linalg.lstsq(X,LoopDeathRatio[i])[0]
        print ("Coefficients : ",RegCoefs)
        
        ############PROBLEM WITH PLOTTING BECAUSE THE LISTS ARE NOT SORTED 
        ############SOLVED
        
        
    ############Estimations
        estimation = RegCoefs[0]*StateParams[0]+RegCoefs[1]*StateParams[1]+RegCoefs[2]*StateParams[2]+RegCoefs[3]
        Error = StateParams[3]-estimation
        PercentError = abs((Error / StateParams[3])*100)
        print("Estimation : ",estimation)
        print("Actual Data : ",StateParams[3])
        print("Error : ",Error)
        print("Percent Error : ", PercentError)
        print("\n\n")
        fEstimation.write(str(estimation))
        fErrorPercent.write(str(PercentError))
        if j !=48:
            fEstimation.write(',')
            fErrorPercent.write(',')
    
    fit = np.polyfit(Precipitation[i],DeathRatio[i],1)
    fit_fn = np.poly1d(fit) 
    Estimation = fit_fn(sorted(Precipitation[i]))
    plt.scatter(Precipitation[i],DeathRatio[i])
    plt.plot(sorted(Precipitation[i]),Estimation,c='r')
    plt.xlabel("Precipitation "+year)
    plt.ylabel("Death Ratio "+year)
    plt.title(year)
    plt.show()
    plt.close()
fEstimation.close()
fErrorPercent.close()

#calculate multiple correlation ceofficients
for i in range(6):
    print(MultipleCorrCoef(DeathRatio[i],BeltRatioFixed[i],Temperature[i],Precipitation[i]))
    
    
    


