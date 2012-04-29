import urllib2, sys, re, json
from bs4 import BeautifulSoup, NavigableString, Comment

IGNORE_BREAKS = False
INVALID_TAGS = ['a','b','i','u']

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

def main():
    url = sys.argv[1]
    cookieprocessor = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(url)
    soup = BeautifulSoup(page.read())

    for tag in soup.find_all(True):
        if tag.name in INVALID_TAGS:
            tag.replace_with(tag.encode_contents())
    strings = []
    for tag in soup.strings:
        strings.append(tag)
    while len(strings) > 0:
        tag = strings[0]
        if isinstance(tag.next_element, NavigableString):
            strings.remove(tag.next_element)
            new_tag = tag.wrap(soup.new_tag('b'))
            new_tag.string.replace_with(tag + tag.next_element.extract())
            strings[0] = new_tag.string
            new_tag.unwrap()
        else:
            strings.remove(tag)

    cur_el = soup
    f_in = open(sys.argv[2])
    path, elem_id = json.loads(f_in.read())
    f_in.close()
    for node in path:
        elem_name, elem_attrs, elem_attrs_num, elem_num = node
        matching_elems = cur_el.find_all(elem_name.strip())
        # First try matching element by matching attributes
        attrs_match_count = 0
        found = False
        for i,el in enumerate(matching_elems):
            if el.attrs == elem_attrs:
                if elem_attrs_num == attrs_match_count:
                    found = True
                    cur_el = el
                    break
                attrs_match_count += 1
        # If attributes do not match, just match by children's index in parent
        if not found:
            cur_el = matching_elems[elem_num]

    res = []
    for el in cur_el.contents:
        if isinstance(el, NavigableString) and not isinstance(el, Comment):
            if el.strip() or IGNORE_BREAKS:
                res.append(el)
    if not IGNORE_BREAKS:
        print res[elem_id].strip()
    else:
        print ''.join(res).strip()

if __name__ == "__main__":
    main()
