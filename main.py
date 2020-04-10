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

	def _update_display(self):
		if self._time_valid():
			now_utc_timet = self._now()
			now_local = UDateTime.unix_timet_to_local_time_tuple(now_utc_timet, UDateTime.tz_europe_berlin)
			print("Update", now_local)
		else:
			print("Time not valid (yet).")

	def run(self):
		self._init_wifi()
		while True:
			self._update_display()
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
