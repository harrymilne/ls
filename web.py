import time
import os
import pickle
import jinja2 as jin
from stats import Total


class Webpage:

	def __init__(self, prefs):
		self.env 	= jin.Environment(loader=jin.FileSystemLoader("templates/"))
		self.index 	= self.env.get_template("index.html")
		self.js 	= self.env.get_template("main.js")
		self.graph 	= self.env.get_template("graph.html")
		self.prefs 	= prefs
		for f in ["index", "js", "graph"]:
			self.init_file(f)


	def init_file(self, dict_n):
		if dict_n in self.prefs:
			if not os.path.exists(self.prefs[dict_n]):
				with open(self.prefs[dict_n], mode="w", encoding="utf-8") as f:
					pass

	def write(self, server_data):
		self.write_HTML(server_data)
		self.write_graph()

	def write_HTML(self, server_data):
		servers_online = sorted([server for server in server_data if bool(len(server_data[server]["players"]))])
		servers_empty = sorted([server for server in server_data if not bool(len(server_data[server]["players"]))])
		updated = "{0} {1}".format(time.ctime(), time.strftime("%Z", time.gmtime()))

		rendered = self.index.render(
			server_data 	= server_data, 
			servers_online	= servers_online,
			servers_empty	= servers_empty,
			date			= updated,
			icon			= chr(61475))

		with open(self.prefs["index"], mode="w", encoding="utf-8") as index_f:
			index_f.write(rendered)
		print("MSG: HTML Written.")

		self.write_JS(len(servers_online))

	def write_JS(self, server_count):
		server_num = [i for i in range(server_count)]
		rendered = self.js.render(server_num = server_num)
		with open(self.prefs["js"], mode="w", encoding="utf-8") as js_f:
			js_f.write(rendered)
		print("MSG: JS Written.")

	def write_graph(self):
		if os.path.exists("total.bin"):
			with open("total.bin", "rb") as total_f:
				total = pickle.load(total_f)
			graph_name 	= "Total Activity Data"
			hour_list 	= sorted(list(total.hours.keys()))
			xy_data 	= zip(hour_list, [total.hours[i] for i in hour_list])
			caption 	= "Days sampled: {0}".format(", ".join(total.records_included))
			rendered = self.graph.render(
				title			= graph_name, 
				player_activity	= xy_data,
				caption 		= caption)
			file_name = graph_name.lower().replace(" ","-")+".html"
			with open(self.prefs["graphs"]+file_name, mode="w", encoding="utf-8") as graph_f:
				graph_f.write(rendered)


