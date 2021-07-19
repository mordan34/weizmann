# importing the libraries
from bs4 import BeautifulSoup
import requests
from lxml import html

url="https://prodis.weizmann.ac.il/ords306/isprod/f?p=133:101:5308135562788:::::"
custom_User_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
# Start the session
session = requests.session()

# Create the payload
payload = {'P101_USERNAME':'[mordan]', 
          'P101_PASSWORD':'[Makeachange67]'
         }

result = session.post(
	url, 
	data = payload, 
	headers = dict(referer=url)
)

result = session.get(
	url, 
	headers = dict(referer = url)
)

tree = html.fromstring(result.content)
print(result.content)