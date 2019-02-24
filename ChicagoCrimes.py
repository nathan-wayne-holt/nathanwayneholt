import csv, time, operator, random, time
import numpy as np
import csvsort
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf

def sortFile():
    csvsort.csvsort('Crimes_-_2001_to_present.csv', [2], output_filename='sortedtest.csv', has_header=True)

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

def createIUCRDict():
    with open('IUCR_codes.csv') as csvfile:
        fieldnamelist = ['IUCR','Primary Description','Secondary Description','Index Code']
        reader = csv.DictReader(csvfile, fieldnames=fieldnamelist)

        IUCRDict = {}
        i = 0
        for row in reader:
            if len(row['IUCR']) == 4:
                IUCRDict[row['IUCR']] = i
                if row['IUCR'] == '5007':
                    i+= 1
                    IUCRDict['5008'] = i
                if row['IUCR'] == '5004':
                    i+= 1
                    IUCRDict['5005'] = i
                if row['IUCR'] == '5011':
                    i+= 1
                    IUCRDict['5013'] = i
                if row['IUCR'] == '502T':
                    i+= 1
                    IUCRDict['5073'] = i
                    i+= 1
                    IUCRDict['5093'] = i
                    i+= 1
                    IUCRDict['5094'] = i
                if row['IUCR'] == '5112':
                    i+= 1
                    IUCRDict['5113'] = i
                    i+= 1
                    IUCRDict['5114'] = i
                if row['IUCR'] == '5132':
                    i+= 1
                    IUCRDict['9901'] = i
            else:
                IUCRDict['0' + row['IUCR']] = i
                if '0'+row['IUCR'] == '0820':
                    i+= 1
                    IUCRDict['0830'] = i
                    i+= 1
                    IUCRDict['0840'] = i
                    i+= 1
                    IUCRDict['0841'] = i
                    i+= 1
                    IUCRDict['0842'] = i
                    i+= 1
                    IUCRDict['0843'] = i
                if '0'+row['IUCR'] == '0584':
                    i+= 1
                    IUCRDict['0585'] = i
                if '0'+row['IUCR'] == '0498':
                    i+= 1
                    IUCRDict['0499'] = i
            i += 1
            
        return IUCRDict

def createTimeDict():
    #returns a dict serialized with the date
    timeDict = {}
    i = 0
    for j in range(0,2):
        if j == 0:
            tag = 'AM'
        elif j == 1:
            tag = 'PM'
        for hour in range(1,13):
            for minute in range(0,60):
                for second in range(0,60):
                    if hour < 10:
                        #Pad index of hour
                        if minute < 10:
                            #Pad index of minute
                            if second < 10:
                                #Pad index of second
                                index = '0'+str(hour)+':0'+str(minute)+':0'+str(second)+tag
                            else:
                                index = '0'+str(hour)+':0'+str(minute)+':'+str(second)+tag
                        else:
                            if second < 10:
                                #Pad index of second
                                index = '0'+str(hour)+':'+str(minute)+':0'+str(second)+tag
                            else:
                                index = '0'+str(hour)+':'+str(minute)+':'+str(second)+tag
                            
                    else:
                        if minute < 10:
                            #pad index of minute
                            if second < 10:
                                #Pad index of second
                                index = str(hour)+':0'+str(minute)+':0'+str(second)+tag
                            else:
                                index = str(hour)+':0'+str(minute)+':'+str(second)+tag
                                
                        else:
                            if second < 10:
                                #Pad index of second
                                index = str(hour)+':'+str(minute)+':0'+str(second)+tag
                            else:
                                index = str(hour)+':'+str(minute)+':'+str(second)+tag
                    
                    timeDict[index] = i
                    i += 1
    return timeDict

