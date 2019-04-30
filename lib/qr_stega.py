"""
used to run the program via command line arguments
"""
from stega import Stega
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--address','-a', help = "Path to the image you want to encode/decode")
parser.add_argument('--text', '-t',help = "The text you want to embed into the qr code")
parser.add_argument('--mode', '-m',help = "The mode the program is going to run at (decode/encode)")
parser.add_argument('--output', '-o',help = "Name of the output file")
args = parser.parse_args()

x = Stega(args.input, args.text, args.mode,args.output)

