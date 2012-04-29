import urllib2, sys, re
from bs4 import BeautifulSoup

def main():
    url = sys.argv[1]
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    og_el = soup.find(text=re.compile(sys.argv[2]))
    cur_el = og_el.parent
    elem_name_list = []
    elem_num_list = []
    while cur_el.name != '[document]':
        elem_name_list.insert(0, cur_el.name)
        found = False
        for i,el in enumerate(cur_el.parent.find_all(cur_el.name)):
            if el == cur_el:
                if not found:
                    found = True
                    elem_num_list.insert(0, i)
                else:
                    print 'ERROR: duplicate element found in children of parent'
        if not found:
            print 'ERROR: element not found in children of parent'
        cur_el = cur_el.parent
    for i in range(len(elem_name_list)):
        print elem_name_list[i]
        print elem_num_list[i]

if __name__ == "__main__":
    main()

