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

class DCF77Generator():
	def __init__(self):
		self._hour = None
		self._minute = None
		self._bits = None

	def set_time(self, hour, minute):
		self._hour = hour
		self._minute = minute
		self._calcbits()

	@staticmethod
	def _parity(bits):
		return sum(bits) & 1

	def get_bit(self, bitno):
		if self._bits is None:
			return None
		else:
			return self._bits[bitno]

	def _calcbits(self):
		self._bits = [ 0 ]												# Start of frame
		self._bits += [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]		# MeteoTime
		self._bits += [ 0 ]												# Rufbit
		self._bits += [ 0 ]												# No MET/MEST change
		self._bits += [ 0, 1 ]											# MET
		self._bits += [ 0 ]												# No leap second
		self._bits += [ 1 ]												# Begin of time info

		m_low = self._minute % 10
		for bit in range(4):
			self._bits += [ (m_low >> bit) & 1  ]						# Minute 10^0
		m_high = self._minute // 10
		for bit in range(3):
			self._bits += [ (m_high >> bit) & 1  ]						# Minute 10^1
		self._bits += [ self._parity(self._bits[-7 : ]) ]				# Minute parity

		h_low = self._hour % 10
		for bit in range(4):
			self._bits += [ (h_low >> bit) & 1  ]						# Hour 10^0
		h_high = self._hour // 10
		for bit in range(2):
			self._bits += [ (h_high >> bit) & 1  ]						# Hour 10^1
		self._bits += [ self._parity(self._bits[-6 : ]) ]				# Hour parity

		self._bits += [ 1, 0, 0, 0, 0, 0 ]								# 1st of month
		self._bits += [ 0, 1, 0 ]										# Tuesday (1 = Monday, 7 = Sunday)
		self._bits += [ 0, 1, 0, 0, 1 ]									# December
		self._bits += [ 0, 0, 0, 0, 0, 1, 0, 0 ]						# 2020
		self._bits += [ 1 ]												# Date parity

		self._bits += [ None ]											# Last bit not transmitted at all
