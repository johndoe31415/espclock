#!/usr/bin/python3
#	espclock - ESP-based dot matrix clock with NTP synchronization
#	Copyright (C) 2020-2021 Johannes Bauer
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

from UNTPClient import UNTPClient
from UDateTime import UDateTime

ntp = UNTPClient("pool.ntp.org")
t = ntp.sync()
print("UTC          ", UDateTime.unix_timet_to_time_tuple(t))
print("Europe/Berlin", UDateTime.unix_timet_to_local_time_tuple(t, UDateTime.tz_europe_berlin))
