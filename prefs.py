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
			return False

	def open_prefs(self):
		with open(self.pref_file, mode = "r") as config_file:
			self.raw_config = config_file.read().splitlines()
		for line in self.raw_config:
			equals_index = line.index("=")
			self.prefs[line[:equals_index]] = line[equals_index+1:].strip()
		return self.prefs


if __name__ == "__main__":
	prefs = Prefs("prefs.ini")
	print(prefs.prefs)