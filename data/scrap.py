import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

page = "https://www.defense.gov/Resources/Military-Departments/DOD-Websites/"
div = "DGOVWebsitesLinks"
req = requests.get(page)
soup = BeautifulSoup(req.text, features="html.parser")
link_box = soup.find("div", {"class": div})
dods_link = {}
children = link_box.findChildren("a", recursive=True)

for child in children:
    href = child["href"]
    title = child.text

    url = urlparse(href)

    dods_link[url.netloc] = ""

print(dods_link.keys())
with open("data.txt", "a") as f:
    for link in dods_link.keys():
        f.write(f"{link}\n")
