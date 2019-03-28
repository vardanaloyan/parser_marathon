import requests
from bs4 import BeautifulSoup
import urllib3
import csv
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
domain = "https://marathons.ahotu.com/"

def parse_page(url):
    lst = []
    session = requests.Session()
    session.max_redirects = 9999999
    url = url.strip('"')
    page = session.get(url,headers=header, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    # author_program = soup.find('h1', {'class': 'product_title entry-title'}).get_text()
    # tmp = author_program.split("–")
    # author_name = tmp[0].strip()
    # product = "".join(tmp[1:]).strip()
    # retail_price = soup.find_all('span', {'class': 'woocommerce-Price-amount amount'})
    tmp = soup.find_all("a", {"class" : "list-group-item mb-2 pb-0 calendar"}, href=True)
    # print (len(tmp))
    for i in tmp:
        # print (domain+i['href'])
        lst.append((domain+i['href']))
    return lst

    # sales_price = soup.select_one("p.price > ins span").get_text()
    # category = soup.select_one("div.product_meta > span.posted_in a").get_text()
    # tags = soup.select("div.product_meta > span.tagged_as a")
    # tags = [i.get_text() for i in tags]

    # dct = {"URL": url, "Author Name": author_name, "Product Name": product, "Retail Price": retail_price, "Sales Price": sales_price, \
    # "Category": category, "Tags": tags}

    # return dct
def parse_content(url):
    dct = {}
    session = requests.Session()
    session.max_redirects = 9999999
    url = url.strip('"')
    page = session.get(url,headers=header, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    country = soup.select("nav ol li")
    country = [i.get_text() for i in country]
    
    # Event
    event = soup.select_one("div.col-12 h1").get_text()

    # Starting Point
    starting_point = country[-1]
    # Description
    description = soup.find("descriptions").get_text().strip()
    # Sign Up
    registry = soup.find("a" , {"class" : "btn btn-secondary"}, href = True)["href"]
    # Reference URL
    reference_url = url

    races = soup.select("div.mb-3")
    for race in races:
        attrs = [i.get_text() for i in race.select("div.col")]
        Races = [race.select_one("h3").get_text()]

    # print (len(attrs))
    # for i in attrs:
    #     print(i.get_text().strip())

    # print (registry)


fields = ["URL", "Author Name", "Product Name", "Retail Price", "Sales Price", "Category", "Tags"]

links = parse_page("https://marathons.ahotu.com/calendar?page=1")
parse_content(links[0])

# with open("urls.txt", "r") as f:
#     lst = []
#     for line in f:
#         try:
#             lst.append(parse(line.strip()))
#         except: pass

# with open('basic.csv', 'w', encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fields)
#     writer.writeheader()
#     writer.writerows(lst)



