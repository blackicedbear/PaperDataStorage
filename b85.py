import argparse
import base64

parser = argparse.ArgumentParser(description='Base85 Encoder and Decoder')

parser.add_argument('operation', choices=['encode', 'decode'],
                    help='Operation to perform: encode or decode')
parser.add_argument('input_file', type=str, help='Input file name')
parser.add_argument('output_file', type=str, help='Output file name')

args = parser.parse_args()

if args.operation == 'encode':
    with open(args.input_file, 'rb') as f:
        input_data = f.read()
    output_data = base64.b85encode(input_data)
elif args.operation == 'decode':
    with open(args.input_file, 'r') as f:
        input_data = f.read()
    output_data = base64.b85decode(input_data)

with open(args.output_file, 'wb') as f:
    f.write(output_data)