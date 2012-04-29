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

def createEntry(request):
    print parser("http://sfbay.craigslist.org/sfc/bks/2943895191.html", "Books for Sale! - $1 (north beach / telegraph hill)")
    return HttpResponse("success")
                 

def createEntryActual(request):
    json_data = simplejson.loads(request.raw_post_data)
    url = json_data['url']
    name = json_data['name']
    fields = json_data['fields']
    url_obj = Url(url=url, name=name)
    url_obj.save()
    for field in fields:
        field_obj = Field(field_name=field[0], match_text=field[1], match_data="hello", url=url_obj)
        print parser(url, field[1])
        field_obj.save()
    return HttpResponse("success")
    



def parser(url, text_to_match):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(url)
    soup = BeautifulSoup(page.read())

    og_el = soup.find(text=re.compile(text_to_match))
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





def scraper(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = opener.open(url)
    soup = BeautifulSoup(page.read())

    cur_el = soup
    f_in = open(sys.argv[2])
    path, elem_id = json.loads(f_in.read())
    f_in.close()
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
    print res[elem_id].strip()
