#!/usr/bin/env python3

def crcCalculation(data):
	'''
	Note: This calculation was implmented based on the information
	  in the "6-bit CRC calculation with 0x43 polynome for BiSS"
	  section of the "Decoding the BiSS information" application
	  note from RLS (E201D02_02, issue 2, 9th February 2017).
	'''
	
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
	
	return crc

def getPrintableDataString(data, offset, size):
	#print(len(data[offset:offset+size]))
	return " " * offset + data[offset:offset+size]
	#return data[offset:size]

def parseBiSSdata(data, encBits, reducedBits, verbose):
	if len(data) != 64:
		print("Error: data length (%d) isn't 64".format(len(data)))
		return -1
	
	if data[:2] != "11":
		print("Error: first two bits (%s) aren't '11'".format(data[:2]))
		return -1
	
	# First Bits (always 11)
	firstBitsIdx = 0
	firstBitsSize = 2
	
	# Find Start & CDS bits
	idx = data.find("010")
	
	# Pad Bits (variable number of 0's; changes with BiSS clock frequency)
	padBitsIdx = firstBitsIdx + firstBitsSize
	# One pad bit was missed and two non-pad bits were included
	padBitsSize = idx + 1 - firstBitsSize
	
	# Start Bit (always 1)
	startBitIdx = padBitsIdx + padBitsSize
	startBitSize = 1
	
	# CDS Bit (always 0)
	cdsBitIdx = startBitIdx + startBitSize
	cdsBitSize = 1
	
	# Position Data
	posDataIdx = cdsBitIdx + cdsBitSize
	posData = data[posDataIdx:posDataIdx+encBits]
	posDataSize = encBits
	
	# Encoder Status Bit: Error
	encErrIdx = posDataIdx + posDataSize
	encErr = int(data[encErrIdx])
	encErrSize = 1

	# Encoder Status Bit: Warn
	encWarnIdx = encErrIdx + encErrSize
	encWarn = int(data[encWarnIdx])
	encWarnSize = 1
	
	# CRC Data = Position Data + Status Bits
	crcDataIdx = posDataIdx
	crcData = data[posDataIdx:posDataIdx+posDataSize+encErrSize+encWarnSize]
	crcDataSize = posDataSize + encErrSize + encWarnSize
	
	# CRC Value
	crcValueIdx = encWarnIdx + encWarnSize
	crcValueSize = 6
	crcValue = data[crcValueIdx:crcValueIdx+crcValueSize]
	
	# Ignored Bits
	ignoredDataIdx = crcValueIdx + crcValueSize
	ignoredData = data[ignoredDataIdx:]
	ignoredDataSize = len(ignoredData)
	
	#!print("010", posData, encErr, encWarn, crc, ignored)
	
	# Validate CRC
	crcActual = crcCalculation(int(crcData, base=2))
	crcExpected = int(crcValue, base=2)
	
	# Convert position even if the CRC check failed
	#!print(posData)
	posDataint = int(posData, base=2)
	
	if verbose:
		print("BiSS data      (64-bits):", data)
		print("First bits   (always 11):", getPrintableDataString(data, firstBitsIdx, firstBitsSize))
		print("Pad bits   (variable 0s):", getPrintableDataString(data, padBitsIdx, padBitsSize))
		print("Start bit     (always 1):", getPrintableDataString(data, startBitIdx, startBitSize))
		print("CDS bit       (always 0):", getPrintableDataString(data, cdsBitIdx, cdsBitSize))
		print("Position data   ({}-bit):".format(encBits), getPrintableDataString(data, posDataIdx, posDataSize))
		print("Encoder error bit (1=OK):", getPrintableDataString(data, encErrIdx, encErrSize))
		print("Encoder warn bit  (1=OK):", getPrintableDataString(data, encWarnIdx, encWarnSize))
		print("CRC                     :", getPrintableDataString(data, crcValueIdx, crcValueSize))
		print("Ignored bits            :", getPrintableDataString(data, ignoredDataIdx, ignoredDataSize))
		print()
	
	if crcActual == crcExpected:
		print("CRC check: OK")
	else:
		if verbose:
			print("CRC check: FAILED - Expected {} ({:b}), Actual {} ({:b})".format(crcExpected, crcExpected, crcActual, crcActual))
		else:
			print("CRC check: FAILED")
	# 
	if (encErr == 1) and (encWarn == 1):
		print("Encoder status: OK")
	elif (encErr == 0) and (encWarn == 0):
		print("Encoder status: ERROR & WARNING")
	elif encErr == 0:
		print("Encoder status: ERROR")
	elif encWarn == 0:
		print("Encoder status: WARNING")
	
	# Convert position even if the CRC check failed
	posDataint = int(posData, base=2)
	
	print("{}-bit position: {}".format(encBits, posDataint))
	if reducedBits != 0:
		print("{}-bit position: {}".format(reducedBits, (posDataint >> (encBits - reducedBits))))


def main(args):
	encBits = args.enc_bits
	reducedBits = args.reduced_bits
	hexStr = args.hex_data
	verbose = args.verbose
	# c0a1685e9f3bcc0a
	#!print(hexStr)
	intValue = int(hexStr, base=16)
	# 13880490282140290058
	#!print(intValue)
	binStr = f'{intValue:b}'
	# 1100000010100001011010000101111010011111001110111100110000001010
	#!print(binStr)
	
	parseBiSSdata(binStr, encBits, reducedBits, verbose)


if __name__ == '__main__':
	import argparse as ap
	import sys
	import os
	
	parser = ap.ArgumentParser("biss-calc.py")
	
	parser.add_argument("enc_bits", action="store", type=int, default=None, help="BiSS-C encoder resolution")
	parser.add_argument("hex_data", action="store", default=None, help="BiSS-C hex data")
	parser.add_argument("-r", action="store", dest="reduced_bits", type=int, default=0, help="Reduced data bits")
	parser.add_argument("-v", action="store_true", dest="verbose", default=False, help="Enable verbose output")
	
	args = parser.parse_args(sys.argv[1:])
	
	#!print(args)
	
	main(args)
	
