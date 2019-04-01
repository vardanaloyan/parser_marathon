import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import re
import json
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'

    }

headers =\
{ 
# "Host": "itra.run",
# "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
# "Accept": "*/*",
# "Accept-Language": "en-US,en;q=0.5",
# "Accept-Encoding": "gzip, deflate, br",
# "Referer": "https://itra.run/page/290/Calendar.html",
# "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
# "X-Requested-With": "XMLHttpRequest",
# "Content-Length": 160,
# "Connection": "keep-alive",
# "Cookie": "PHPSESSID=1m78gn86k822fur2ke4n4qatd6; langue_affich=_en; __utma=186997872.1875485845.1553926291.1553926291.1553926291.1; __utmb=186997872.1.10.1553926291; __utmc=186997872; __utmz=186997872.1553926291.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1",
# "Cache-Control": "max-age=0, no-cache",
# "Pragma": "no-cache"
}

# domain = "https://marathons.ahotu.com/"
domain = "https://itra.run"
start_page = 1
end_page = 2



def _tmp(val):
    if val == "":
        return False
    else:
        return True

def showEvt(*args):
    return args

def parse_inner2(url):
    session = requests.Session()
    session.max_redirects = 9999999
    dct = {}
    # url = url.strip('"')
    page = session.get(url,headers=header, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    Event = soup.select_one("div#calevt_titre").contents[-1].strip() 
    Race = soup.select_one("div#race-container h2").contents[-1].strip() #get_text(strip=True)
    WEBSITE = soup.select_one("div#calevt_titre > div > a.web", href = True)
    img_url = soup.select_one("div#im-container a", href = True)
    All_info = soup.select("div#calevt_fich tr") #get_text(strip=True)
    lst_1 = []
    dct_2 = {}
    registr_url = ""


    for info in All_info:
        tds = info.select("td")
        if len(tds) == 2:
            dct_2[tds[0].get_text().strip()] = tds[1].get_text().strip()
        elif len(tds) == 1:
            if tds[0].get_text().strip() != "":
                if tds[0].select_one("a", href = True) is not None:
                    registr_url = tds[0].select_one("a", href = True)["href"]
                else:
                    lst_1.append(tds[0].get_text().strip())

    try:
        registr_fee = lst_1[lst_1.index("Registration fees")+1]
    except ValueError:
        registr_fee = ""

    print ("-"*15)
    # print (dct_2.keys())
    try:
        registr_open = dct_2["Opening of registration"]
    except:
        registr_open = ""
    try:
        registr_close = dct_2["Closure of registration"]
    except:
        registr_close = ""

    date_time = dct_2["Date and time of start"].split()
    starting_time = date_time.pop().strip()
    location_start = dct_2["Location of start"].split()
    date = " ".join(date_time)

    try:
        starting_point = location_start[0]
    except:
        starting_point = ""
        
    
    try:
        country = re.sub('[(){}<>]', '', location_start[1])
    except:
        country = ""

    try:
        distance = re.sub('[(){}<>]', '', dct_2["Distance"]).split()[0].strip()
    except:
        distance = ""

    try:
        elevation_gain = dct_2["Ascent"].strip()
    except:
        elevation_gain = ""

    try:
        descent = dct_2["Descent"].strip()
    except:
        descent = ""
    
    try:
        refreshment_points = dct_2["Refreshment points"].strip()
    except:
        refreshment_points = ""
    
    try:
        time_limit = dct_2["Maximum time"].strip()
    except:
        time_limit = ""
    
    source_url = url
    try:
        course_url = soup.select_one("div#calevt_fich iframe", src = True)["src"]
    except:
        course_url = ""
    try:
        participants = dct_2["Number of participants"].strip()
    except:
        participants = ""

    description = soup.select("div.content p")
    Description = ""
    if len(description) != 0:
        for c, desc in enumerate(description):
            if c == 1:
                 Description += "\nDescription in English\n"
            Description += desc.get_text()
    else:
        Description = ""

    if img_url is not None:
        img_url = domain + img_url["href"]
    else:
        img_url = ""

    if WEBSITE is not None:
        WEBSITE = WEBSITE["href"]
    else:
        WEBSITE = ""

    th = soup.select_one("div#calevt_fich tr th", onclick = True)
    if th is not None:
        stage = th.select_one("a.rightarr", onclick = True)
        params = eval(stage['onclick'].split(";")[0])
        global sum_distance, sum_elevation_gain, sum_descent, sum_refreshment_points, sum_time_limit

        sum_distance = sum_elevation_gain = sum_descent = sum_refreshment_points = sum_time_limit = 0
        try:

            sum_distance = reprDist(distance)[0]
        except Exception as ex:
            print (ex)

        try:

            sum_elevation_gain = reprDist(elevation_gain)[0]
        except Exception as ex:
            print (ex)

        try:
        
            sum_descent = reprDist(descent)[0]
        except Exception as ex:
            print (ex)

        try:
        
            sum_refreshment_points = reprDist(refreshment_points)[0]
        except Exception as ex:
            print (ex)

        try:
            sum_time_limit = get_sec(time_limit)
        except Exception as ex:
            sum_time_limit = 0
            print (ex)

        calcSUMS(params)
        # print (Event, " ; ", Race)
        print (source_url)
        print (sum_distance , sum_elevation_gain , sum_descent , sum_refreshment_points, get_str(sum_time_limit))

        # print (th.get_text().strip())
        # print (params)
    # "https://itra.run/calend.php?mode=getEvt&id=2953&annee=2019&idc=16457&idx=2"

    dct["Event"]   = Event
    dct["Race"]    = Race
    dct["WEBSITE"] = WEBSITE

    return dct

def calcSUMS(params):
    global sum_distance, sum_elevation_gain, sum_descent, sum_refreshment_points, sum_time_limit
    url = "https://itra.run/calend.php?mode=getEvt&id={}&annee={}&idc={}&idx={}".format(*params)
    session = requests.Session()
    session.max_redirects = 9999999
    dct = {}
    # url = url.strip('"')
    page = session.get(url,headers=header, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    All_info = soup.select("div#calevt_fich tr") #get_text(strip=True)
    lst_1 = []
    dct_2 = {}

    for info in All_info:
        tds = info.select("td")
        if len(tds) == 2:
            dct_2[tds[0].get_text().strip()] = tds[1].get_text().strip()
        elif len(tds) == 1:
            if tds[0].get_text().strip() != "":
                if tds[0].select_one("a", href = True) is not None:
                    registr_url = tds[0].select_one("a", href = True)["href"]
                else:
                    lst_1.append(tds[0].get_text().strip())

    try:
        distance = re.sub('[(){}<>]', '', dct_2["Distance"]).split()[0].strip()
    except:
        distance = ""

    try:
        elevation_gain = dct_2["Ascent"].strip()
    except:
        elevation_gain = ""

    try:
        descent = dct_2["Descent"].strip()
    except:
        descent = ""
    
    try:
        refreshment_points = dct_2["Refreshment points"].strip()
    except:
        refreshment_points = ""
    
    try:
        time_limit = dct_2["Maximum time"].strip()
    except:
        time_limit = ""

    sum_distance += reprDist(distance)[0]
    sum_elevation_gain += reprDist(elevation_gain)[0]
    sum_descent += reprDist(descent)[0]
    sum_refreshment_points += reprDist(refreshment_points)[0]
    sum_time_limit += get_sec(time_limit)

    th = soup.select_one("div#calevt_fich tr th", onclick = True)
  
    if th is not None:
        try:
            stage = th.select_one("a.rightarr", onclick = True)
            params = eval(stage['onclick'].split(";")[0])
            calcSUMS(params)
        except:
            return 1


def get_sec(time_str):
    _lst = time_str.split(':')
    if len(_lst) == 3:
        h, m, s = _lst
        return int(h) * 3600 + int(m) * 60 + int(s)
    else:
        h = 0
        m, s = _lst
        return int(h) * 3600 + int(m) * 60 + int(s)


def get_str(time_sec):
    return time.strftime('%H:%M:%S', time.gmtime(time_sec))

def reprDist(val):
    retval = float(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0])
    unit = val.replace(re.findall(r"[-+]?\d*\.\d+|\d+", val)[0], "").strip()

    return retval, str(retval)+unit

def parse_inner(lst_item):
    urls = []
    url = "https://itra.run/calend.php?ide={0}&mode=getEvt&id={0}&annee={1}&opendirect=1".format(*lst_item)
    session = requests.Session()
    page = session.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")


    race_params =  [eval(i['onclick'].split(";")[0]) for i in soup.select("div#calevt_lst a", href = True)]
    for race_param in race_params:
        sub_url = "https://itra.run/calend.php?ide={0}&mode=getEvt&id={0}&annee={1}&idc={2}".format(*race_param)
        urls.append(sub_url)
    return urls


def parse_content():
    lst = []
    url = "https://itra.run/calend.php?mode=getcal&num_page=&input_cal_rech=&ptsmin=0&ptsmax=6&montmin=0&montmax=14&finishmin=100&finishmax=600&periode=perso&dtmin=01/04/2019&dtmax=01/04/2020"
    session = requests.Session()
    session.max_redirects = 9999999

    page = session.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    Params = soup.select("div.race a", href = True)
    for param in Params:
        params = eval(param["onclick"].split(";")[0])
        lst.append(params)

    return lst
  
URLS = []
params = parse_content()
for param in params:
    URLS += parse_inner(param)

Data_list = []
for URL in URLS:
    Data_list.append(parse_inner2(URL))

fields = ["Event", "Race", "WEBSITE"]

# fields = ["Event", "Race", "Country", "RegionString",  "Tag", "Date", "Starting Time", "Type", "Distance", "Starting Point", "Description", "Sign Up", "Reference URL", \
# "WEBSITE"]


with open('scrapped.csv', 'w', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fields)
    writer.writeheader()
    writer.writerows(Data_list)
    