import binascii
import math

img = open("moonroad.bmp", "rb");
out_file = open("edges.bmp", "wb")

stream = []
output = []

Gy = [[-1, -2, -1],[0, 0, 0],[1, 2, 1]]
Gx = [[-1, 0, 1],[-2, 0, 2], [-1, 0, 1]]

try:
	fileSignature = ""

	byte = img.read(1)

	fileSignature += byte.decode("utf-8")
	byte = img.read(1)
	fileSignature += byte.decode("utf-8")

	if fileSignature == "BM":
		fileSize = 0

		byte = img.read(1)
		fileSize += int(binascii.hexlify(byte), 16)
		byte = img.read(1)
		fileSize += int(binascii.hexlify(byte), 16) << 8
		byte = img.read(1)
		fileSize += int(binascii.hexlify(byte), 16) << 16
		byte = img.read(1)
		fileSize += int(binascii.hexlify(byte), 16) << 24

		print(fileSize)

		img.seek(10)
		startOfData = 0 
		byte = img.read(1)
		startOfData += int(binascii.hexlify(byte), 16)
		byte = img.read(1)
		startOfData += int(binascii.hexlify(byte), 16) << 8
		byte = img.read(1)
		startOfData += int(binascii.hexlify(byte), 16) << 16
		byte = img.read(1)
		startOfData += int(binascii.hexlify(byte), 16) << 24

		print(startOfData)

		img.seek(18)
		width = 0
		byte = img.read(1)
		width += int(binascii.hexlify(byte), 16)
		byte = img.read(1)
		width += int(binascii.hexlify(byte), 16) << 8

		print(width)

		img.seek(22)
		height = 0
		byte = img.read(1)
		height += int(binascii.hexlify(byte), 16)
		byte = img.read(1)
		height += int(binascii.hexlify(byte), 16) << 8

		print(height)

		img.seek(startOfData)
		for i in range(width):
			row = []
			
			for j in range(height):
				row.append(int(binascii.hexlify(img.read(1)),16))

			stream.append(row)

		Gx_array = []
		
		for i in range(width):
			row = []
			for j in range(height):
				calcedGx = 0
				lower_i = 0
				upper_i = 3
				lower_j = 0
				upper_j = 3
				if(i == 0):
					lower_i += 1
				if(j == 0):
					lower_j += 1
				if(i == width - 1):
					upper_i -= 1
				if(j == height - 1):
					upper_j -= 1
				for Gi in range(lower_i, upper_i):
					for Gj in range(lower_j, upper_j):
						try:
							calcedGx += Gx[Gi][Gj] * stream[i + Gi - 1][j + Gj - 1]
						except IndexError:
							print("Index Error")
				row.append(abs(calcedGx))
			Gx_array.append(row)
		
		Gy_array = []
		for i in range(width):
			row = []
			for j in range(height):
				calcedGy = 0
				lower_i = 0
				upper_i = 3
				lower_j = 0
				upper_j = 3
				if(i == 0):
					lower_i += 1
				if(j == 0):
					lower_j += 1
				if(i == width - 1):
					upper_i -= 1
				if(j == height - 1):
					upper_j -= 1
				for Gi in range(lower_i, upper_i):
					for Gj in range(lower_j, upper_j):
						try:
							calcedGy += Gy[Gi][Gj] * stream[i + Gi - 1][j + Gj - 1]
						except IndexError:
							print("Index Error")
				row.append(abs(calcedGy))
			Gy_array.append(row)

		max = 0;

		for i in range(len(Gx_array)):
			row = []
			for j in range(len(Gx_array[i])):
				g = int(math.sqrt(math.pow(Gx_array[i][j], 2) + math.pow(Gy_array[i][j], 2)))
				if(g > max):
					max = g
				row.append(g)
			output.append(row)

		img.seek(0)
		for i in range(startOfData):
			byte = img.read(1)
			out_file.write(byte)

		for i in range(width):
			for j in range(height):
				normalized = int((output[i][j]/ max) * 255)
				byte = bytes([normalized])
				out_file.write(byte)
finally:
	img.close()
	out_file.close()
