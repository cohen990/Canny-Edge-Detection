import binascii

img = open("test.bmp", "rb");

stream = []

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

		# while(byte!=''):
		# 	stream.append(byte)
			# byte = img.read(1)
finally:
	img.close()

print(stream)