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

import socket

class UNTPClient():
	def __init__(self, hostname, timeout_secs = 3):
		self._hostname = hostname
		self._timeout_secs = timeout_secs

	def sync(self):
		packet = [ ]
		packet += [ 0xe3, 0x00, 0x03 ]			# Unsynchronized NTPv4 client, no stratum, invalid polling interval
		packet += [ 0xfa ]						# 0.015625 sec peer clock precision
		packet += [ 0x00, 0x01, 0x00, 0x00 ]	# 1 sec root delay
		packet += [ 0x00, 0x01, 0x00, 0x00 ]	# 1 sec root dispersion
		packet += [ 0x00 ] * 4					# reference ID
		packet += [ 0x00 ] * 8					# reference TS
		packet += [ 0x00 ] * 8					# origin TS
		packet += [ 0x00 ] * 8					# receive TS
		packet += [ 0x00 ] * 8					# transmit TS
		packet = bytes(packet)

		addr = socket.getaddrinfo(self._hostname, 123)
		if len(addr) == 0:
			return None
		addr = addr[0][-1]
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(self._timeout_secs)
		sock.sendto(packet, addr)
		try:
			offset = -8
			response = sock.recv(len(packet))
			timestamp_bin = response[offset : offset + 4]
			timestamp = sum((value << (byteno * 8)) for (byteno, value) in enumerate(reversed(timestamp_bin)))
			time_t = timestamp - 2208988800

			fraction = response[offset + 4]
			if fraction >= 0x7f:
				# Round up
				time_t += 1
			return time_t
		except OSError:
			return None
