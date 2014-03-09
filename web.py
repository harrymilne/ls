import time
import os
import pickle
import jinja2 as jin

class Webpage:

	def __init__(self, cfg):
		self.env 	= jin.Environment(loader=jin.FileSystemLoader("templates/"))
		self.index 	= self.env.get_template("index.html")
		self.js 	= self.env.get_template("main.js")
		self.graph 	= self.env.get_template("graph.html")
		self.cfg 	= cfg
		for f in ["index", "js"]:
			self.init_folder(f)
			self.init_file(f)


	def init_folder(self, dict_n):
		dirs = self.cfg.get("core", dict_n).split("/")
		for i, d in zip(range(1, len(dirs)+1), dirs):
			if "." not in d and not os.path.exists(os.path.join(*dirs[0:i])):
				os.mkdir(os.path.join(*dirs[0:i]))


	def init_file(self, dict_n):
		with open(self.cfg.get("core", dict_n), mode="w") as f:
			pass

	def write(self, server_data):
		self.write_HTML(server_data)

	def write_HTML(self, server_data):
		servers_online = sorted([server for server in server_data if bool(len(server_data[server]["players"]))])
		servers_empty = sorted([server for server in server_data if not bool(len(server_data[server]["players"]))])
		updated = "{0} {1}".format(time.ctime(), time.strftime("%Z", time.gmtime()))

		rendered = self.index.render(
			server_data 	= server_data, 
			servers_online	= servers_online,
			servers_empty	= servers_empty,
			date			= updated,
			icon			= unichr(61475))

		with open(self.cfg.get("core", "index"), mode="w") as index_f:
			index_f.write(rendered.encode("utf-8"))
		print("MSG: HTML Written.")

		self.write_JS(len(servers_online))

	def write_JS(self, server_count):
		server_num = [i for i in range(server_count)]
		rendered = self.js.render(server_num = server_num)
		with open(self.cfg.get("core", "js"), mode="w") as js_f:
			js_f.write(rendered)
		print("MSG: JS Written.")



