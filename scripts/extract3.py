# importing the libraries
import requests
from bs4 import BeautifulSoup


loginurl= ('https://prodis.weizmann.ac.il/ords306/isprod/f?p=133:4:7531191127977::NO:::')
secure_url= ('https://prodis.weizmann.ac.il/ords306/isprod/wwv_flow.accept')
custom_User_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

payload = {'P101_USERNAME':'mordan', 
           'P101_PASSWORD':'Makeachange67'
}