def createDateDict():
    #returns a dict serialized with the date
    dateDict = {}
    i = 0
    for month in range(1,13):
        if month in (1,3,5,7,8,10,12):
            #31 days in a month
            for day in range(1,32):
                if month >= 10:
                    if day >= 10:
                        index = str(month) + "/" + str(day)
                    else:
                        index = str(month) + "/0" + str(day)
                else:
                    if day >= 10:
                        index = '0' + str(month) + "/" + str(day)
                    else:
                       index = '0' + str(month) + "/0" + str(day) 
                dateDict[index] = i
                i += 1
        elif month in (4,6,9,11):
            #30 days in a month
            for day in range(1,31):
                if month >= 10:
                    if day >= 10:
                        index = str(month) + "/" + str(day)
                    else:
                        index = str(month) + "/0" + str(day)
                else:
                    if day >= 10:
                        index = '0' + str(month) + "/" + str(day)
                    else:
                       index = '0' + str(month) + "/0" + str(day) 
                dateDict[index] = i
                i += 1
        elif month == 2:
            #Assume 28 days. None on Leap year?
            for day in range(1,30):
                if month >= 10:
                    if day >= 10:
                        index = str(month) + "/" + str(day)
                    else:
                        index = str(month) + "/0" + str(day)
                else:
                    if day >= 10:
                        index = '0' + str(month) + "/" + str(day)
                    else:
                       index = '0' + str(month) + "/0" + str(day) 
                dateDict[index] = i
                i += 1
    return dateDict

# Make a prediction with coefficients
def predict(row, coefficients):
    zhat = coefficients[0]
    for i in range(len(row)):
        zhat += coefficients[i + 1] * row[i]
    return zhat

def equal_ignore_order(a, b):
    """ Use only when elements are neither hashable nor sortable! """
    unmatched = list(b)
    for element in a:
        try:
            unmatched.remove(element)
        except ValueError:
            return False
    return not unmatched

