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

from UDisplay import UDisplay
from Font import glyphs

display = UDisplay(32, 8)
for i in range(1440):
	display.clear()
	display.set_cursor(1, 8)
	(hour, minute) = divmod(i, 60)
	hm_str = "%2d:%02d" % (hour, minute)
	for char in hm_str:
		display.blit(glyphs[char])
	display.dump()
