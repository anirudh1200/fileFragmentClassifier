import os
import math
import re

files = os.listdir("./files/training1")
count = 0
total = len(files)
for file in files:
	count += 1
	print("Starting " + str(count) + "/" + str(total) + '  ' + file)
	f = open("./files/training1/"+file, "rb")
	raw = b""
	try:
		byte = f.read(1)
		while byte:
			raw += byte
			byte = f.read(1)
	finally:
		f.close()

	histogram = [0] * 256
	for i in range(len(raw)):
		histogram[raw[i]] += 1
	for i in range(len(histogram)):
		histogram[i] /= float(len(raw))

	entropy = 0
	for i in range(len(histogram)):
		if histogram[i] != 0:
			entropy += -histogram[i] * math.log(histogram[i], 2)

	extension = re.match('.*\.(.*)$', file).groups()[0]
	ff = open("./train1.csv", 'a')
	line = ','.join([ str(x) for x in histogram])
	line += ',' + str(entropy)
	line += ',' + str(extension)
	ff.write(line + "\r\n")
