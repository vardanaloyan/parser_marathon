import requests
import json
headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
headers= {}

Data =dict(
	mode="getcal", \
	num_page=2, \
	input_cal_rech=None, \
	ptsmin=0, \
	ptsmax=6, \
	montmin=0, \
	montmax=14, \
	finishmin=100, \
	finishmax=600, \
	periode="perso", \
	dtmin="03/04/2019", \
	dtmax="03/04/2020" \
	)
page = requests.post('https://itra.run/calend.php?mode=getcal&num_page=6&input_cal_rech=&ptsmin=0&ptsmax=6&montmin=0&montmax=14&finishmin=100&finishmax=600&periode=perso&dtmin=03%2F04%2F2019&dtmax=03%2F04%2F2020', headers = headers, data = {'num_page': 3})

# url = "https://itra.run/calend.php?mode=getcal&num_page=2&input_cal_rech=&ptsmin=0&ptsmax=6&montmin=0&montmax=14&finishmin=100&finishmax=600&periode=perso&dtmin=03/04/2019&dtmax=03/04/2020"
# page = requests.get(url, headers=headers, verify=False)
# print(page.status_code)

# url = "https://itra.run/calend.php"
# page = requests.get(url, params = Data, headers=headers, verify=False)
# print (page.url)
# from bs4 import BeautifulSoup
#soup = BeautifulSoup(page.text, "html.parser")

print (page.text)