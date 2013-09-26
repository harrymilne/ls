from prefs import Prefs
from pprint import pprint
import pickle
import os
import time

class Total:
	def __init__(self, stats_list):
		self.date_generated = time.strftime("%d/%m/%Y", time.gmtime())
		self.records_included = []
		self.hours = {}
		self.servers = {}
		self.record_count = len(stats_list)
		self.stats_list = stats_list
		self.get_dates()
		self.get_hours()

	def get_dates(self):
		for record in self.stats_list:
			self.records_included.append(record.date_recorded)
		self.records_included.sort()

	def get_hours(self):
		for record in self.stats_list:
			if self.hours == {}:
				self.hours = record.hours.copy()
			else:
				for hour in record.hours:
					self.hours[hour] += record.hours[hour]

		for hour in self.hours:
			self.hours[hour] = round(self.hours[hour]/self.record_count, 3)



class Activity:
	def __init__(self, date):
		self.date_recorded = date
		self.hours = {}
		self.servers = {}

	def is_full_day(self):
		keys = list(self.hours.keys())
		keys.sort()
		check_keys = ["{:0>2}".format(i) for i in range(24)]
		if keys == check_keys:
			return True
		else:
			return False

def get_stats(prefs):
	stat_file = prefs["stats"]
	if os.path.exists(stat_file):
		with open(stat_file, "rb") as stat_file:
			return pickle.load(stat_file)
	else:
		return "prefs.ini does not exist."


if __name__ == "__main__":
	prefs = Prefs("prefs.ini").open_prefs()
	stats_list = get_stats(prefs)
	print(stats_list)
	if type(stats_list) == type([]):
		for i in stats_list:
			print(i.date_recorded)
			pprint(i.hours)

	full_day_count = ([record for record in stats_list if record.is_full_day()])

	print("There are {0} full days.".format(len(full_day_count)))