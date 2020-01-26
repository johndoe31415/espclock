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

import sys
import datetime
import calendar
import pytz

from UDateTime import UDateTime

def print_die_table():
	die = 0
	table = [ ]
	for year in range(2000, 2400):
		die += UDateTime.days_in_year(year)
		table.append(die)
	print(table)

def print_diy_table():
	diy = 0
	table = [ ]
	for month in range(12):
		diy += UDateTime.days_in_month(2004, month + 1)
		table.append(diy)
	print(table)


#	print_die_table()
#	print_diy_table()

def tt(ts):
	ts = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
	return calendar.timegm(ts.utctimetuple())

def ttuple(timet):
	ts = datetime.datetime.utcfromtimestamp(timet)
	return (ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, ts.weekday())


ltz = pytz.timezone("Europe/Berlin")
def lttuple(timet):
	tt = ttuple(timet)
	utcts = datetime.datetime(tt[0], tt[1], tt[2], tt[3], tt[4], tt[5])
	lts = ltz.fromutc(utcts)
	return (lts.year, lts.month, lts.day, lts.hour, lts.minute, lts.second, lts.weekday())

assert(tt("1970-01-01 00:00:00") == 0)
assert(ttuple(0) == (1970, 1, 1, 0, 0, 0, 3))
assert(ttuple(tt("2345-06-07 12:34:56")) == (2345, 6, 7, 12, 34, 56, 3))
assert(lttuple(0) == (1970, 1, 1, 1, 0, 0, 3))

#print(UDateTime.unix_timet_to_time_tuple(tt("1970-01-01 00:00:00")))
#print(UDateTime.unix_timet_to_time_tuple(tt("2000-12-30 12:34:56")))
#print(UDateTime.unix_timet_to_time_tuple(tt("2000-12-31 12:34:56")))
#print(UDateTime.unix_timet_to_time_tuple(tt("2001-01-01 12:34:56")))
#print(UDateTime.unix_timet_to_time_tuple(tt("2001-01-02 12:34:56")))
#print(UDateTime.unix_timet_to_time_tuple(tt("2020-01-24 12:34:56")))

start_timet = tt("2020-01-01 00:00:00")
t = start_timet
while True:
	#ref = ttuple(t)
	#got = UDateTime.unix_timet_to_time_tuple(t)

#	ref = ttuple(t)
#	got = UDateTime.time_tuple_to_unix_timet(ref)
#	ref = t

	ref = lttuple(t)
	got = UDateTime.unix_timet_to_local_time_tuple(t, UDateTime.tz_europe_berlin)
	if ref != got:
		print("ERROR")
		print(t)
		print("ref/got", t, ref, got)
		sys.exit(0)
	t += 30
	if (t % 100000) == 0:
		print("Progress", got)
