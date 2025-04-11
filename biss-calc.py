#!/usr/bin/env python3

def parseBiSSdata(data):
	# IAMHERE
	pass


def main(args):
	
	hexStr = args.hex_data
	# c0a1685e9f3bcc0a
	print(hexStr)
	intValue = int(hexStr, base=16)
	# 13880490282140290058
	print(intValue)
	binStr = f'{intValue:b}'
	# 1100000010100001011010000101111010011111001110111100110000001010
	print(binStr)
	
	parseBiSSdata(binStr)


if __name__ == '__main__':
	import argparse as ap
	import sys
	import os
	
	parser = ap.ArgumentParser("biss-calc.py")
	
	parser.add_argument("hex_data", action="store", default=None, help="BiSS-C hex data")
	
	args = parser.parse_args(sys.argv[1:])
	
	#!print(args)
	
	main(args)
	
