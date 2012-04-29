import urllib2
import sys
from bs4 import BeautifulSoup
import re


def main():
    #url = sys.argv[1]
    url = "http://en.wikipedia.org/wiki/Web_scraping"
    url = "http://sfbay.craigslist.org/nby/muc/2985476465.html"
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    web_page = opener.open(url)
    soup = BeautifulSoup(web_page.read())

    text_to_match = soup.find(text=re.compile("Blues/Country Bass Player available"))


    """This section is for training""" 
    #ToMatch [(name, attrs, ith name in parent)]
    path = []
    current_element = text_to_match.parent
    while type(current_element) != type(soup):
        

        parent = current_element.parent
        current_type = current_element.name
        
        for i, ele in enumerate(parent.find_all(current_type)):
            parents_nth_tag = i
            if ele == current_element:
                break
        
        match = (current_element.name, current_element.attrs, parents_nth_tag)
        path.append(match)
        current_element = current_element.parent



    """This section actually matches the data"""
    web_page = opener.open(sys.argv[1])
    soup = BeautifulSoup(web_page.read())
    path.reverse()
    current_element = soup
    for node in path:
        tag_type_elements = current_element.find_all(node[0])
        element = tag_type_elements[node[2]]
        if element.attrs == node[1]:
            print "Attribute matched"
        else:
            print "Attribute did not match"
        print element.attrs, node[1]
        #print element.name, node[0]
        current_element = element
    
    
    print current_element
        
#for child in list(soup.contents):
        #print child




if __name__ == "__main__":
    main()
