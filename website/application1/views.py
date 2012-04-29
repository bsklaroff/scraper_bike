from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from application1.models import Field, Url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from datetime import datetime
import uuid
import urllib2, sys, re, json
from bs4 import BeautifulSoup, NavigableString, Comment
import os

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

def home(request):
    # t = loader.get_template('postRequest.html')
    # t.render(Context({"name":"Lu"}))
    #{{{Name}}}
    if request.user.is_authenticated():
        is_authenticated = True
    else:
        is_authenticated = False

    c = {'Name':'Lu', 'is_authenticated':is_authenticated}
    c.update(csrf(request))
    #return render_to_response('postRequest.html', c)
    return render_to_response('index.html', c)
#return HttpResponse(loader.get_template('postRequest.html').render(c))
#return HttpResponse("you have come home to app1")

def createUser(request):
    jsonData = simplejson.loads(request.raw_post_data)
    username = jsonData['username'].strip()
    email = jsonData['email'].strip()
    password = jsonData['password'].strip()
    first = jsonData['first'].strip()
    last = jsonData['last'].strip()
    newUser = User(username=username, email=email, password=password, first_name=first, last_name=last)
    newUser.set_password(password)
    newUser.save()

    return HttpResponse("Yay")


def login_view(request):
    jsonData = simplejson.loads(request.raw_post_data)
    email = jsonData['email'].strip()
    password = jsonData['password'].strip()
    if email == '' or password == '':
        return HttpResponse("wrong password")
    if len(User.objects.filter(email=email)) == 1:
        username = User.objects.get(email=email).username
    else:
        return HttpResponse("wrong password")

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(user.first_name)
        else:
            return HttpResponse("no longer active")
    else:
        return HttpResponse("wrong password")

def logout_view(request):
    logout(request)
    return HttpResponse("Successfully logged out")

def test(request):
    print parser("http://sfbay.craigslist.org/sfc/bks/2943895191.html", "Books for Sale")
    return HttpResponse("success")

def create_entry(request):
    json_data = simplejson.loads(request.raw_post_data)
    url = json_data['url']
    name = json_data['name'].strip()
    fields = json_data['fields']
    print fields
    url_obj = Url(url=url, name=name)
    url_obj.save()
    write_data = '{'
    for field in fields:
        match_text = ''.join(field[1].split('\n')[0].split()).strip()
        match_data = parser(url, match_text)
        field_obj = Field(field_name=field[0].strip(),
                          match_text=match_text,
                          match_data=match_data,
                          url=url_obj,
                          field_name_ns=field[0].strip().replace(' ', ''))
        write_data += '"' + field[0].replace(' ', '') + '"' + ':' + match_data + ','
        print match_data
        field_obj.save()
    write_data = write_data[:-1] + '}'
    file_name = 'scraper_' + name.replace(' ', '') + '.py'
    os.system('cp scraper_customized.py files/static/scripts/' + file_name)
    f = open('files/static/scripts/' + file_name, 'r')
    lines = f.read().split('\n')
    f.close()
    f = open('files/static/scripts/' + file_name, 'w')
    for line in lines:
        if 'DATA = []' in line:
            f.write("DATA = '" + write_data + "'\n")
        else:
            f.write(line + '\n')
    f.close()
    return HttpResponse(url_obj.id)




def create_entry2(request):
    json_data = simplejson.loads(request.raw_post_data)
    url = json_data['url']
    name = json_data['name'].strip()
    fields = json_data['fields']
    print fields
    url_obj = Url(url=url, name=name)
    url_obj.save()
    for field in fields:
        print 'got here'
        match_text = field[1].split('\n')[0].replace(' ','').strip()
        field_obj = Field(field_name=field[0].strip(),
                          match_text=match_text,
                          match_data=parser(url, match_text),
                          url=url_obj,
                          field_name_ns=field[0].strip().replace(' ', ''))
        field_obj.save()
    return HttpResponse(url_obj.id)


def get_entry(request):
    id = request.GET['id']
    url_obj = Url.objects.get(id=id)
    fields = Field.objects.filter(url = url_obj)
    url_link = '/static/scripts/scraper_' + url_obj.name.replace(' ', '') + '.py'
    c = {'url_obj' : url_obj, 'fields' : fields, 'id' : id, 'link' : url_link}
    return render_to_response('get_entry.html', c)

def clean_up_soup(soup, is_parser):
    invalid_tags = ['a','b','i','u']
    for tag in soup.find_all(True):
        if tag.name in invalid_tags:
            tag.replace_with(tag.encode_contents())

    strings = []
    for tag in soup.strings:
        strings.append(tag)
    if is_parser:
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
    return soup

def scrape(request):
    url = request.GET['url']

    cookieprocessor = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(url)
    soup = BeautifulSoup(page.read())
    clean_up_soup(soup, False)

    id = request.GET['id']
    url_obj = Url.objects.get(id=id)
    fields = Field.objects.filter(url = url_obj)

    return_field_data = {}
    for field in list(fields):
        return_field_data[field.field_name_ns] = scraper(soup, field.match_data)

    return HttpResponse(json.dumps(return_field_data))

def parser(url, text_to_match):
    def matches_input(tag):
        return tag.find(text_to_match) != -1

    cookieprocessor = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(url)
    soup = BeautifulSoup(page.read())
    soup = clean_up_soup(soup, True)

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
    return json.dumps([path, el_id])
#f_out = open('data', 'w')
    #f_out.write(json.dumps([path, el_id]))
    #f_out.close()

def scraper(soup, match_data):
    cur_el = soup
    path, elem_id = json.loads(match_data)
    for node in path:
        print node
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
            if el.strip():
                res.append(el)
    return res[elem_id].strip()
