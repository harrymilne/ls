import time
import os
import pickle

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

class Stats:
	def __init__(self, prefs):
		self.prefs = prefs
		self.stats_filen 	= prefs["stats"]
		self.total_stats_filen = prefs["total_stats"]
		self.stats 		= []
		self.date 		= "0/0/0"
		if os.path.exists(self.stats_filen):
			self.stats 	= self.load()
			self.date 	= self.stats[-1].date_recorded
		else:
			for f in ["stats", "total_stats"]:
				self.init_folder(f)
				self.init_file(f)


	def init_folder(self, dict_n):
		dirs = self.prefs[dict_n].split("/")
		for i, d in zip(range(1, len(dirs)+1), dirs):
			if "." not in d and not os.path.exists(os.path.join(*dirs[0:i])):
				os.mkdir(os.path.join(*dirs[0:i]))


	def init_file(self, dict_n):
		if dict_n in self.prefs:
			if not os.path.exists(self.prefs[dict_n]):
				with open(self.prefs[dict_n], mode="w", encoding="utf-8") as f:
					pass

	def load(self):
		with open(self.stats_filen, "rb") as stats_file:
			return pickle.load(stats_file)

	def save(self):
		with open(self.stats_filen, "wb") as stats_file:
			pickle.dump(self.stats, stats_file)
		
	def log(self, server_data):
		hour = time.strftime("%H", time.gmtime())
		if self.new_day():
			new_date = time.strftime("%d/%m/%Y", time.gmtime())
			self.stats.append(Activity(new_date))
			self.date = new_date
		self.set_players_online(server_data, hour)
		self.set_server_players(server_data, hour)
		full_days = self.get_full_days()
		if len(full_days) > 1:
			with open(self.total_stats_filen, "wb") as total_f:
				pickle.dump(Total(full_days), total_f)
		self.save()

	def new_day(self):
		if self.date != time.strftime("%d/%m/%Y", time.gmtime()):
			return True
		else:
			return False

	def get_full_days(self):
		full_days = []
		for record in self.stats:
			if record.is_full_day():
				full_days.append(record)
		return full_days

	def set_players_online(self, server_data, hour):
		players_online = 0
		for server in server_data:
			players_online += len(server_data[server]["players"])

		if hour in self.stats[-1].hours:
			self.stats[-1].hours[hour] += players_online/60
		else:
			self.stats[-1].hours[hour] = players_online/60

		self.stats[-1].hours[hour] = round(self.stats[-1].hours[hour], 2)

	def set_server_players(self, server_data, hour):
		for server in server_data:
			players = len(server_data[server]["players"])
			if server not in self.stats[-1].servers:
				self.stats[-1].servers[server] = {}
			if hour in self.stats[-1].servers[server]:
				self.stats[-1].servers[server][hour] += players/60
			else:
				self.stats[-1].servers[server][hour] = players/60

			self.stats[-1].servers[server][hour] = round(self.stats[-1].servers[server][hour], 2)
