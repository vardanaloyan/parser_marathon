import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import re
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
domain = "https://marathons.ahotu.com/"

start_page = 1
end_page = 2

def parse_page(url):
    lst = []
    session = requests.Session()
    session.max_redirects = 9999999
    url = url.strip('"')
    page = session.get(url,headers=header, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    tmp = soup.find_all("a", {"class" : "list-group-item mb-2 pb-0 calendar"}, href=True)
    for i in tmp:
        lst.append((domain+i['href']))
    return lst

def _tmp(val):
    if val == "":
        return False
    else:
        return True

def parse_content(url):
    dct = {}
    session = requests.Session()
    session.max_redirects = 9999999
    url = url.strip('"')
    page = session.get(url,headers=header, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    country = soup.select("nav ol li")
    country = [i.get_text().strip() for i in country]
    # Country = country[-2]
    Region = country[0]
    website = soup.select_one("div.card-body a", href = True)
    Website = "" if website is None else website["href"]
    dct["WEBSITE"] = Website
    dct["Country"] = ""
    dct["RegionString"] = "/".join(country)
    # Event
    event = soup.select_one("div.col-12 h1").get_text()
    dct["Event"] = event
    # Starting Point
    starting_point = country[-1]
    dct["Starting Point"] = starting_point
    # Description
    description = soup.find("descriptions").get_text().strip()
    dct["Description"] = description
    # Sign Up
    try:
        registry = soup.find("a" , {"class" : "btn btn-secondary"}, href = True)["href"]
    except:
        registry = ""
    dct["Sign Up"] = registry
    # Reference URL
    reference_url = url
    dct["Reference URL"] = url

    races = soup.select("div.card-body div.mb-3")
    # print ("Len of Races: ", len(races), url)

    for num, race in enumerate(races):
        dct["Tag"] = dct["Date"] = dct["Starting Time"] = dct["Type"] = dct["Distance"] = dct["Race"] = ""
        attrs = [i.get_text().strip() for i in race.select("div.col")]
        Tags =  [i.get_text() for i in race.select("div.col span")]
        attrs = list(filter(lambda x: True if x != "" else False, attrs))
        try:
            Races = race.select_one("h3").get_text().replace('[',"").replace(']',"")
        except:
            continue
        dct["Tag"] = str(Tags).replace('[',"").replace(']',"").replace("'","")  # attrs[-1]
    
        _lst = [i.strip() for i in attrs[0].split("-")]
        try:
            dct["Date"], dct["Starting Time"] = _lst[0], _lst[1]
        except IndexError:
            dct["Date"] = _lst[0]
            dct["Starting Time"] = ""

        dct["Date"] = re.sub(r'\([^)]*\)', '', dct["Date"]).strip()
        dct["Type"] = attrs[1]
        dct["Distance"] = attrs[2]
        dct["Race"] = Races

        yield dct.copy()


fields = ["Event", "Race", "Country", "RegionString",  "Tag", "Date", "Starting Time", "Type", "Distance", "Starting Point", "Description", "Sign Up", "Reference URL", \
"WEBSITE"]

# Lst = []
# for page in range(start_page, end_page):
#     links = parse_page("https://marathons.ahotu.com/calendar?page=%d" % page)
#     for link in links:
#         print ("Processing: %s" % link)
#         for dct in parse_content(link):
#             Lst.append(dct)

# with open('scrapped.csv', 'w', encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fields)
#     writer.writeheader()
#     writer.writerows(Lst)

for dct in parse_content("https://marathons.ahotu.com//event/dead-sea-ultra-marathon"):
    print (dct)