@timing
def openFile():
    with open('Crimes_-_2001_to_present.csv') as csvfile:
        fieldnamelist = ['ID','Case Number','FullDate','Block','IUCR','Primary Type','Description','Location Description','Arrest','Domestic','Beat','District','Ward','Community Area','FBI Code','X Coordinate','Y Coordinate','Year','Updated On','Latitude','Longitude','Location']
        reader = csv.DictReader(csvfile, fieldnames=fieldnamelist)
        print("CSV file loaded.")

        #row_count = sum(1 for row in reader)
        
        dateDict = createDateDict()
        timeDict = createTimeDict()
        IUCRDict = createIUCRDict()

        maxDate = max(dateDict, key=dateDict.get)
        maxTime = max(timeDict, key=timeDict.get)
        maxIUCR = max(IUCRDict, key=IUCRDict.get)

        dates,times,IUCRs,points = [],[],[],[]
        
        lines = 0
        for row in reader:
            lines += 1
            #Split into different date columns.
            if lines != 1:
                date = row['FullDate'].split()[0].split('/')[0]+'/'+row['FullDate'].split()[0].split('/')[1]
                row['Date'] = dateDict[date]
                dates.append(row['Date'])
                time = row['FullDate'].split()[1]+row['FullDate'].split()[2]
                row['Time'] = timeDict[time]
                times.append(row['Time'])
                #print(row['IUCR'])
                IUCRs.append(IUCRDict[row['IUCR']])
                points.append([row['Date'],row['Time'],IUCRDict[row['IUCR']]])

        originalPoints = points
        points = points[::1000]

        #Intial centroids: first k points
        k = 4
        n = 100
        maxiterations = 1000
        centroids = points[0:k]
        #print(centroids)

        clusters = []
        pointsInClusters,pointsInClustersX,pointsInClustersY,pointsInClustersZ = {},{},{},{}
        for point in points:
            cluster = None
            mindist = None
            i = 0
            for centroid in centroids:
                dist = (point[0]-centroid[0])**2+(point[1]-centroid[1])**2+(point[2]-centroid[2])**2
                if (mindist == None) or (dist < mindist):
                    mindist = dist
                    cluster = i
                i += 1
            clusters.append(cluster)
            try:
                pointsInClusters[cluster].append(point)
                pointsInClustersX[cluster].append(point[0])
                pointsInClustersY[cluster].append(point[1])
                pointsInClustersZ[cluster].append(point[2])
            except KeyError:
                pointsInClusters[cluster] = [point]
                pointsInClustersX[cluster] = [point[0]]
                pointsInClustersY[cluster] = [point[1]]
                pointsInClustersZ[cluster] = [point[2]]
        #print(len(clusters))
        #print(clusters[0:100])

        #reevaluate centroids
        newcentroids = []
        for i in range(0,k):
            numOfPoints = len(pointsInClusters[i])

            xSum,ySum,zSum = 0,0,0
            for point in pointsInClusters[i]:
                xSum += point[0]
                ySum += point[1]
                zSum += point[2]
            xMean = round(xSum / numOfPoints)
            yMean = round(ySum / numOfPoints)
            zMean = round(zSum / numOfPoints)

            newcentroid = [xMean,yMean,zMean]
            newcentroids.append(newcentroid)

        iteration = 1
        while (equal_ignore_order(centroids,newcentroids) != True) and (iteration <= maxiterations):
            centroids = newcentroids
            clusters = []
            pointsInClusters,pointsInClustersX,pointsInClustersY,pointsInClustersZ = {},{},{},{}
            for point in points:
                cluster = None
                mindist = None
                i = 0
                for centroid in centroids:
                    dist = (point[0]/dateDict[maxDate]-centroid[0]/dateDict[maxDate])**2+(point[1]/timeDict[maxTime]-centroid[1]/timeDict[maxTime])**2+(point[2]/IUCRDict[maxIUCR]-centroid[2]/IUCRDict[maxIUCR])**2
                    if (mindist == None) or (dist < mindist):
                        mindist = dist
                        cluster = i
                    i += 1
                clusters.append(cluster)
                try:
                    pointsInClusters[cluster].append(point)
                    pointsInClustersX[cluster].append(point[0])
                    pointsInClustersY[cluster].append(point[1])
                    pointsInClustersZ[cluster].append(point[2])
                except KeyError:
                    pointsInClusters[cluster] = [point]
                    pointsInClustersX[cluster] = [point[0]]
                    pointsInClustersY[cluster] = [point[1]]
                    pointsInClustersZ[cluster] = [point[2]]

            #reevaluate centroids
            newcentroids = []
            for i in range(0,k):
                numOfPoints = len(pointsInClusters[i])

                xSum,ySum,zSum = 0,0,0
                for point in pointsInClusters[i]:
                    xSum += point[0]
                    ySum += point[1]
                    zSum += point[2]
                xMean = round(xSum / numOfPoints)
                yMean = round(ySum / numOfPoints)
                zMean = round(zSum / numOfPoints)

                newcentroid = [xMean,yMean,zMean]
                newcentroids.append(newcentroid)

            print(iteration)
            iteration += 1

        print("It took", iteration-1, "iterations to stabilize")
        print("Centroids:", newcentroids)

        #Plot points with colors for centroids
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(np.array(pointsInClustersX[0]),np.array(pointsInClustersY[0]),np.array(pointsInClustersZ[0]),s=20,c='r',depthshade=True)
        ax.scatter(np.array(pointsInClustersX[1]),np.array(pointsInClustersY[1]),np.array(pointsInClustersZ[1]),s=20,c='b',depthshade=True)
        ax.scatter(np.array(pointsInClustersX[2]),np.array(pointsInClustersY[2]),np.array(pointsInClustersZ[2]),s=20,c='g',depthshade=True)
        ax.scatter(np.array(pointsInClustersX[3]),np.array(pointsInClustersY[3]),np.array(pointsInClustersZ[3]),s=20,c='black',depthshade=True)
        ax.set_xlabel('Dates (MM/DD)')
        ax.set_ylabel('Time HH:MM:SS')
        ax.set_zlabel('IUCR')
        plt.show()

        #find_centers(np.array(points), 10)

        #fig = plt.figure()
        #ax = fig.gca(projection='3d')
        #ax.scatter(np.array(dates)[1::5000],np.array(times)[1::5000],np.array(IUCRs)[1::5000],s=20,c=[1]*len(dates[1::5000]),depthshade=True)
        #ax.set_xlabel('Dates (MM/DD)')
        #ax.set_ylabel('Time HH:MM:SS')
        #ax.set_zlabel('IUCR')
        #plt.show()
        #points = tf.convert_to_tensor(points)







        

        #print(predict(points[0], [0.0, 0.0, 1.0, 1.0]),dates[0],times[0],IUCRs[0])
