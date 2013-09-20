import time
import os
import pickle

class Activity:
	def __init__(self, date):
		self.date_recorded = date
		self.hours = {}
		self.servers = {}

class Stats:
	def __init__(self, prefs):
		self.file_name 	= prefs["stats"]
		self.stats 		= []
		self.date 		= "0/0/0"
		if os.path.exists(self.file_name):
			self.stats 	= self.load()

	def load(self):
		with open(self.file_name, "rb") as stats_file:
			return pickle.load(stats_file)

	def save(self):
		with open(self.file_name, "wb") as stats_file:
			pickle.dump(self.stats, stats_file)
		
	def log(self, server_data):
		hour = time.strftime("%H", time.gmtime())
		if self.new_day():
			new_date = time.strftime("%d/%m/%Y", time.gmtime())
			self.stats.append(Activity(new_date))
			self.date = new_date
		self.set_players_online(server_data, hour)
		self.set_server_players(server_data, hour)
		self.save()

	def new_day(self):
		if self.date != time.strftime("%d/%m/%Y", time.gmtime()):
			return True
		else:
			return False

	def set_players_online(self, server_data, hour):
		players_online = 0
		for server in server_data:
			players_online += len(server_data[server]["players"])

		if hour in self.stats[-1].hours:
			self.stats[-1].hours[hour] += round(players_online/60, 2)
		else:
			self.stats[-1].hours[hour] = round(players_online/60, 2)

	def set_server_players(self, server_data, hour):
		for server in server_data:
			players = len(server_data[server]["players"])
			if server not in self.stats[-1].servers:
				self.stats[-1].servers[server] = {}
			if hour in self.stats[-1].servers[server]:
				self.stats[-1].servers[server][hour] += round(players/60, 2)
			else:
				self.stats[-1].servers[server][hour] = round(players/60, 2)

