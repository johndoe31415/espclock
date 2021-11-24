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

import network
import time
import machine
import socket
import machine
from UNTPClient import UNTPClient
from UDateTime import UDateTime
from UDisplay import UDisplay
from Font import glyphs
from Configuration import configuration
from DCF77Generator import DCF77Generator
from Max7219 import Max7219

class Clock():
	def __init__(self, config):
		self._config = config
		self._wifi = self._init_wifi()
		self._ntp = UNTPClient(self._config["ntp_server"])
		self._last_sync = None
		self._offset = 0
		self._debug = 0
		self._statusled = machine.Pin(2, machine.Pin.OUT)
		if self._config["mode"] == "dcf77":
			self._dcfgen = DCF77Generator()
			self._dcfpin = machine.Pin(15, machine.Pin.OUT)
		elif self._config["mode"] in [ "spi_max7219_32x8", "spi_max7219_32x8_debug" ]:
			cspin = machine.Pin(12, machine.Pin.OUT)
			spi = machine.SPI(1, 400000, sck = machine.Pin(14), mosi = machine.Pin(13))
			self._display = UDisplay(32, 8)
			self._max7219 = Max7219(cspin, spi, daisy_chain_length = 4)
		else:
			raise NotImplementedError("Mode: %s" % (self._config["mode"]))

	def _init_wifi(self):
		wifi = network.WLAN(network.STA_IF)
		wifi.active(True)
		try:
			wifi.connect(self._config["wifi"]["essid"], self._config["wifi"]["psk"])
		except OSError as e:
			# Sometimes we get "WiFi internal error" here when the hardware is
			# in a weird state. Hard reset.
			print("WiFi connect failed (%s). Hard resetting device." % (str(e)))
			time.sleep(0.5)
			machine.reset()
		return wifi

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
			self._statusled.value(1)
			if bit == 0:
				time.sleep(0.100)
			else:
				time.sleep(0.200)
			self._dcfpin.value(0)
			self._statusled.value(0)

	def _spi_max7219_interrupt(self, arg):
		if self._debug >= 1:
			self._statusled.value(1 - self._statusled.value())
		if not self._time_valid():
			hm_str = ":"
			self._display.clear()
			self._display.set_cursor(round(time.time()) % 32, 8)
			for char in hm_str:
				self._display.blit(glyphs[char])
			self._max7219.send_display_data(self._display)
			return

		now_utc_timet = self._now()
		now_local = UDateTime.unix_timet_to_local_time_tuple(now_utc_timet, UDateTime.tz_europe_berlin)
		hour = now_local[3]
		minute = now_local[4]

		self._display.clear()
		self._display.set_cursor(3, 8)
		hm_str = "%2d:%02d" % (hour, minute)
		for char in hm_str:
			self._display.blit(glyphs[char])
		self._max7219.send_display_data(self._display)

	def _debug_interrupt(self, arg):
		self._debug += 1
		if self._debug > 0xf:
			self._debug = 0
		text = "%d" % (self._debug)
		self._max7219.set_brightness(self._debug)
		self._display.clear()
		self._display.set_cursor(3, 8)
		for char in text:
			self._display.blit(glyphs[char])
		self._max7219.send_display_data(self._display)

	def run(self):
		if self._config["mode"] == "dcf77":
			machine.Timer(1).init(mode = machine.Timer.PERIODIC, period = 1000, callback = self._dcf77_interrupt)
		elif self._config["mode"] == "spi_max7219_32x8":
			machine.Timer(1).init(mode = machine.Timer.PERIODIC, period = 1000, callback = self._spi_max7219_interrupt)
		elif self._config["mode"] == "spi_max7219_32x8_debug":
			machine.Timer(1).init(mode = machine.Timer.PERIODIC, period = 200, callback = self._debug_interrupt)
		else:
			raise NotImplementedError(self._config["mode"])

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

	def shutdown(self):
		machine.Timer(1).deinit()

# Without this initial delay sometimes the GPIOs are not properly initialized
# and weird things happen. Not sure why.
print("Booting...")
time.sleep(0.5)
print("Initializing ESPclock...")
espclock = Clock(configuration)
try:
	espclock.run()
	pass
except KeyboardInterrupt:
	espclock.shutdown()
	raise
