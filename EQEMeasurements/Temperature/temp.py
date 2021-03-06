import matplotlib.pyplot as plt

REFERENZ = "ReferenzDSR.txt"
SAMPLE = "../BiasRamps/PERC11V.txt"
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

#returns Spectral photon irradiance  (m-2s-1nm-1) 
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
	
#returns R_test / R_ref w/o units
def getCoefs(sampleFile):
	referenz = getData(REFERENZ)
	sample = getData(sampleFile)

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
		integral = integral + 10 * (spectrum[1][i]*eqe[1][i] + spectrum[1][i+1]*eqe[1][i+1]) / 2

	#remember to convert jexp from mA cm-2 to A m-2 -> jexp = jexp*10 in the next eqn
	ret = 10*jexp / (integral * 1.602e-19)
	#print(ret)
	return ret

#returns relative EQE no units
def getRelativeEQE(sampleFile):

	coefs = getCoefs(sampleFile)
	calib = getKalib()
	eqe = [[], []]

	konstante = 3099.250936 #check unit of area (cm or m)
	for i in range(len(coefs)):
		eqe[0].append(calib[0][i])
		eqe[1].append(calib[1][i] * coefs[i] * konstante / calib[0][i])
		
	return eqe

#returns absolute EQE no units
def getAbsoluteEQE(sampleFile, jexp):
	rel = getRelativeEQE(sampleFile)
	spect = getAM15()
	scale = getScaling(rel, spect, jexp)
	for i in range(len(rel[1])):
		rel[1][i] = rel[1][i] * scale
	
	return rel

def plotEQE(eqe):
	axes = plt.gca()
	axes.set_xlim([300, 1200])
	axes.set_ylim([0, 0.25])

	plt.plot(eqe[0], eqe[1], marker='.')
	#plt.plot(referenz[0], referenz[1], marker='.')
	plt.show()


def getAbsEQEErrs(sampleFile, jexp):
	eqe = getAbsoluteEQE(sampleFile, jexp)
	relerrs = [0.35768865800478594, 0.6031851453286338, 0.050121630903570295, 0.05006760686043129, 0.05000930361255885, 0.05002394779546438, 0.050041635379218574, 0.050028121793822516, 0.05009705404734112, 0.07593144016100795]
	errs = []
	
	j = 0
	for i in range(len(eqe[0])):
		if i == 5 or ((i - 5) % 10 == 0 and i > 0):
			j = j + 1
			
		errs.append(eqe[1][i] * relerrs[j])
			
	return [eqe[0], eqe[1], errs]