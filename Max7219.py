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

class Max7219():
	COMMAND_NOOP = 0x00
	COMMAND_DIGIT = 0x01
	COMMAND_DECODE_MODE = 0x09
	COMMAND_INTENSITY = 0x0a
	COMMAND_SCAN_LIMIT = 0x0b
	COMMAND_SHUTDOWN = 0x0c
	COMMAND_DISPLAY_TEST = 0x0f

	def __init__(self, cspin, spi, daisy_chain_length = 1):
		self._cspin = cspin
		self._spi = spi
		self._daisy_chain_length = daisy_chain_length
		self._initialize_max7219()

	def _initialize_max7219(self):
		for row in range(8):
			self._send_command(self.COMMAND_DIGIT + row, [ 0 ] * self._daisy_chain_length)
		self._send_command(self.COMMAND_SHUTDOWN, [ 1 ] * self._daisy_chain_length)
		self._send_command(self.COMMAND_DECODE_MODE, [ 0 ] * self._daisy_chain_length)
		self._send_command(self.COMMAND_SCAN_LIMIT, [ 7 ] * self._daisy_chain_length)
		self.set_brightness(1)
		self._send_command(self.COMMAND_DISPLAY_TEST, [ 0 ] * self._daisy_chain_length)

	def set_brightness(self, value):
		self._send_command(self.COMMAND_INTENSITY, [ value ] * self._daisy_chain_length)

	def _send_command(self, command, data):
		packet = bytearray()
		for value in data:
			packet.append(command)
			packet.append(value)
		self._cspin.value(0)
		self._spi.write(packet)
		self._cspin.value(1)

	def send_display_data(self, display):
		for row in range(8):
			rowdata = display.get_row(row)
			self._send_command(self.COMMAND_DIGIT + row, rowdata)
