import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import re
import json
import time
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'

    }

domain = "https://itra.run"
now = datetime.datetime.today()
dateMin = now.strftime('%d/%m/%Y')
dateMax = datetime.datetime(day = now.day, month = now.month, year=now.year + 1).strftime('%d/%m/%Y')
print (dateMin)
print (dateMax)

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
    page = session.get(url,headers=headers, verify=False)
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
        country = re.search(r'\((.*?)\)', dct_2["Location of start"].strip()).group(1)
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


    logo = soup.select_one("div#calevt_lst img", src = True)
    
    if logo is not None:
        logo_url = logo["src"]
    else:
        logo_url = ""

    th = soup.select_one("div#calevt_fich tr th", onclick = True)

    if th is not None:
        stage = th.select_one("a.rightarr", onclick = True)
        params = eval(stage['onclick'].split(";")[0])
        global sum_distance, sum_elevation_gain, sum_descent, sum_refreshment_points, sum_time_limit

        sum_distance = sum_elevation_gain = sum_descent = sum_refreshment_points = sum_time_limit = 0
        try:

            sum_distance = reprDist(distance)[0]
        except Exception as ex:
            pass

        try:

            sum_elevation_gain = reprDist(elevation_gain)[0]
        except Exception as ex:
            pass


        try:
        
            sum_descent = reprDist(descent)[0]
        except Exception as ex:
            pass
            
        try:
        
            sum_refreshment_points = reprDist(refreshment_points)[0]
        except Exception as ex:
            pass
            
        try:
            sum_time_limit = get_sec(time_limit)
        except Exception as ex:
            sum_time_limit = 0
            pass
            
        calcSUMS(params)
        sum_time_limit = get_str(sum_time_limit)

    else:
        sum_distance = distance
        sum_elevation_gain = elevation_gain
        sum_descent = descent
        sum_refreshment_points = refreshment_points
        sum_time_limit = time_limit

    dct["Event"]   = Event
    dct["Race"]    = Race
    dct["Description"] = Description
    dct["Participants"] = participants 
    dct["Registration Opens"] = registr_open
    dct["Registration Closes"] = registr_close
    dct["Entry Fee"] = registr_fee
    dct["Sign Up"] = registr_url
    dct["Date"] = date
    dct["Starting Time"] = starting_time
    dct["Starting Point"] = starting_point
    dct["Country"] = country
    dct["SumDistance"] = sum_distance 
    dct["SumElevation Gain"] = sum_elevation_gain
    dct["SumDescent"] = sum_descent
    dct["SumRefreshment Points"] = sum_refreshment_points
    dct["SumTimeLimit"] = sum_time_limit #
    dct["Website"] = WEBSITE
    dct["CourseUrl"] = course_url
    # dct["CourseFileName"] = "" #
    dct["LogoPicURL"] = logo_url
    dct["ProfilePicURL"] = img_url
    # dct["ProfilePicFile Name"] = "" #
    dct["SourceUrl"] = source_url

    return dct

def calcSUMS(params):
    global sum_distance, sum_elevation_gain, sum_descent, sum_refreshment_points, sum_time_limit
    url = "https://itra.run/calend.php?mode=getEvt&id={}&annee={}&idc={}&idx={}".format(*params)
    session = requests.Session()
    session.max_redirects = 9999999
    dct = {}
    # url = url.strip('"')
    page = session.get(url,headers=headers, verify=False)
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
    elif len(_lst) == 2:
        h = 0
        m, s = _lst
        return int(h) * 3600 + int(m) * 60 + int(s)
    else:
        return 0


def get_str(time_sec):
    if time_sec >= 3600:
        return time.strftime('%H:%M:%S', time.gmtime(time_sec))
    else:
        return time.strftime('%M:%S', time.gmtime(time_sec))

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


def number_of_pages(main_url):
    session = requests.Session()
    session.max_redirects = 9999999
    page = session.get(main_url.format(1, dateMin, dateMax), headers=headers, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    nbpmax = soup.select_one("script").get_text().strip().split()[-2]
    nbpmax = int(re.findall(r"[-+]?\d*\.\d+|\d+", nbpmax)[0])

    return nbpmax

def parse_content(url, pageNo):
    lst = []
    session = requests.Session()
    session.max_redirects = 9999999

    page = requests.post(url, headers = headers, data = {'num_page': pageNo})

    soup = BeautifulSoup(page.text, "html.parser")
    Params = soup.select("div.race a", href = True)
    for param in Params:
        params = eval(param["onclick"].split(";")[0])
        lst.append(params)
    return lst
  
PAGE_URL = "https://itra.run/calend.php?mode=getcal&num_page={}&input_cal_rech=&ptsmin=0&ptsmax=6&montmin=0&montmax=14&finishmin=100&finishmax=600&periode=perso&dtmin={}&dtmax={}"
NUMBER_OF_PAGES = number_of_pages(PAGE_URL)
Data_list = []

for page in range(1, NUMBER_OF_PAGES + 1):
    URLS = []
    url = PAGE_URL.format(page, dateMin, dateMax)
    print ("Page ", page)
    params = parse_content(url, page)
    for param in params:
        URLS += parse_inner(param)
    print ("  Scrapping {} URLS".format(len(URLS)))
    
    for URL in URLS:
        Data_list.append(parse_inner2(URL))

fields = ['Event', 'Race', 'Description', 'Participants', 'Registration Opens', 'Registration Closes', 'Entry Fee', 'Sign Up', 'Date', 'Starting Time', 'Starting Point', 'Country', 'SumDistance', 'SumElevation Gain', 'SumDescent', 'SumRefreshment Points', 'SumTimeLimit', 'Website', 'CourseUrl', 'LogoPicURL', 'ProfilePicURL', 'SourceUrl']



with open('scrapped.csv', 'w', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fields)
    writer.writeheader()
    writer.writerows(Data_list)
    