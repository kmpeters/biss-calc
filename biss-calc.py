#!/usr/bin/env python3

def crcValidation(data, crcToValidate):
	# IAMHERE
	
	tableCRC6 = [
	0x00, 0x03, 0x06, 0x05, 0x0C, 0x0F, 0x0A, 0x09,
	0x18, 0x1B, 0x1E, 0x1D, 0x14, 0x17, 0x12, 0x11,
	0x30, 0x33, 0x36, 0x35, 0x3C, 0x3F, 0x3A, 0x39,
	0x28, 0x2B, 0x2E, 0x2D, 0x24, 0x27, 0x22, 0x21,
	0x23, 0x20, 0x25, 0x26, 0x2F, 0x2C, 0x29, 0x2A,
	0x3B, 0x38, 0x3D, 0x3E, 0x37, 0x34, 0x31, 0x32,
	0x13, 0x10, 0x15, 0x16, 0x1F, 0x1C, 0x19, 0x1A,
	0x0B, 0x08, 0x0D, 0x0E, 0x07, 0x04, 0x01, 0x02]
	
	tmp = (data >> 30) & 0xf
	crc = (data >> 24) & 0x3f
	tmp = crc ^ tableCRC6[tmp]
	crc = (data >> 18) & 0x3f
	tmp = crc ^ tableCRC6[tmp]
	crc = (data >> 12) & 0x3f
	tmp = crc ^ tableCRC6[tmp]
	crc = (data >> 6) & 0x3f
	tmp = crc ^ tableCRC6[tmp]
	crc = data & 0x3f
	tmp = crc ^ tableCRC6[tmp]
	crc = tableCRC6[tmp]
	
	# Invert the crc bits
	crc = ~crc & 0x3f
	
	#!print(crcToValidate, crc)
	return (crc == crcToValidate)


def parseBiSSdata(data, bits):
	if len(data) != 64:
		print("Error: data length (%d) isn't 64".format(len(data)))
		return -1
	
	if data[:2] != "11":
		print("Error: first two bits (%s) aren't '11'".format(data[:2]))
	
	# Find Start & CDS bits
	idx = data.find("010")
	# Two non-pad bits were included and one pad bit was missed
	padBits = idx - 1
	
	idx += 3
	
	#!print("padBits {}", padBits)
	#!print("bits {}", bits)
	
	# Extract important data
	posData = data[idx:idx+bits]
	crcData = data[idx:idx+bits+2]
	idx += bits
	encErr = int(data[idx])
	idx += 1
	encWarn = int(data[idx])
	idx += 1
	crc = data[idx:idx+6]
	idx += 6
	ignored = data[idx:]
	#!print("010", posData, encErr, encWarn, crc, ignored)
	
	# 
	print("Encoder status (1=OK): Error = {}, Warning = {}".format(encErr, encWarn))
	
	# Validate CRC
	crcResult = crcValidation(int(crcData, base=2), int(crc, base=2))
	#!print(crcResult)
	
	if crcResult:
		print("CRC check OK")
		
		# Convert position
		#!print(posData)
		posDataint = int(posData, base=2)
		
		print("{}-bit position: {}".format(bits, posDataint))
		#print("{}-bit position: {}".format(bits, (posDataint >> (32 - bits))))
	else:
		print("CRC check FAILED")


def main(args):
	bits = args.bits
	hexStr = args.hex_data
	# c0a1685e9f3bcc0a
	#!print(hexStr)
	intValue = int(hexStr, base=16)
	# 13880490282140290058
	#!print(intValue)
	binStr = f'{intValue:b}'
	# 1100000010100001011010000101111010011111001110111100110000001010
	print(binStr)
	
	parseBiSSdata(binStr, bits)


if __name__ == '__main__':
	import argparse as ap
	import sys
	import os
	
	parser = ap.ArgumentParser("biss-calc.py")
	
	parser.add_argument("hex_data", action="store", default=None, help="BiSS-C hex data")
	parser.add_argument("-b", action="store", dest="bits", type=int, default=0, help="BiSS-C data bits")
	
	args = parser.parse_args(sys.argv[1:])
	
	#!print(args)
	
	main(args)
	
