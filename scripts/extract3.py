# importing the libraries
import requests,requests.cookies
from bs4 import BeautifulSoup as bs


url= 'https://prodis.weizmann.ac.il/'
login_route= 'ords306/isprod/wwv_flow.accept'
data_route= 'ords306/isprod/f?p=133:4:'

payload = {'P101_USERNAME':'mordan', 
           'P101_PASSWORD':'Makeachange67'
}

header= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'origin': url, 'referer': url + login_route}

cookies_jar = requests.cookies.RequestsCookieJar()
#for cookie in response.cookies:
#    cookies_jar.set(cookie.name, cookie.value, domain=cookie.domain)

# Add first cookie
cookies_jar.set('ZNPCQ003-38363900', '984c9b62', domain='.weizmann.ac.il', path='/')

# Add second cookie
cookies_jar.set('ORA_WWV_APP_133', 'ORA_WWV-HdLCv68Y_kOz3uk1UB4W_DrU', domain='prodis.weizmann.ac.il', path='/ords306/isprod')

#response = requests.get(url + login_route, cookies=cookies_jar)
#print(response.text)

with requests.session() as s:
    r= s.post(url + login_route, headers=header, data=payload, cookies=cookies_jar)
    print(r.text)
    print(cookies_jar)
    for cookie in s.cookies:
        cookies_jar.set(cookie.name, cookie.value, domain=cookie.domain, path= '/ords306/isprod')
    response = s.get(url + data_route)
    #print(response.text)
    #soup= bs(s.get(url + 'ords306/isprod/f?p=133:4:').text, 'html.parser')
    #print(soup)
    #tbody=soup.find('table', id='15077363850397519')
  