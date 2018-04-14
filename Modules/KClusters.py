print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

n_neighbors = 5

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
# import some data to play with
iris = datasets.load_iris()
ARRAY = np.array(DataWeather.values.tolist())

NewARRAY = ARRAY[:,[6,12]]
print(NewARRAY.astype(np.float))
NewARRAY.astype(np.float)
print(iris.target)
DeathARRAY = np.array(Death[0])
print(DeathARRAY)
print(len(DeathARRAY))
print(len(NewARRAY))
X = NewARRAY.astype(np.float)#iris.data[:, :2]  # we only take the first two features. We could
                      # avoid this ugly slicing by using a two-dim dataset
y = DeathARRAY#iris.target

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("3-Class classification (k = %i, weights = '%s') 2010"
              % (n_neighbors, weights))
    plt.xlabel("Precipitation")
    plt.ylabel("Temperature")

plt.show()