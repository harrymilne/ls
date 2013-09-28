import time
import jinja2 as jin

class Webpage:

	def __init__(self, prefs):
		self.env 	= jin.Environment(loader=jin.FileSystemLoader("templates/"))
		self.index 	= self.env.get_template("index.html")
		self.js 	= self.env.get_template("main.js")
		self.prefs 	= prefs

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


