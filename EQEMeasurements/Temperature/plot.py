import matplotlib.pyplot as plt

REFERENZ = "ReferenzDSR.txt"
SAMPLE = "AlBSF25.txt"
KALIBDATEI = "Kalibrierdatei.txt"

def fileToArray(fileName, n):
	f = open(fileName, "r")
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
	

coefs = getCoefs()
calib = getKalib()
eqe = [[], []]

for i in range(len(coefs)):
	eqe[0].append(calib[0][i])
	eqe[1].append(calib[1][i] * coefs[i])
	
axes = plt.gca()
axes.set_xlim([300, 1200])
axes.set_ylim([0, 5])

plt.plot(eqe[0], eqe[1], marker='.')
#plt.plot(referenz[0], referenz[1], marker='.')
plt.show()