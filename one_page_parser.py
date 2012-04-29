import urllib2
import sys
from bs4 import BeautifulSoup
import re


def matches_input(tag):
    return tag.find(string_to_match) != -1

#string_to_match = "Recital:  Sandrine Piau, soprano, Susan Manoff, piano"
string_to_match = sys.argv[2]
def main():
    #url = sys.argv[1]
    url = "http://en.wikipedia.org/wiki/Web_scraping"
    url = "http://sfbay.craigslist.org/nby/muc/2985476465.html"
    #url = "http://events.berkeley.edu/"
    url = sys.argv[1]
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    web_page = opener.open(url)
    soup = BeautifulSoup(web_page.read())

    text_to_match = soup.find(text=matches_input)


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

    greatest_false = 1
    best_match = []
    for i in range(len(path)):
        for j in range(len(path)):
            test_values = recursive_match(path, i, j, current_element)
            if not isinstance(test_values, list):
                continue
            if not test_values:
                continue
            if len(test_values) > 300 or len(test_values) < 2:
                continue
            false_count = 0
            for x in test_values:
                if x == False or x is None:
                    false_count += 1
            false_count /= (len(test_values) * 1.0)
            if false_count < greatest_false:
                best_match = test_values
                greatest_false = false_count
            #print test_values
    print best_match
    """for node in path:
        tag_type_elements = current_element.find_all(node[0])
        element = tag_type_elements[node[2]]
        

        if element.attrs == node[1]:
            print "Attribute matched"
        else:
            print "Attribute did not match"
        print element.attrs, node[1]
        #print element.name, node[0]
        current_element = element    
    print "\n\n\n" + current_element.string """
        
#for child in list(soup.contents):
        #print child


#(element_name, element attrs, parents_nth_tag)
def recursive_match(path, i, j, current_element):
    if i == len(path) - 1:
        return current_element.string
    node = path[i]
    tag_type_elements = current_element.find_all(node[0])
    if i == j:
        return [recursive_match(path, i + 1, j, next_element) for next_element in tag_type_elements]
    else:
        if len(tag_type_elements) <= node[2]:
            return False
        next_element = tag_type_elements[node[2]]
        if next_element.attrs == node[1]:
            x = 1
#print "Attribute matched"
        else:
            x = 2
            #print "Attribute did not match"
        current_element = next_element
        return recursive_match(path, i + 1, j, current_element)
    
    


if __name__ == "__main__":
    main()
