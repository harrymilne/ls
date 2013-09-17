import time
import os
import pickle

class Stats:
	def __init__(self, prefs):
		self.file_name = prefs["stats"]
		self.stats = {"active_hours":{}}
		if os.path.exists(self.file_name):
			self.stats = self.load()

	def load(self):
		with open(self.file_name, "rb") as stats_file:
			return pickle.load(stats_file)

	def save(self):
		with open(self.file_name, "wb") as stats_file:
			pickle.dump(self.stats, stats_file)
		
	def log(self, server_data):
		hour = time.strftime("%H", time.gmtime())
		if hour in self.stats["active_hours"]:
			self.stats["active_hours"][hour] += self.get_players_online(server_data)
		else:
			self.stats["active_hours"][hour] = self.get_players_online(server_data)
		self.save()


	def get_players_online(self, server_data):
		players_online = 0
		for server in server_data:
			players_online += len(server_data[server]["players"])
		return players_online

