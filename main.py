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

import network
import time
import machine
import socket
import machine
from UNTPClient import UNTPClient
from UDateTime import UDateTime
from Configuration import configuration
from DCF77Generator import DCF77Generator

class Clock():
	def __init__(self, config):
		self._config = config
		self._wifi = None
		self._ntp = UNTPClient(self._config["ntp_server"])
		self._last_sync = None
		self._offset = 0
		self._dcfgen = DCF77Generator()
		self._dcfpin = machine.Pin(15, machine.Pin.OUT)
		self._dcfled = machine.Pin(2, machine.Pin.OUT)

	def _init_wifi(self):
		self._wifi = network.WLAN(network.STA_IF)
		self._wifi.active(True)
		self._wifi.connect(self._config["wifi"]["essid"], self._config["wifi"]["psk"])

	def _now(self):
		return time.time() + self._offset

	def _need_sync(self):
		# Sync once every hour with NTP server
		return (self._last_sync is None) or (self._last_sync >= 3600)

	def _time_valid(self):
		# But even when sync fails, show time up to 1 day afterwards (our clock
		# hopefully won't drift that much)
		return (self._last_sync is not None) and (self._last_sync < 86400)

	def _dcf77_interrupt(self, arg):
		if not self._time_valid():
			return

		now_utc_timet = self._now()
		now_local = UDateTime.unix_timet_to_local_time_tuple(now_utc_timet, UDateTime.tz_europe_berlin)
		hour = now_local[3]
		minute = now_local[4]
		second = now_local[5]
		bit = self._dcfgen.get_bit(second)
		if second == 59:
			next_hour_minute = ((hour * 60) + minute + 2) % 1440
			hour = next_hour_minute // 60
			minute = next_hour_minute % 60
			self._dcfgen.set_time(hour, minute)

		if bit is not None:
			self._dcfpin.value(1)
			self._dcfled.value(1)
			if bit == 0:
				time.sleep(0.100)
			else:
				time.sleep(0.200)
			self._dcfpin.value(0)
			self._dcfled.value(0)

	def run(self):
		self._init_wifi()
		machine.Timer(1).init(mode = machine.Timer.PERIODIC, period = 1000, callback = self._dcf77_interrupt)
		while True:
			if self._need_sync():
				current_timet = self._ntp.sync()
				if current_timet is not None:
					self._last_sync = 0
					self._offset = current_timet - time.time()
					print("Successfully synced:", current_timet)
				else:
					print("Sync failed.")
			if self._last_sync is not None:
				self._last_sync += 1
			time.sleep(1)

clk = Clock(configuration)
clk.run()
