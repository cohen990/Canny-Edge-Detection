import binascii

img = open("test.bmp", "rb");

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


		for i in range(width):
			row = []
			for j in range(height):
				calcedGx = 0
				for Gi in range(3):
					for Gj in range(3):
						try:
							calcedGx += Gx[Gi][Gj] * stream[i + Gi - 1][j + Gj - 1]
						except IndexError:
							print("Index Error")
				row.append(calcedGx)
			output.append(row)

finally:
	img.close()

print(output)