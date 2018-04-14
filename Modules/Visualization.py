import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


##################
import os

ApplicationPath = os.getcwd()
ApplicationPath = ApplicationPath[:(len(ApplicationPath)-7)]#since len("modules") = 7 we substract 7

DataPath = ApplicationPath + "Data\\"

################## this block is for to determine the data path in the project folder

ErrorPercentageData = pd.read_csv(DataPath+'ErrorPercentage.csv')
ErrorHeader = ErrorPercentageData.columns
ErrorsYear = ErrorPercentageData.values.tolist()
EstimationData = pd.read_csv(DataPath+'Estimations.csv')
EstimationHeader = EstimationData.columns
EstimationYear = EstimationData.values.tolist()
DataCrash = pd.read_csv(DataPath+"death_crash 2005 - 2010.csv",sep=';')
CrashHeader = DataCrash.columns
Population = [DataCrash[CrashHeader[16]].tolist(),DataCrash[CrashHeader[13]].tolist(),DataCrash[CrashHeader[10]].tolist(),DataCrash[CrashHeader[7]].tolist(),DataCrash[CrashHeader[4]].tolist(),DataCrash[CrashHeader[1]].tolist()]
Death = [DataCrash[CrashHeader[18]].tolist(),DataCrash[CrashHeader[15]].tolist(),DataCrash[CrashHeader[12]].tolist(),DataCrash[CrashHeader[9]].tolist(),DataCrash[CrashHeader[6]].tolist(),DataCrash[CrashHeader[3]].tolist()]
DeathRatio = [[100*Death[j][i]/Population[j][i] for i in range(len(Population[j]))] for j in range(6)]
for i in range (6):
    del ErrorsYear[i][0]
    x = range(49)
    plt.xticks(x,ErrorHeader[1:],rotation = 70)
    plt.bar(x,ErrorsYear[i],width = 1,align='center')
    plt.ylabel('Percent Error')
    plt.xlabel('States')
    plt.title(str(2005+i)+" Percent Death Estimation Error")
    plt.tight_layout()
    plt.grid()
    plt.show()

for i in range (6):
    mpl_fig = plt.figure()
    del EstimationYear[i][0]
    x = np.arange(49)
    plt.xticks(x,EstimationHeader[1:],rotation = 80)
    plt.bar(x+0.5,EstimationYear[i],color = 'b',width=0.5,label = 'Estimation')
    plt.ylabel('Percent Death')
    plt.xlabel('States')
    plt.bar(x,DeathRatio[i],color='g',width=0.5,label = 'Actual Data')
    plt.title(str(2005+i)+" Estimation")
    plt.legend(loc='upper left')
   
    plt.grid()
    plt.tight_layout()
    plt.show()
for i in range (6):
    del ErrorsYear[i][0]
    x = range(49)
    plt.xticks(x,ErrorHeader[1:],rotation = 70)
    plt.bar(x,ErrorsYear[i],width = 1,align='center')
    plt.ylabel('Percent Error')
    plt.xlabel('States')
    plt.title(str(2005+i)+" Percent Death Estimation Error")
    plt.tight_layout()
    plt.grid()
    plt.show()



