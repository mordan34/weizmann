# importing the libraries
import requests,requests.cookies
from bs4 import BeautifulSoup as bs

url= 'https://prodis.weizmann.ac.il/'
login_route= 'ords306/isprod/wwv_flow.accept'
data_route= 'ords306/isprod/f?p=133:4:'
new_url= 'https://prodis.weizmann.ac.il/ords306/isprod/f?p=133:4:212727186819::NO:::'


response = requests.get(url + login_route)
for cookie in response.cookies:
    print('cookie domain = ' + cookie.domain)
    print('cookie name = ' + cookie.name)
    print('cookie value = ' + cookie.value)
    print('*************************************')

# Create a RequestsCookieJar object.
cookies_jar = requests.cookies.RequestsCookieJar()

# Add first cookie
cookies_jar.set('ZNPCQ003-38363900', '984c9b62', domain='.weizmann.ac.il', path='/')

# Add second cookie
cookies_jar.set('ORA_WWV_APP_133', 'ORA_WWV-HdLCv68Y_kOz3uk1UB4W_DrU', domain='prodis.weizmann.ac.il', path='/ords306/isprod')

response = requests.get(url + data_route, cookies=cookies_jar)
print(response.text)