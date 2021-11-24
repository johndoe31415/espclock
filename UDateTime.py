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

import enum

class UTimezone(enum.Enum):
	UTC = "UTC"
	Europe_Berlin = "Europe/Berlin"

class UDateTime():
	_DAYS_IN_MONTH_NONLEAP = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
	_TABLE_DAYS_IN_YEAR_NONLEAP = [ 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365 ]
	_TABLE_DAYS_IN_YEAR_LEAP = [ 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366 ]
	_TABLE_ERA_DAYS = [ 366, 731, 1096, 1461, 1827, 2192, 2557, 2922, 3288, 3653, 4018, 4383, 4749, 5114, 5479, 5844, 6210, 6575, 6940, 7305, 7671, 8036, 8401, 8766, 9132, 9497, 9862, 10227, 10593, 10958, 11323, 11688, 12054, 12419, 12784, 13149, 13515, 13880, 14245, 14610, 14976, 15341, 15706, 16071, 16437, 16802, 17167, 17532, 17898, 18263, 18628, 18993, 19359, 19724, 20089, 20454, 20820, 21185, 21550, 21915, 22281, 22646, 23011, 23376, 23742, 24107, 24472, 24837, 25203, 25568, 25933, 26298, 26664, 27029, 27394, 27759, 28125, 28490, 28855, 29220, 29586, 29951, 30316, 30681, 31047, 31412, 31777, 32142, 32508, 32873, 33238, 33603, 33969, 34334, 34699, 35064, 35430, 35795, 36160, 36525, 36890, 37255, 37620, 37985, 38351, 38716, 39081, 39446, 39812, 40177, 40542, 40907, 41273, 41638, 42003, 42368, 42734, 43099, 43464, 43829, 44195, 44560, 44925, 45290, 45656, 46021, 46386, 46751, 47117, 47482, 47847, 48212, 48578, 48943, 49308, 49673, 50039, 50404, 50769, 51134, 51500, 51865, 52230, 52595, 52961, 53326, 53691, 54056, 54422, 54787, 55152, 55517, 55883, 56248, 56613, 56978, 57344, 57709, 58074, 58439, 58805, 59170, 59535, 59900, 60266, 60631, 60996, 61361, 61727, 62092, 62457, 62822, 63188, 63553, 63918, 64283, 64649, 65014, 65379, 65744, 66110, 66475, 66840, 67205, 67571, 67936, 68301, 68666, 69032, 69397, 69762, 70127, 70493, 70858, 71223, 71588, 71954, 72319, 72684, 73049, 73414, 73779, 74144, 74509, 74875, 75240, 75605, 75970, 76336, 76701, 77066, 77431, 77797, 78162, 78527, 78892, 79258, 79623, 79988, 80353, 80719, 81084, 81449, 81814, 82180, 82545, 82910, 83275, 83641, 84006, 84371, 84736, 85102, 85467, 85832, 86197, 86563, 86928, 87293, 87658, 88024, 88389, 88754, 89119, 89485, 89850, 90215, 90580, 90946, 91311, 91676, 92041, 92407, 92772, 93137, 93502, 93868, 94233, 94598, 94963, 95329, 95694, 96059, 96424, 96790, 97155, 97520, 97885, 98251, 98616, 98981, 99346, 99712, 100077, 100442, 100807, 101173, 101538, 101903, 102268, 102634, 102999, 103364, 103729, 104095, 104460, 104825, 105190, 105556, 105921, 106286, 106651, 107017, 107382, 107747, 108112, 108478, 108843, 109208, 109573, 109938, 110303, 110668, 111033, 111399, 111764, 112129, 112494, 112860, 113225, 113590, 113955, 114321, 114686, 115051, 115416, 115782, 116147, 116512, 116877, 117243, 117608, 117973, 118338, 118704, 119069, 119434, 119799, 120165, 120530, 120895, 121260, 121626, 121991, 122356, 122721, 123087, 123452, 123817, 124182, 124548, 124913, 125278, 125643, 126009, 126374, 126739, 127104, 127470, 127835, 128200, 128565, 128931, 129296, 129661, 130026, 130392, 130757, 131122, 131487, 131853, 132218, 132583, 132948, 133314, 133679, 134044, 134409, 134775, 135140, 135505, 135870, 136236, 136601, 136966, 137331, 137697, 138062, 138427, 138792, 139158, 139523, 139888, 140253, 140619, 140984, 141349, 141714, 142080, 142445, 142810, 143175, 143541, 143906, 144271, 144636, 145002, 145367, 145732, 146097 ]

	@classmethod
	def _cumulative_table_lookup(cls, table, value):
		tsize = len(table)
		approximate_step_per_index = table[-1] // tsize
		approximate_index = value // approximate_step_per_index

		for index in (approximate_index - 1, approximate_index, approximate_index + 1):
			if (index < 0) or (index >= tsize):
				continue
			table_value = table[index]
			prev_table_value = 0 if (index == 0) else table[index - 1]
			if value < table_value:
				return (index, value - prev_table_value)

	@classmethod
	def year_is_leap(cls, year):
		return ((year % 4) == 0) and (((year % 100) != 0) or ((year % 400) == 0))

	@classmethod
	def days_in_year(cls, year):
		return 366 if cls.year_is_leap(year) else 365

	@classmethod
	def days_in_month(cls, year, month):
		dim = cls._DAYS_IN_MONTH_NONLEAP[month - 1]
		if (month == 2) and (cls.year_is_leap(year)):
			dim += 1
		return dim

	@classmethod
	def y2k_to_time_tuple(cls, y2k):
		(days, seconds) = divmod(y2k, 86400)
		(era, day_in_era) = divmod(days, 146097)

		# year_in_era_index is between 0..399
		(year_in_era_index, day_of_year_index) = cls._cumulative_table_lookup(cls._TABLE_ERA_DAYS, day_in_era)

		year = 2000 + (era * 400) + year_in_era_index

		month_table = cls._TABLE_DAYS_IN_YEAR_LEAP if cls.year_is_leap(year) else cls._TABLE_DAYS_IN_YEAR_NONLEAP
		(month_index, days_in_month_index)  = cls._cumulative_table_lookup(month_table, day_of_year_index)
		month = month_index + 1
		day = days_in_month_index + 1

		day_of_week = (days + 5) % 7

		(hour, minute, second) = (seconds // 3600, seconds % 3600 // 60, seconds % 3600 % 60)
		return (year, month, day, hour, minute, second, day_of_week)

	@classmethod
	def time_tuple_to_y2k(cls, time_tuple):
		(year, month, day, hour, minute, second, day_of_week) = time_tuple

		year_index = year - 2000
		(era, year_in_era_index) = divmod(year_index, 400)

		# Days of the ERA
		days = era * 146097

		# Days of all years within the ERA
		days += cls._TABLE_ERA_DAYS[year_in_era_index - 1] if (year_in_era_index > 0) else 0

		# Days in the current year for the previous months
		leap = cls.year_is_leap(year)
		if month >= 2:
			days += cls._TABLE_DAYS_IN_YEAR_LEAP[month - 2] if leap else cls._TABLE_DAYS_IN_YEAR_NONLEAP[month - 2]

		# Days in the current month
		days += day - 1

		y2k_date = days * 86400
		y2k_date = y2k_date + (3600 * hour) + (60 * minute) + second
		return y2k_date

	@classmethod
	def unix_timet_to_time_tuple(cls, time_t):
		# Rebase to have offset relative 2000-01-01
		y2k = time_t - 946684800
		return cls.y2k_to_time_tuple(y2k)

	@classmethod
	def time_tuple_to_unix_timet(cls, time_tuple):
		return cls.time_tuple_to_y2k(time_tuple) + 946684800

	@classmethod
	def _tz_europe_berlin(cls, time_t, utc_timetuple):
		first_april = cls.y2k_to_time_tuple(cls.time_tuple_to_y2k((utc_timetuple[0], 4, 1, 0, 0, 0, -1)))
		last_sunday_march = 31 - first_april[6]

		first_november = cls.y2k_to_time_tuple(cls.time_tuple_to_y2k((utc_timetuple[0], 11, 1, 0, 0, 0, -1)))
		last_sunday_october = 31 - first_november[6]

		mdhms = utc_timetuple[1 : 1 + 5]
		is_dst = (3, last_sunday_march, 1, 0, 0) <= mdhms < (10, last_sunday_october, 1, 0, 0)

		second_offset = (3600 * 2) if is_dst else 3600
		return cls.unix_timet_to_time_tuple(time_t + second_offset)

	@classmethod
	def unix_timet_to_local_time_tuple(cls, time_t, timezone):
		assert(isinstance(timezone, UTimezone))
		utc_ttuple = cls.unix_timet_to_time_tuple(time_t)
		if timezone == UTimezone.UTC:
			return utc_ttuple
		else:
			handler = {
				UTimezone.Europe_Berlin: cls._tz_europe_berlin,
			}[timezone]
			return handler(time_t, utc_ttuple)
