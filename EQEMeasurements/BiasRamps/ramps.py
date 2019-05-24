import matplotlib.pyplot as plt

REFERENZ = "./ReferenzDSR.txt"
SAMPLE = "PERC5V.txt"
KALIBDATEI = "../Temperature/Kalibrierdatei.txt"
AM15PATH = "../../GivenData/spectrum.csv"
#JEXP = 37.02 #AlBSF
JEXP = 38.582 #PERC

def fileToArray(fileName, n):
	with open(fileName, encoding="utf8", errors='ignore') as f:#f = open(fileName, "r")
		lns = f.readlines()
		return lns[n:]
	
def getData(temp):
	data = fileToArray(temp, 3)
	
	x = []
	y = []
	z = []
	
	for line in data:
		buffer = line.split('\t')
		x.append(float(buffer[0]))
		y.append(float(buffer[1]))
		z.append(float(buffer[2]))
	
	ret = [x, y, z]
	
	return ret
	
def makePlots():		
	referenz = getData(REFERENZ)
	sample = getData(SAMPLE)

	Rref = []
	Rspl = []
	Rcoefs = []

	for i in range(len(referenz[1])):
		Rref.append(referenz[1][i] / referenz[2][i])
		Rspl.append(sample[1][i] / sample[2][i])
		Rcoefs.append(Rspl[i] / Rref[i])
		
	for i in range(len(Rref)):
		print(str(referenz[0][i]) + "\t" + str(Rcoefs[i]))
		

	axes = plt.gca()
	axes.set_xlim([300, 1200])
	axes.set_ylim([0, 0.25])

	plt.plot(sample[0], sample[1], marker='.')
	plt.plot(referenz[0], referenz[1], marker='.')
	plt.show()
	

def plotDSR(eqe):
	axes = plt.gca()
	axes.set_xlim([300, 1200])
	axes.set_ylim([0, 10])

	plt.plot(eqe[0], eqe[1], marker='.')
	#plt.plot(referenz[0], referenz[1], marker='.')
	plt.show()

	
#returns s_ref in mA W-1 m2
def getKalib():
	kalib = fileToArray(KALIBDATEI, 24)
	x = []
	y = []
	for i in range(len(kalib)):
		if i % 2 == 0:
			buffer = kalib[i].split("\t")
			x.append(float(buffer[0]))
			y.append(float(buffer[1]))
	
	ret = [x, y]
	return ret
	
def getDSR(sampleFile):
	rawSample = getData(sampleFile)
	rawRef = getData(REFERENZ)
	rcoef = [[], [], [], []]
	for i in range(len(rawSample[1])):
		rcoef[0].append(rawSample[0][i])
		rcoef[1].append(rawSample[1][i] / rawSample[2][i])
		rcoef[2].append(rawRef[1][i] / rawRef[2][i])
		
	dsr = [[], []]
	sref = getKalib()
	for i in range(len(sref[0])):
		if i % 5 == 0 and sref[0][i] > 301 and sref[0][i] < 1101:
			rcoef[3].append(sref[1][i])
		
	for i in range(len(rcoef[0])):
		dsr[0].append(rcoef[0][i])
		dsr[1].append((rcoef[1][i] / rcoef[2][i]) * rcoef[3][i])
		
	return dsr
