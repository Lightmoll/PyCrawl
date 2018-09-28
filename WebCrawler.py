import re
import time
from utils import *
from interface import user_interface


valid_urls_file = "urls.txt"
not_valid_urls_file = "nv_urls.csv"
main_urls = ["i-onconnect.com", "members.i-onconnect.com"]
interface = user_interface(user_interface.ARG_MODE)

def get_urls(url):
    page = requests.get(url)                                    #getURL
    return re.findall("<a href=\"([^\">]+)\">", page.text)      #parseUrl

def search_urls(url):
    valid_urls = []
    nv_urls = []

    urls = get_urls(url)
    for i in range(len(urls)):                                  #handleExeptions
        try:
            if (urls[i][0] == "/" and urls[i][1] != "/"):
                urls[i] = conjugate_urls(url, urls[i])
            elif (urls[i][0:2] == '//'):
                urls[i] = "http://" + urls[i][2:]
        except IndexError:
            pass                                                #urlTooShort

    urls = check_dup_in_list(urls)

    for i in range(len(urls)):                                  #validadeUrls
        if valid_url(urls[i]):
            valid_urls.append(urls[i])
        else:
            if urls[i][:6] != "?lang=" and urls[i][:24] != "https://www.instagram.co":
                nv_urls.append((url, urls[i]))
                print(url, urls[i], sep="\t")
    a = valid_urls
    return [valid_urls, nv_urls]


def save_urls(urls):
    global main_urls
    with open(valid_urls_file, "r", encoding="utf-8") as table_r:
        existing_urls = table_r.readlines()

    with open(valid_urls_file, "a", encoding="utf-8") as table:
        for i in range(len(urls[0])):
            for j in range(len(existing_urls)):
                existing = existing_urls[j][:-1].split("//")[1]
                new = urls[0][i].split("//")[1]
                if (existing == new):
                    unique = False
                    break
                else:
                    unique = True

            if unique:
                if urls[0][i].split("/")[2] == main_urls[0] or urls[0][i].split("/")[2] == main_urls[1]:
                    table.write(urls[0][i] + "\n")
    with open(not_valid_urls_file, "a", encoding="utf-8") as nv_table:
        for i in range(len(urls[1])):
            nv_table.write(urls[1][i][0] + "," + urls[1][i][1] + "\n")


def main():
    global current_line
    first_time = time.time()
    try:
        with open(valid_urls_file, "r", encoding="utf-8") as table:
            table_content = table.readlines()
            current_url = table_content[current_line][:-1]
            urls = search_urls(current_url)
            if urls[0] != None: #In case there are no new links on site
                save_urls(urls)
            time_took = round(time.time() - first_time,4)
            print(current_line, time_took, current_url, sep="\t")
            time_table.write(str(time_took) + ",")
            current_line += 1
    except IndexError:
        print("END OF FILE REACHED")
        quit(0)

if __name__ == '__main__':
    current_line = interface.get_values()["start_line"]
    #current_line = 0
    time_table = open("time_table.csv", "w")

    while True:
        main()

current_line = 0
time_table = open("time_table.csv", "w")
main()
