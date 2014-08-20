import time
import os
import jinja2 as jin

class Webpage:

	def __init__(self, cfg):
		self.env 	= jin.Environment(loader=jin.FileSystemLoader("templates/"))
		self.index 	= self.env.get_template("index.html")
		self.js 	= self.env.get_template("main.js")
		self.graph 	= self.env.get_template("graph.html")
		self.cfg 	= cfg
		for f in ["www_root", "js_path"]:
			self.init_folder(f)


	def init_folder(self, dict_n):
		path = self.cfg.get("core", dict_n)
		if not path.endswith("/"):
			path = path + "/"
		self.cfg.set("core", dict_n, path)
		if not os.path.exists(path):
			os.makedirs(path)
			print("created path: %s" % path)

	def write(self, server_data):
		self.write_HTML(server_data)

	def write_HTML(self, server_data):
		servers_online = sorted([server for server in server_data if bool(len(server_data[server]["players"]))])
		servers_empty = sorted([server for server in server_data if not bool(len(server_data[server]["players"]))])
		total_players = sum([len(server_data[server]["players"]) for server in server_data])
		updated = "{0} {1}".format(time.ctime(), time.strftime("%Z", time.gmtime()))

		rendered = self.index.render(
			server_data 	= server_data, 
			servers_online	= servers_online,
			servers_empty	= servers_empty,
			total_players	= total_players,
			date			= updated,
			icon			= unichr(61475))

		path = self.cfg.get("core", "www_root")
		filen = self.cfg.get("core", "www_filen")
		with open(path + filen, mode="w") as index_f:
			index_f.write(rendered.encode("utf-8"))
		print("MSG: HTML Written.")

		self.write_JS(len(servers_online))

	def write_JS(self, server_count):
		server_num = [i for i in range(server_count)]
		rendered = self.js.render(server_num = server_num)
		path = self.cfg.get("core", "js_path")
		filen = self.cfg.get("core", "js_file")
		with open(path + filen, mode="w") as js_f:
			js_f.write(rendered)
		print("MSG: JS Written.")