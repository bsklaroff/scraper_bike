import urllib2, sys, re, json
from bs4 import BeautifulSoup, NavigableString, Comment

INVALID_TAGS = ['a','b','i','u']

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

def matches_input(tag):
    return tag.find(sys.argv[2]) != -1

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
    for i,tag in enumerate(strings):
        new_tag = tag.wrap(soup.new_tag('b'))
        new_tag.string.replace_with(new_tag.string.replace(' ',''))
        strings[i] = new_tag.string
        new_tag.unwrap()
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

    og_el = soup.find(text=matches_input)
    cur_el = og_el.parent

    # This finds the exact index of the element in the contents of its parent
    nav_contents = []
    for el in cur_el.contents:
        if isinstance(el, NavigableString) and not isinstance(el, Comment):
            if el.strip():
                nav_contents.append(el)
    el_id = 0
    for i,el in enumerate(nav_contents):
        if el == og_el:
            el_id = i

    # This finds the path to the parent in the document tree
    path = []
    while cur_el.name != soup.name:
        # Find the index of the element out of the elements that match its attributes
        cur_el_attrs_num = 0
        # Find the index of the element out of all possible elements
        cur_el_num = 0
        attrs_match_count = 0
        for i,el in enumerate(cur_el.parent.find_all(cur_el.name)):
            if el == cur_el:
                cur_el_num = i
                cur_el_attrs_num = attrs_match_count
            if el.attrs == cur_el.attrs:
                attrs_match_count += 1
            
        cur_el_attrs = cur_el.attrs if cur_el.attrs else {}
        cur_el_info = (cur_el.name, cur_el_attrs, cur_el_attrs_num, cur_el_num)
        path.insert(0, cur_el_info)
        cur_el = cur_el.parent

    print path
    f_out = open('data', 'w')
    f_out.write(json.dumps([path, el_id]))
    f_out.close()

if __name__ == "__main__":
    main()
