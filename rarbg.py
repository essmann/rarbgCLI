import requests
from bs4 import BeautifulSoup
import sys
import os
import winreg as reg  # Import registry module for Windows
import re
import json
from qbittorrent import add_magnet_to_qbittorrent

config = {"max_pages_search": 2, 
          "max_url_display": 20,
          "default_category": "movies",
          "quality_filters": ["1080p", "2160p"]
          
          }
 
filename = 'config.txt'


# Check if the file exists in the current working directory
if not os.path.exists(filename):
    # If it doesn't exist, create the file
    with open(filename, 'w') as f:
        json.dump(config, f, indent = 4) 
    print(f"{filename} created.")
else:
      # If the file exists, load the JSON data
    with open(filename, 'r') as f:
        config = json.load(f)
    print(f"Data loaded from {filename}.")
print(config)
testing = False
quality = config["quality_filters"] if config["quality_filters"] else ["1080p", "2160p"]
urls = []
filtered_urls = []



if(not testing):
    #name = sys.argv[1]
    for arg in sys.argv:
        if '-m' in arg:
            category = "movies"
        elif "-tv" in arg:
            category = "tv"
        elif "-g" in arg:
            category = "games"
        else:
            category = config["default_category"]

#print(category)
try:
    name = sys.argv[1]
except:
    name = input("Invalid input. Select a Name and category: ")

params = {
    'search':  name,
    'order': 'size',
    'category[]':category,
    'by': 'DESC'
}
def getMaxPages():
        max = 0
        try:
             page_div = soup.find("div", id="pager_links")
             page_tags = page_div.find_all("a")
        except:
            print("no pages found")
            return 1
        
        length = len(page_tags)
        for element in page_tags:
            if element.string != '>>' :
                if int(element.string) > max:
                    max = int(element.string)
            
        #max_page_number = int(page_tags[length-2].string) 
        return max
def getTdData(tr):
  
        film_td = tr.contents[3]
        seeders = int(tr.contents[11].contents[0].string)
        leeches = int(tr.contents[13].string)
        size = tr.contents[9].string
        url_part = film_td.find("a")["href"]
        href = "https://rargb.to" + url_part
        return {"href": href, "leeches": leeches, "seeders": seeders, "size":size, "url_part": url_part}
    
###INITIAL URL
response = requests.get('https://rargb.to/search', params=params)
soup = BeautifulSoup(response.text, 'html.parser')
max_pages = getMaxPages()
#####

def getUrls(page_number=1):
    if(page_number==1):
        url = 'https://rargb.to/search'
    else:
        url = 'https://rargb.to/search/{0}'.format(page_number)
    response = requests.get(url, params=params)
    print("PAGE: ", page_number)
    print("URL: ", response.url)

    soup = BeautifulSoup(response.text, 'html.parser')
    tr = soup.find_all("tr", class_="lista2")
   
    for t in tr:
        data = getTdData(t)
        urls.append(data)
  
page = 1
if(config["max_pages_search"] < max_pages):
    pages_to_search = config["max_pages_search"]
else:
    pages_to_search = max_pages
    
while(page<=pages_to_search):
    getUrls(page)
    page+=1



for url in urls:
    regex_url = re.split(r"[-.\s]+", url["url_part"])
    for filter in quality:
        if filter in  regex_url:
            url["quality"] = filter
            filtered_urls.append(url)


def sortBySeeders():
    
    length = len(filtered_urls)-1
    i = 0
    j = 0
    while(i<length):
        j = 0
        #current_element = filtered_urls[i]["seeders"]
        #next_element = filtered_urls[i+1]["seeders"]
        while(j<length):
            
                current_element = filtered_urls[j]["seeders"]
                next_element = filtered_urls[j+1]["seeders"]
                if current_element < next_element:
                    temp = filtered_urls[j]
                    filtered_urls[j] = filtered_urls[j+1]
                    filtered_urls[j+1] = temp
                j+=1
                
                
        i+=1
    
sortBySeeders()


def displayUrls(max_display = 20):
    max_display = config["max_url_display"]
    
    count = 0
    for url in filtered_urls:
        print("[{3}] Quality: {0} | Seeders: {1} | URL: {2}".format(url["quality"], url["seeders"], url["url_part"], count)  )
        count+=1
        if count==max_display:
            break
def getMagnet(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    td = soup.find("td", class_="lista")
    magnet = td.find("a")["href"]
    return magnet

    
displayUrls()
print("Select a torrent: ")
index = int(input())
torrent_url = filtered_urls[index]["href"]

magnet = getMagnet(torrent_url)

add_magnet_to_qbittorrent(magnet)





