import urllib2
from bs4 import BeautifulSoup
import re


def main():
    url = "http://sfbay.craigslist.org/pen/app/2985634788.html"
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    web_page = opener.open(url)
    soup = BeautifulSoup(web_page)
    all_divs = soup.find_all('div')
    print type(soup.body)
    for x in soup.body.children:
        if isinstance(x, NavigationString):
            print x
        if isinstance(x, Tag):
            
#x.string.replace_with("trololo")
#x.replace_with(x.string.replace(" ", ""))
        #print soup.get_text()
#x.string.replace_with(x.string.replace(" ", ""))





if __name__ == "__main__":
    main()
