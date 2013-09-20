import time

class Webpage:

	def __init__(self, prefs):
		self.prefs = prefs

	def write(self, server_data):
		self.write_JS(len(server_data), self.prefs)
		self.write_HTML(server_data)

	def write_HTML(self, server_data):

		with open(self.prefs["index"], mode="r", encoding="utf-8") as htmlFile:
			htmlLines = htmlFile.readlines()

		html_start = htmlLines.index("<!--SERVERSTART-->\n")
		html_end = htmlLines.index("<!--SERVEREND-->\n")
		html_date = htmlLines.index('\t\t<div class="server-box" id="info-box">\n')
		new_HTML = []

		process_online = {}
		process_empty = {}
		for server in server_data:
			if server_data[server]["player_count"]:
				process_online[server] = server_data[server].copy()
			else:
				process_empty[server] = server_data[server].copy()


		htmlLines[html_date+1] = "Last Updated: {0} (GMT{1})\n".format(time.ctime(), self.prefs["timezone"])

		serverCount = 0

		for server in sorted(process_online):
			socket = server_data[server]["socket"][0] +":"+ str(server_data[server]["socket"][1])

			if process_online[server]["passworded"]:
				pwd_html = '<span id="icon"></span>'
				pwd_uri = '*'
			else:
				pwd_html = pwd_uri = ''
			

			serverHeader = '<div class="button" id="server{0}">'.format(serverCount)
			info_line = """
					<div class="server-box" id="server-online-box">
						<div id="box-title">{0}</div>
						<div id="box-middle">{5} {1}/{2}</div>
						<div id="box-mission">{3}</div>
						<div id="box-end">{4}</div>
					</div>
			""".format(server, process_online[server]["player_count"], process_online[server]["max_players"], process_online[server]["mission"], process_online[server]["gamemode"], pwd_html)

			playerLine = '\t\t\t\t<div class = "playerlist" id = "server{0}list">'.format(serverCount)
			for player in sorted(process_online[server]["players"]):
				playerLine += '\n\t\t\t\t\t<div id="box-name">{0}</div>'.format(player)
			playerLine += '\n\t \t\t\t\t<div id="box-join"><a href = "legions://{0}{1}">Join Server</a></div>'.format(socket, pwd_uri)
			playerLine += '\n\t\t\t\t</div>'

			serverFooter = "</div>\n"
			new_HTML.append(serverHeader + info_line + serverFooter + playerLine)

			serverCount += 1


		for server in sorted(process_empty):
			socket = server_data[server]["socket"][0] +":"+ str(server_data[server]["socket"][1])

			if process_empty[server]["passworded"]:
				pwd_html = '<span id="icon"></span>'
				pwd_uri = '*'
			else:
				pwd_html = pwd_uri = ''

			info_line = """
					<div class="server-box" id="server-empty-box">
						<div id="box-title"><a href = "legions://{5}{7}">{0}</a></div>
						<div id="box-middle">{6} {1}/{2}</div>
						<div id="box-mission">{3}</div>
						<div id="box-end">{4}</div>
					</div>
			""".format(server, process_empty[server]["player_count"], process_empty[server]["max_players"], process_empty[server]["mission"], process_empty[server]["gamemode"], socket, pwd_html, pwd_uri)


			new_HTML.append(info_line)


		html = htmlLines[:html_start+1] + ['\n'] + new_HTML + ['\n'] +htmlLines[html_end:]
		encoded_html = []
		for line in html:
			encoded_html.append(line.encode("utf-8"))

		with open(self.prefs["index"], mode="w", encoding="utf-8") as htmlFile:
			htmlFile.writelines(html)
		print("MSG: HTML written.")

	def write_JS(self, serverCount, prefs):
		js = ""
		header = '$(document).ready(function(){'
		footer = '\n});'
		js += header
		for serverID in range(serverCount):
			serverLine = '\n\t$("#server{0}").click(function() {1}\n\t\t$("#server{0}list").slideToggle("fast", "linear");\n\t{2});'.format(serverID, '{', '}')
			js += serverLine
		js += footer
		with open(prefs["js"], 'w') as jsfile:
			jsfile.write(js)
		print("MSG: JS written.")
