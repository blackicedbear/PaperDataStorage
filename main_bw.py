import numpy as np
from math import sqrt, ceil
import cv2
import struct
import brotli
import reedsolo

rsc = reedsolo.RSCodec(12)

file_size_bits = 64

def encode(input_file_name, output_file_name):
    #Read the whole file to data
    with open(input_file_name, 'rb') as binary_file:        
        data = binary_file.read()
        data = brotli.compress(data)
        data = rsc.encode(data)

    # Print the type of data
    print(type(data))

    # d is a verctor of data_len bytes
    d = np.frombuffer(data, dtype=np.uint8)
    d = np.unpackbits(d.reshape(-1, 1), axis=1).flatten()

    # Data length in bytes
    data_len = len(d)

    data_len_as_bytes = np.frombuffer(struct.pack("Q", data_len), dtype=np.uint8) # Convert data_len to 8 bytes
    data_len_as_bytes = np.unpackbits(data_len_as_bytes.reshape(-1, 1), axis=1).flatten()

    data_len = data_len + len(data_len_as_bytes) #Update length to include the 8 bytes

    # Set data_len as first 8 bytes of d
    d = np.hstack((data_len_as_bytes, d))

    # Assume image shape should be close to square
    sqrt_len = int(ceil(sqrt(data_len)))  # Compute square toot and round up

    # Requiered length in bytes.
    new_len = sqrt_len*sqrt_len

    # Number of bytes to pad (need to add zeros to the end of d)
    pad_len = new_len - data_len

    # Pad d with zeros at the end.
    # padded_d = np.pad(d, (0, pad_len))
    padded_d = np.hstack((d, np.zeros(pad_len, np.uint8) + 1)) * 255

    # Reshape 1D array into 2D array with sqrt_len pad_len x sqrt_len (im is going to be a Grayscale image).
    im = np.reshape(padded_d, (sqrt_len, sqrt_len))

    # Save image
    cv2.imwrite(output_file_name, im)

def decode(input_file_name, output_file_name):
    im = cv2.imread(input_file_name, cv2.IMREAD_GRAYSCALE)

    # Convert 2D to 1D
    padded_d = im.flatten()

    # Iterate over the array and set values to 0 when smaller than 127 and to 1 if higher
    for i in range(len(padded_d)):
        if padded_d[i] < 127:
            padded_d[i] = 0
        else:
            padded_d[i] = 1

    # Get original length
    data_len = [padded_d[:file_size_bits][n:n+8] for n in range(0, len(padded_d[:file_size_bits]), 8)]
    data_len_as_bytes = np.packbits(data_len, axis=1).flatten()

    orig_data_len = struct.unpack("Q", data_len_as_bytes.tobytes())

    # Crop the original data bytes (without the padding).
    data_pack = [padded_d[file_size_bits:file_size_bits+orig_data_len[0]][n:n+8] for n in range(0, len(padded_d[file_size_bits:file_size_bits+orig_data_len[0]]), 8)]
    data = np.packbits(data_pack, axis=1).flatten().tobytes()

    # Print the type of data
    print(type(data))

    #Write d whole file to binary file
    with open(output_file_name, 'wb') as binary_file:
        data = bytes(rsc.decode(data)[0])
        data = brotli.decompress(data)
        binary_file.write(data)

if __name__ == "__main__":
    #encode("testfile.txt", "testfile.txt.png")
    decode("C:\\Users\\Michael\\Documents\\ScanImage001.jpg", "testfile2.txt")