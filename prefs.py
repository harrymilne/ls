import os

class Prefs:
	def __init__(self, pref_file):
		self.prefs = {}
		self.pref_file = pref_file

	def check_prefs(self):
		if os.path.exists(self.pref_file):
			self.open_prefs()
			return True
		else:
			with open(self.pref_file, encoding="utf-8", mode="w") as pref_f:
				pref_f.write("index=html/index.html\njs=html/js/main.js\nerrors=error.log\nstats=stats/stats.bin\ntotal_stats=stats/total.bin\ngraphs=html/graphs/")
			print("created default.cfg")
			return True

	def open_prefs(self):
		with open(self.pref_file, mode = "r") as config_file:
			self.raw_config = config_file.read().splitlines()
		for line in self.raw_config:
			equals_index = line.index("=")
			self.prefs[line[:equals_index]] = line[equals_index+1:].strip()
		return self.prefs


if __name__ == "__main__":
	prefs = Prefs("default.cfg")
	print(prefs.prefs)