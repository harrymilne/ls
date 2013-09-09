import os
import time
class Logger:
	def __init__(self, log_file):
		self.log_file = log_file
		self.checkFile()

	def checkFile(self):
		if not os.path.exists(self.log_file):
			with open(self.log_file, "w") as log:
				log.write("---LEGIONS MASTER QUERY ERROR LOGS---\n")

	def write(self, msg, lvl):
		time_now = time.strftime("[%d/%m %H:%m] ", time.localtime())
		formatted_msg = time_now + lvl + msg + "\n"

		with open(self.log_file, mode="r", encoding="utf-8") as log:
			history = log.readlines()

		history.append(formatted_msg)

		with open(self.log_file, mode="w", encoding="utf-8") as log:
			log.writelines(history)

if __name__ == "__main__":
	logger = Logger("error.log")
	logger.write("UH OH SHIT FUCKED UP", "lvl")