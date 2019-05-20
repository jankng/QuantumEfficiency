def getAM15():
	fileName = "AM15g_Spektrum.txt"
	f = open(fileName, "r")
	data = f.readlines();
	
	ret = [[], []]
	for i in range(len(data[40:1041])):
		if i % 20 == 0:
			buffer = data[40:1041][i].split(' ')
			ret[0].append(float(buffer[0]))
			ret[1].append(float(buffer[1]))

	return ret


#spectrum = getAM15()
#for i in range(len(spectrum[0])):
#	print(str(spectrum[0][i]) + "\t" + str(spectrum[1][i]))

#spectrum = getAM15()
#print(spectrum)