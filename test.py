import requests
from bs4 import BeautifulSoup
import urllib3
import csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
domain = "https://marathons.ahotu.com/"

start_page = 1
end_page = 4663

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
    country = [i.get_text() for i in country]
    Country = country[-2]
    Region = country[0] 
    dct["Country"] = Country
    dct["Region"] = Region
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

    races = soup.select("div.mb-3")
    for race in races:
        attrs = [i.get_text().strip() for i in race.select("div.col")]
        attrs = list(filter(lambda x: True if x != "" else False, attrs))
        Races = [race.select_one("h3").get_text()]
        dct["Tag"] = attrs[-1]
        _lst = [i.strip() for i in attrs[0].split("-")]
        try:
            dct["Date"], dct["Starting Time"] = _lst[0], _lst[1]
        except IndexError:
            dct["Date"] = _lst[0]
            dct["Starting Time"] = ""

        dct["Type"] = attrs[1]
        dct["Distance"] = attrs[2]
        dct["Race"] = Races
        yield dct


fields = ["Event", "Race", "Country", "Region",  "Tag", "Date", "Starting Time", "Type", "Distance", "Starting Point", "Description", "Sign Up", "Reference URL"]

lst = []
for page in range(start_page, end_page):
    links = parse_page("https://marathons.ahotu.com/calendar?page=%d" % page)
    for link in links:
        for dct in parse_content(link):
            lst.append(dct)

with open('scrapped.csv', 'w', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fields)
    writer.writeheader()
    writer.writerows(lst)



