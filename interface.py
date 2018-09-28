import argparse


class user_interface():
	ARG_MODE = 1
	CONSOLE_MODE = 2

	def __init__(self, MODE):
		self.mode = MODE
		self.start_line = 0
		self.file_path = ""
		self.parser = argparse.ArgumentParser()
		self._select_mode()

	def _select_mode(self):
		if self.mode == 1:
			print("argmode")
			self._arg_mode()
		elif self.mode == 2:
			print("consolemode")
			self._console_mode()
		else:
			raise ValueError("Unsupported Mode - use constants")

	def _arg_mode(self):
		self.parser.add_argument("urls", help="URLs you want to scan")
		self.parser.add_argument("-l", "--starting_line", help="At which line you want to start in the valid urls file")
		self.parser.add_argument("-p", "--path", help="Specify the output path")

	def _console_mode(self):
		current_line = input("start line: ")
		if current_line == "":
			current_line = 0
		else:
			current_line = int(current_line)
		return current_line

	def get_values(self):
		out = {
			"start_line" : self.start_line,
			"file_path" :   self.file_path
		}
		return out