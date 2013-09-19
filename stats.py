import time
import os
import pickle

class Stats:
	def __init__(self, prefs):
		self.file_name = prefs["stats"]
		self.stats = {"active_hours":{}, "active_servers":{}}
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
		self.set_players_online(server_data, hour)
		self.set_server_players(server_data, hour)
		self.save()

	#WIP to record how long the data has been recorded for
	def new_day(self):
		if "date" not in self.stats:
			self.stats["date"] = time.strftime("%d/%m/%Y", time.gmtime())

	def set_players_online(self, server_data, hour):
		players_online = 0
		for server in server_data:
			players_online += len(server_data[server]["players"])

		if hour in self.stats["active_hours"]:
			self.stats["active_hours"][hour] += players_online
		else:
			self.stats["active_hours"][hour] = players_online

	def set_server_players(self, server_data, hour):
		for server in server_data:
			players = len(server_data[server]["players"])
			if server not in self.stats["active_servers"]:
				self.stats["active_servers"][server] = {}
			if hour in self.stats["active_servers"]:
				self.stats["active_servers"][server][hour] += players
			else:
				self.stats["active_servers"][server][hour] = players

