#!/usr/bin/env python3

def parseBiSSdata(data, bits):
	if len(data) != 64:
		print("Error: data length (%d) isn't 64".format(len(data)))
		return -1
	
	if data[:2] != "11":
		print("Error: first two bits (%s) aren't '11'".format(data[:2]))
	
	# Find Start & CDS bits
	idx = data.find("010")
	idx += 3
	
	# Extract important datad
	pos32 = data[idx:idx+32]
	idx += 32
	encErr = int(data[idx])
	idx += 1
	encWarn = int(data[idx])
	idx += 1
	crc = data[idx:idx+6]
	idx += 6
	ignored = data[idx:]
	#!print(pos32, encErr, encWarn, crc, ignored)
	
	# 
	print("Encoder status (1=OK): Error = {}, Warning = {}".format(encErr, encWarn))
	
	# TODO: Check CRC here
	
	# Convert position
	#!print(pos32)
	pos32int = int(pos32, base=2)
	print("32-bit position: {}".format(pos32int))
	print("{}-bit position: {}".format(bits, (pos32int >> (32 - bits))))


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
	
