import matplotlib.pyplot as plt

REFERENZ = "ReferenzDSR.txt"
SAMPLE = "PERC25.txt"
KALIBDATEI = "Kalibrierdatei.txt"
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

def getAM15():
	fileName = AM15PATH
	f = open(fileName, "r")
	data = f.readlines();
	
	ret = [[], []]
	for i in range(len(data[40:1041])):
		if (i % 20 == 0) or (i > 201 and i % 10 == 0):
			buffer = data[40:1041][i].split(',')
			#print(buffer)
			ret[0].append(float(buffer[0]))
			ret[1].append(float(buffer[2]))

	return ret
	
def getCoefs():
	referenz = getData(REFERENZ)
	sample = getData(SAMPLE)

	Rref = []
	Rspl = []
	Rcoefs = []

	for i in range(len(referenz[1])):
		Rref.append(referenz[1][i] / referenz[2][i])
		Rspl.append(sample[1][i] / sample[2][i])
		Rcoefs.append(Rspl[i] / Rref[i])
		
	#for i in range(len(Rref)):
		#print(str(referenz[0][i]) + "\t" + str(Rcoefs[i]))
	
	return Rcoefs
	
def getScaling(eqe, spectrum, jexp):
	# computing scaling factor
	integral = 0
	for i in range(len(eqe[0]) - 1):
		integral = integral + 1 * (spectrum[1][i]*eqe[1][i] + spectrum[1][i+1]*eqe[1][i+1]) / 2

	ret = jexp / (integral * 1.602e-19)
	#print(ret)
	return ret

def getRelativeEQE():

	coefs = getCoefs()
	calib = getKalib()
	eqe = [[], []]

	konstante = 309.9250 #check unit of area (cm or m)
	for i in range(len(coefs)):
		eqe[0].append(calib[0][i])
		eqe[1].append(calib[1][i] * coefs[i] * konstante / calib[0][i])
		
	return eqe

def getAbsoluteEQE():
	rel = getRelativeEQE()
	spect = getAM15()
	scale = getScaling(rel, spect, JEXP)
	for i in range(len(rel[1])):
		rel[1][i] = rel[1][i] * scale
	
	return rel

def plotEQE(eqe):
	axes = plt.gca()
	axes.set_xlim([300, 1200])
	axes.set_ylim([0, 1])

	plt.plot(eqe[0], eqe[1], marker='.')
	#plt.plot(referenz[0], referenz[1], marker='.')
	plt.show()


	
	
eqe = getAbsoluteEQE()
plotEQE(eqe)