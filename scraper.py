import urllib2, sys, re
from bs4 import BeautifulSoup

def main():
    url = sys.argv[1]
    opener = urllib2.build_opener()
    opener.addheaders[('User-agent', 'Mozilla/5.0')]
    page = opener.open(url)
    soup = BeautifulSoup(page.read())
    f_in = open(sys.argv[2])
    cur_el = soup
    elem_name = f_in.readline()
    while elem_name != '':
        elem_num = int(f_in.readline())
        cur_el = cur_el.find_all(elem_name.strip())[elem_num]
        elem_name = f_in.readline()
    f_in.close()
    
    for el in cur_el.contents:
        
    print cur_el.
    

if __name__ == "__main__":
    main()
