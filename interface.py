import argparse


class user_interface():
	ARG_MODE = 1
	CONSOLE_MODE = 2

	def __init__(self, MODE):
		self.mode = MODE
		self.urls = ""
		self.start_line = 0
		self.file_path = ""
		self.parser = argparse.ArgumentParser()
		self._select_mode()

	def _select_mode(self):
		if self.mode == 1:
			self._arg_mode()
		elif self.mode == 2:
			self._console_mode()
		else:
			raise ValueError("Unsupported Mode - use constants")

	def _arg_mode(self):
		self.parser.add_argument("urls", help="URLs you want to scan")
		self.parser.add_argument("-l", "--starting_line", help="At which line you want to start in the valid urls file")
		self.parser.add_argument("-p", "--path", help="Specify the output path")
		arguments = self.parser.parse_args()
		self.urls = arguments.urls
		try:
			self.start_line = arguments.l
			self.file_path = arguments.p
		except AttributeError:
			pass

	def _console_mode(self):
		self.current_line = input("start line: ")


	def get_values(self):
		out = {
			"urls" : self.urls.split(" "),
			"start_line" : self.start_line,
			"file_path" :   self.file_path
		}
		return out