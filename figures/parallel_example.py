#!/usr/bin/env python

import sys
import random

random.seed(1)

msg        = sys.argv[1]
max_offset = float(sys.argv[2])

def c2b(char):
	"""Char to bits."""
	bits = ord(char)
	return [(bits>>i)&1 for i in range(8)]

msg_bits = list(map(c2b, msg))
offsets = [1.0 + max_offset*random.uniform(-1.0, 1.0) for _ in range(8)]

# Corrupt message
corrupt_msg_bits = [ [ ([0]+msg_bits[char_num]+[0])[bit_num + int(round(offset))]
                       for bit_num, offset in enumerate(offsets)
                     ] for char_num in range(len(msg))
                   ]
corrupt_msg = "".join( repr(chr(sum(b<<i for i,b in enumerate(char_bits))))[1:-1]
                       for char_bits in corrupt_msg_bits
                     )


# Print out waveforms
for bit_num, offset in enumerate(offsets):
	print(
		r"\waveform{bit %d}{Bit %d}{%s}{%s}{%f}{%f}{%d}"%(
			bit_num,
			bit_num,
			"above=of bit %d"%(bit_num-1) if bit_num > 0 else "",
			",".join(str(char[bit_num]) for char in msg_bits),
			offset,
			max_offset,
			msg_bits[0][bit_num],
		)
	)

# Print out labels
for char_num in range(len(msg)):
	print( (r"\draw [help lines]"
	       + r"      ([shift={(%d+1.5,0.3)}]bit 7.north east)"
	       + r"   -- ([shift={(%d+1.5,-0.3)}]bit 0.south east)"
	       + r"      node [anchor=north,text height=1.0em,black] {%s};"
	       ) % (char_num, char_num, corrupt_msg[char_num])
	     )

