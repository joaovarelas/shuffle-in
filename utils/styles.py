from bs4 import BeautifulSoup
import requests
import json
import time


f = open("styles.txt", "a")

url = "https://reference.discogs.com/browse/style?page="
for i in range(1, 40):
    print("---------------------" + str(i) + "----" )

    r = requests.get(url+str(i), headers={"User-Agent": "Mozilla Firefox"})
    soup = BeautifulSoup(r.text)
    divs = soup.find_all("div", {"id": "cards"})[0]
    data = divs["data-props"]

    js = json.loads(data)
    for ent in js["data"]["entities"]:
        print(ent["title"])
        f.write(ent["title"]+"\n")

    
f.close()
