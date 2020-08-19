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

class UDisplay():
	def __init__(self, width, height, xoffset = None, yoffset = None, xadvance = None):
		self._width = width
		self._height = height
		self._buffer_width = self._width
		self._buffer_height = (self._height + 7) // 8
		self._buffer = bytearray(self._buffer_width * self._buffer_height)
		self._cursor = (0, 0)
		self._xoffset = xoffset
		self._yoffset = yoffset
		self._xadvance = xadvance

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	@property
	def buffer(self):
		return self._buffer

	@property
	def xoffset(self):
		return self._xoffset

	@property
	def yoffset(self):
		return self._yoffset

	@property
	def xadvance(self):
		return self._xadvance

	@classmethod
	def create_glyph(cls, width, height, xoffset, yoffset, xadvance, data):
		glyph = cls(width, height, xoffset = xoffset, yoffset = yoffset, xadvance = xadvance)
		glyph._buffer = data
		return glyph

	def _offset(self, x, y):
		byte_offset = (y // 8) + (x * self._buffer_height)
		bit_offset = y % 8
		return (byte_offset, bit_offset)

	def get_pixel(self, x, y):
		(byte, bit) = self._offset(x, y)
		return ((self._buffer[byte] >> bit) & 1) != 0

	def set_pixel(self, x, y):
		if (x < 0) or (x >= self.width):
			return
		if (y < 0) or (y >= self.height):
			return
		(byte, bit) = self._offset(x, y)
		self._buffer[byte] |= (1 << bit)

	def clear_pixel(self, x, y):
		(byte, bit) = self._offset(x, y)
		self._buffer[byte] &= ~(1 << bit)

	def set_pixel_to(self, x, y, value):
		if value:
			self.set_pixel(x, y)
		else:
			self.clear_pixel(x, y)

	def clear(self):
		self._buffer = bytearray(len(self._buffer))
		self.set_cursor(0, 0)

	def set_cursor(self, x, y):
		self._cursor = (x, y)

	def dump(self):
		print(self._buffer.hex())
		print("-" * (self.width * 2))
		for y in range(self.height):
			line = ""
			for x in range(self.width):
				if self.get_pixel(x, y):
					line += "⬤ "
				else:
					line += "  "
			print(line)
		print("-" * (self.width * 2))

	def blit(self, glyph):
		for src_y in range(glyph.height):
			dst_y = self._cursor[1] + src_y + glyph.yoffset
			for src_x in range(glyph.width):
				if glyph.get_pixel(src_x, src_y):
					dst_x = self._cursor[0] + src_x + glyph.xoffset
					self.set_pixel(dst_x, dst_y)
		self._cursor = (self._cursor[0] + glyph.xadvance, self._cursor[1])
