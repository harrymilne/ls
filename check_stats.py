from prefs import Prefs
from pprint import pprint
import pickle

def get_stats(prefs):
	with open(prefs["stats"], "rb") as stat_file:
		return pickle.load(stat_file)

if __name__ == "__main__":
	prefs = Prefs("prefs.ini").open_prefs()
	pprint(get_stats(prefs))

