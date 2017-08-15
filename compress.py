"""
1. Pass the name/path of the file to be compressed at the commandline.(Run at the source).
2.Check the intermediate file(temp.zlib) this is the binary version of the input file.
This file size is lesser then the input file. We will transfer this file through the N/W to the server.  
3. Now check the "decompressed_file.txt",it contains the content of the original input file.
We will run the program for this on the server. And use the "decompressed_file.txt" for further processing.
"""
import zlib
import sys

print(__doc__)

# Read a file
input_file = sys.argv[1]
lines = []
with open(input_file,'r') as file:
	for line in file:
		lines.append(line)

# Writing a compressed file in binary form
string = zlib.compress(str(lines))
with open("temp.zlib","wb") as file:
	file.write(string)

# Decompression
string = []
lines = []
with open("temp.zlib","rb") as file:
	string = file.read()
lines = zlib.decompress(string)

# Writing decompressed output to a file
with open("decompressed_file.txt","w") as file:
	# file.write('\n'.join(lines))
	file.write(lines)
