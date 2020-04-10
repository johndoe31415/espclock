#!/usr/bin/python3
#	espclock - ESP-based dot matrix clock with NTP synchronization
#	Copyright (C) 2020-2020 Johannes Bauer
#
#	This file is part of espclock.
#
#	espclock is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	espclock is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with espclock; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import re

def calc_parity(bits):
	return sum(bits) % 2

def print_decoding(bitstream):
	bitstream = re.sub("[^01]", "", bitstream)
	bitstream = [ int(x) for x in bitstream ]
	print("Received bits            : %d" % (len(bitstream)))
	print("    0 Start bit          : %d%s" % (bitstream[0], "" if (bitstream[0] == 0) else " - INCORRECT"))
	print(" 1-14 Meteo bits         : %s" % (" ".join(str(bit) for bit in bitstream[1 : 15])))
	print("   15 Call bit           : %d%s" % (bitstream[15], "" if (bitstream[15] == 0) else " - Abnormal operation"))
	print("   16 Timezone change bit: %d%s" % (bitstream[16], "" if (bitstream[15] == 0) else " - Change of timezone imminent"))
	print("   17 Timezone           : %d %s" % (bitstream[17], "MEZ" if (bitstream[17] == 0) else "MESZ"))
	print("   18 Timezone           : %d %s" % (bitstream[18], "MESZ" if (bitstream[18] == 0) else "MEZ"))
	if not (bitstream[17] ^ bitstream[18]):
		print("Timezone bits 17 and 18 in disagreement!")
	print("   19 Leap second        : %d%s" % (bitstream[19], "" if (bitstream[19] == 0) else " - Leap second imminent"))
	print("   20 Begin of time info : %d%s" % (bitstream[20], " - Error" if (bitstream[20] == 0) else ""))

	minute = sum(bit * bitval for (bit, bitval) in zip(bitstream[21 : 28], [ 1, 2, 4, 8, 10, 20, 40 ]))
	expected_parity = calc_parity(bitstream[21 : 28])
	print("21-27 Minute             : %d" % (minute))
	print("   28 Minute parity      : %d%s" % (bitstream[28], "" if (bitstream[28] == expected_parity) else " - Parity error"))

	hour = sum(bit * bitval for (bit, bitval) in zip(bitstream[29 : 35], [ 1, 2, 4, 8, 10, 20 ]))
	expected_parity = calc_parity(bitstream[29 : 35])
	print("29-34 Hour               : %d" % (hour))
	print("   35 Hour parity        : %d%s" % (bitstream[35], "" if (bitstream[35] == expected_parity) else " - Parity error"))

	day_of_month = sum(bit * bitval for (bit, bitval) in zip(bitstream[36 : 42], [ 1, 2, 4, 8, 10, 20 ]))
	print("36-41 Day of month       : %d" % (day_of_month))

	weekday = sum(bit * bitval for (bit, bitval) in zip(bitstream[42 : 45], [ 1, 2, 4 ]))
	weekday_name = {
		1:	"Monday",
		2:	"Tuesday",
		3:	"Wednesday",
		4:	"Thursday",
		5:	"Friday",
		6:	"Saturday",
		7:	"Sunday",
	}.get(weekday, "Invalid")
	print("42-44 Weekday            : %d %s" % (weekday, weekday_name))

	month = sum(bit * bitval for (bit, bitval) in zip(bitstream[45 : 50], [ 1, 2, 4, 8, 10 ]))
	print("45-49 Month              : %d" % (month))

	year = sum(bit * bitval for (bit, bitval) in zip(bitstream[50 : 58], [ 1, 2, 4, 8, 10, 20, 40, 80 ]))
	print("50-57 Year               : %d" % (year))

	print("      Date               : %s, %d.%d.%d" % (weekday_name, day_of_month, month, year + 2000))

	expected_parity = calc_parity(bitstream[36 : 58])
	print("   58 Date parity        : %d%s" % (bitstream[58], "" if (bitstream[58] == expected_parity) else " - Parity error"))


if __name__ == "__main__":
	import sys
	if len(sys.argv) != 2:
		print("%s [bitstream]" % (sys.argv[0]))
		sys.exit(0)
	print_decoding(sys.argv[1])

	# Real data: https://www.dcf77logs.de/live
	#print_decoding("0-01001000110011-001001-10000010-1000010-000010-101-00100-000001001")
	#print_decoding("0-10000111111111-001001-10011010-1000010-000010-101-00100-000001001")
