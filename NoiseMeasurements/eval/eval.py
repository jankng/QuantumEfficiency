import numpy as np

def fileToArray(i):
	fileName = "Testzelle" + str(i) + ".txt"
	f = open(fileName, "r")
	lns = f.readlines()
	return lns[3:]

def getData():
	#Matrices for data
	w, h = 25, 10;
	monitor = [[0 for x in range(w)] for y in range(h)]
	sample = [[0 for x in range(w)] for y in range(h)]
	
	#file strings
	files = []
	for i in range(1, 26):
		files.append(fileToArray(i))
	
	#parse file strings
	for i in range(25):
		for j in range(10):
			line = files[i][j].split("\t")
			sample[j][i] = float(line[1])
			monitor[j][i] = float(line[2])
	
	ret = [sample, monitor]
	return ret

#retrieve data
data = getData()
sample = data[0]
monitor = data[1]

#arrays to hold averages and std. devs.
avgMonitor = [0 for x in range(10)]
avgSample = [0 for x in range(10)]

stdMonitor = [0 for x in range(10)]
stdSample = [0 for x in range(10)]

#compute average value for monitor and sample voltage
for i in range(len(sample)):
	avgMonitor[i] = np.average(monitor[i])
	avgSample[i] = np.average(sample[i])
	
#compute std. dev. for monitor and sample voltage
for i in range(len(sample)):
	stdMonitor[i] = np.std(monitor[i])
	stdSample[i] = np.std(sample[i])
	
	
#print (avgMonitor)
#print(stdMonitor)

print("Wavelength \t Sample Avg \t Sample Std \t Monitor Avg \t Monitor Std")
for i in range(len(avgMonitor)):
	print(300 + i*100, end='\t')
	print(round(avgSample[i], 5), end='\t')
	print(round(stdSample[i], 5), end='\t')
	print(round(avgMonitor[i], 5), end='\t')
	print(round(stdMonitor[i], 5))
	