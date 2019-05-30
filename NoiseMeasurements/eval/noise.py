import numpy as np

def fileToArray(i, fileName):
	fileName = "../" + fileName + str(i) + ".txt"
	f = open(fileName, "r")
	lns = f.readlines()
	return lns[3:]

def getData(fileName):
	#Matrices for data
	w, h = 25, 10;
	monitor = [[0 for x in range(w)] for y in range(h)]
	sample = [[0 for x in range(w)] for y in range(h)]
	
	#file strings
	files = []
	for i in range(1, 26):
		files.append(fileToArray(i, fileName))
	
	#parse file strings
	for i in range(25):
		for j in range(10):
			line = files[i][j].split("\t")
			sample[j][i] = float(line[1])
			monitor[j][i] = float(line[2])
	
	ret = [sample, monitor]
	return ret

def getNoise(fileName):
	#retrieve data
	data = getData(fileName)
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
	
	#print(data)

	wavelengths = []
	#print("Wavelength \t Sample Avg \t Sample Std \t Monitor Avg \t Monitor Std")
	for i in range(len(avgMonitor)):
		wavelengths.append(300 + i*100)
		#print(300 + i*100, end='\t')
		#print(round(avgSample[i], 5), end='\t')
		#print(round(stdSample[i], 5), end='\t')
		#print(round(avgMonitor[i], 5), end='\t')

		#print(round(stdMonitor[i], 5))
	
	return [wavelengths, avgSample, stdSample, avgMonitor, stdMonitor]

def readKalib(fileName, n):
	with open(fileName, encoding="utf8", errors='ignore') as f:#f = open(fileName, "r")
		lns = f.readlines()
		return lns[n:]

def getKalib():
	kalib = readKalib("Kalibrierdatei.txt", 24)
	
	x = []
	y = []
	for i in range(len(kalib)):
		if i % 20 == 0:
			buffer = kalib[i].split("\t")
			x.append(float(buffer[0]))
			y.append(float(buffer[1]))
	
	ret = [x, y]
	return ret

def getDSRErrors():
	sample = getNoise("Testzelle")
	ref = getNoise("Referenz")
	kalib = getKalib()
	
	wavelengths = []
	for i in range(len(kalib[0])):
		wavelengths.append(kalib[0][i])
	
	dsr = []
	for i in range(len(kalib[0])):
		Rtest = sample[1][i] / sample[3][i]
		Rref = ref[1][i] / ref[3][i]
		
		dsr.append(Rtest / Rref * kalib[1][i])
		
	errs = []
	for i in range(len(kalib[0])):
		Sr = ref[1][i]
		dSr = ref[2][i] * 1
		Smr = ref[3][i]
		dSmr = ref[4][i] * 1
		
		St = sample[1][i]
		dSt = sample[2][i] * 1
		Smt = sample[3][i]
		dSmt = sample[4][i] * 1
		
		errs.append(np.sqrt((dSr / Sr)**2 + (dSmr / Smr)**2 + (dSt / St)**2 + (dSmt / Smt)**2 + 0.05**2))
		
	return [wavelengths, dsr, errs]

test = getDSRErrors()
print(test)