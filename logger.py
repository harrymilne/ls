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

		with open(self.log_file, "r") as log:
			history = log.readlines()

		history.append(formatted_msg)

		with open(self.log_file, "w") as log:
			log.writelines(history)

if __name__ == "__main__":
	logger = Logger("error.log")
	logger.error("UH OH SHIT FUCKED UP")