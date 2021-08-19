##################################### Method 1
import mechanize
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
import html2text

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]
url="https://prodis.weizmann.ac.il/ords306/isprod/f?p=133:101:5308135562788:::::"
# The site we will navigate into, handling it's session
br.open(url)

# View available forms
for f in br.forms():
    print(f)

# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=0)

# User credentials
br.form['P101_USERNAME'] = 'mordan'
br.form['P101_PASSWORD'] = ''

# Login
br.submit()

print(br.open('url').read())