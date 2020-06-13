import re

from multiprocessing import Process, Queue
from Database import Database
from utils import *

from interface import user_interface

def get_urls(url):
	page = requests.get(url)									#getURL
	return re.findall("<a href=\"([^\">]+)\">", page.text)	  #parseUrl

def search_urls(url, queue):
	valid_urls = []
	nv_urls = []

	urls = get_urls(url)
	for i in range(len(urls)):								  #handleExeptions
		try:
			if (urls[i][0] == "/" and urls[i][1] != "/"):
				urls[i] = conjugate_urls(url, urls[i])
			elif (urls[i][0:2] == '//'):
				urls[i] = "http://" + urls[i][2:]
		except IndexError:
			pass												#urlTooShort

	urls = check_dup_in_list(urls)

	for i in range(len(urls)):								  #validadeUrls
		if valid_url(urls[i]):
			valid_urls.append(urls[i])
		else:
			nv_urls.append((url, urls[i]))

	queue.put(valid_urls)
	return [valid_urls, nv_urls]


import time
if __name__ == "__main__":
	interface = user_interface(user_interface.CONSOLE_MODE)
	print(interface.get_values())
	db_file = interface.get_values()["file_path"]
	if db_file == "":
		db_file = "urls.txt"
	db = Database(db_file)
	max_th = int(input("mx_th: "))
	current_line = interface.get_values()["start_line"]
	threads = []
	que = Queue()
	for i in range(max_th):
		thread = Process(target=search_urls, args=(db.get_index(current_line),que))
		thread.start()
		threads.append(thread)
		current_line += 1

	start_time = time.time()
	while current_line <= db.get_length() -1:
		for thread in threads:
			if not thread.is_alive():
				queue_data = que.get()
				db.append_data(queue_data)
				if current_line <= db.get_length() -1:
					print("P: " + thread.name.split("-")[1],current_line,sep="\t")
					#print("P: " + str(i), current_line, sep="\t")

					thread = Process(target=search_urls, args=(db.get_index(current_line),que))
					thread.start()
					current_line += 1
