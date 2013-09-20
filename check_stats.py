from prefs import Prefs
from pprint import pprint
import pickle

class Activity:
	def __init__(self, date):
		self.date_recorded = date
		self.hours = {}
		self.servers = {}

def get_stats(prefs):
	with open(prefs["stats"], "rb") as stat_file:
		return pickle.load(stat_file)

if __name__ == "__main__":
	prefs = Prefs("prefs.ini").open_prefs()
	stats_list = get_stats(prefs)
	for i in stats_list:
		print(i.date_recorded)
		pprint(i.hours)
		pprint(i.servers)

