import utils
import threading
from time import sleep

UPDATE_FIFO = 0.05
UPDATE_BUFFER = 0.2
AUTO_SAVE = 20

class Database:
	def __init__(self, database_file, check_dup = True):
		self.buffer = []
		self.buffered_fifo = []
		self.fifo = []
		self.database_file = database_file
		self.chk_du = check_dup
		self._get_data_from_file()

		self.lock = threading.Lock()

		self.fifo_updater = threading.Thread(target=self._get_fifo)
		self.buffer_updater = threading.Thread(target=self._update_buffer)
		self.auto_saver = threading.Thread(target=self._flush_data)

		#self.fifo_updater = Process(target=self._get_fifo)
		#self.buffer_updater = Process(target=self._update_buffer)
		#self.auto_saver = Process(target=self._flush_data)

		self.fifo_updater.start()
		self.buffer_updater.start()
		self.auto_saver.start()

	def get_index(self, index):
		return self.buffer[index]

	def append_data(self, data):
		self.fifo = data

	def get_length(self):
		return len(self.buffer)

	def clear(self):
		self.buffer = []
		self.fifo = []
		self.buffered_fifo = []
		with open(self.database_file,"w") as db_file:
			db_file.write("")

	def _get_fifo(self):
		while True:
			for i in range(len(self.fifo)):
				self.buffered_fifo.append(self.fifo[i])
			self.fifo = []
			sleep(UPDATE_FIFO)

	def _update_buffer(self):
		while True:
			self.lock.acquire()
			for i in range(len(self.buffered_fifo)):
				for j in range(len(self.buffer)):
					#existing = self.buffer[j][:-1].split("//")[1]
					#new = data[i].split("//")[1]
					existing = self.buffer[j]; new = self.buffered_fifo[i]
					if (existing == new):
						unique = False
						break
					else:
						unique = True
				if len(self.buffer) == 0:
					unique = True
				if unique:
					self.buffer.append(self.buffered_fifo[i])
			self.lock.release()
			sleep(UPDATE_BUFFER)

	def _get_data_from_file(self):
		self.buffer = []
		with open(self.database_file,encoding="utf-8") as db_file:
			for line in db_file:
				self.buffer.append(line[:-1])

	def _flush_data(self):
		while True:

			if self.buffer != "":
				print("AUTOSAVE")
				with open(self.database_file,"w",encoding="utf-8") as db_file:
					db_file.write(utils.list_to_str(self.buffer))
			sleep(AUTO_SAVE)

if __name__ == '__main__':
	db = Database("test.db")
	db.clear()
	db.append_data(["1","2","3"])
	sleep(1)
	print(db.get_index(2))
	print(db.get_length())