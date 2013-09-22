from prefs import Prefs
from pprint import pprint
import pickle
import os

class Activity:
	def __init__(self, date):
		self.date_recorded = date
		self.hours = {}
		self.servers = {}

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
			pprint(i.servers)

