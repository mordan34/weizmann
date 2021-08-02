# importing the libraries
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


url= 'https://prodis.weizmann.ac.il/'
login_route= 'ords306/isprod/wwv_flow.accept'

payload = {'P101_USERNAME':'mordan', 
           'P101_PASSWORD':'Makeachange67'
}

header= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'origin': url, 'referer': url + login_route}


with requests.session() as s:
    r= s.post(url + 'ords306/isprod/f?p=133:4', headers=header, data=payload)
    pprint(r.text)

    response = s.get(url + 'ords306/isprod/f?p=133:4:')
    #print(response.text)
    #soup= bs(s.get(url + 'ords306/isprod/f?p=133:4:').text, 'html.parser')
    #print(soup)
    #tbody=soup.find('table', id='15077363850397519')
  