import requests
import urllib3
import os


def file_len(f_path):  # never used
	with open(f_path, "r") as f:
		try:
			for i, l in enumerate(f):
				pass
			return i + 1
		except UnboundLocalError:
			print("URL-List empty")

def list_to_str(list):
	out = ""
	for i in range(len(list)):
		out += list[i] + "\n"
	return out


def file_setup(file, content):
	try:
		with open(file, "w", encoding="utf-8") as opened_file:
			opened_file.write(content)
	except FileNotFoundError:
		res_path = ""
		path = file.split("/")[:-1]
		for i in range(len(path)):
			res_path += path[i] + "/"
		os.mkdir(res_path)
		file_setup(file,content)

def check_dup_in_list(_list, start_i=0, start_j=0):
	list = _list
	try:
		for i in range(len(list)):
			start_i = i
			for j in range(len(list)):
				if i != j and list[i] == list[j]:
					start_j = j
					list.pop(j)
	except IndexError:  # IndexErrors are normal, because we loop over a list, which gets smaller
		check_dup_in_list(list, start_i, start_j)  # Starts, so that you don't loop over already checked entries
	return list


def valid_url(url):
	try:
		head = requests.head(url)
		if (head.status_code == 200):
			if (head.headers._store["content-type"][1][:9] == "text/html"):
				return True
		return False
	except (requests.exceptions.InvalidSchema,
			requests.exceptions.InvalidURL,
	        requests.exceptions.ConnectionError,
	        requests.ReadTimeout,
	        requests.exceptions.MissingSchema,
			urllib3.exceptions.LocationParseError,
			requests.exceptions.InvalidURL,
			requests.exceptions.SSLError,
	        KeyError):
		return False


def conjugate_urls(base_url, addition):
	slash_pos = base_url.split("/")
	based_url = ""
	if len(slash_pos) >= 3:
		for i in range(3):
			based_url += slash_pos[i] + "/"
		res = based_url[:-1] + addition
		return res
	else:
		if base_url[-1:] == "/":
			return base_url[:-1] + addition
		else:
			return base_url + addition
