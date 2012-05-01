from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from application1.models import Field, Url, MultipleMatch
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from datetime import datetime
import uuid
import urllib2, sys, re, json
from bs4 import BeautifulSoup, NavigableString, Comment
import os


def multiple_match(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index_multiple_match.html', c)

def create_entry_multi(request):
    json_data = simplejson.loads(request.raw_post_data)
    url = json_data['url']
    name = json_data['name'].strip()
    fields = json_data['fields']
    print fields
    url_obj = Url(url=url, name=name, multiple_match=True)
    url_obj.save()
    for field in fields:
        match_text = field[1].split('\n')[0].replace(' ','').strip()
        field_obj = MultipleMatch(field_name=field[0].strip(),
                          match_text=match_text,
                          match_data=multi_parser(url, match_text),
                          url=url_obj,
                          field_name_ns=field[0].strip().replace(' ', ''))
        field_obj.save()
    return HttpResponse(url_obj.id)

def get_entry_multi(request, url_obj):
    fields = MultipleMatch.objects.filter(url = url_obj)
    url_link = '/static/scripts/scraper_' + url_obj.name.replace(' ', '') + '.py'
    c = {'url_obj' : url_obj, 'fields' : fields, 'id' : id, 'link' : url_link}
    return render_to_response('get_entry.html', c)

def multi_scrape(request, url, url_obj):
    multiple_match = MultipleMatch.objects.get(url=url_obj)
    path = multiple_match.match_data
    orig_text = multiple_match.match_text
    to_return = {multiple_match.field_name_ns:multi_scraper(url, path, orig_text)}
    return HttpResponse(json.dumps(to_return))

def multi_parser(url, string_to_match):
    def matches_input(tag):
        return tag.find(string_to_match) != -1
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    web_page = opener.open(url)
    soup = BeautifulSoup(web_page.read())
    clean_up_soup(soup, True)

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
    return json.dumps(path)


def multi_scraper(url, path, orig_text):
    path = json.loads(path)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    web_page = opener.open(url)
    soup = BeautifulSoup(web_page.read())
    clean_up_soup(soup, False)
    path.reverse()
    current_element = soup
    
    greatest_false = float('inf')
    best_match = []
    orig_text = orig_text.replace(' ', '')
    for i in range(len(path)):
        test_values = recursive_match(path, 0, i, current_element)
        if not isinstance(test_values, list):
            continue
        if not test_values:
            continue
        if len(test_values) > 300 or len(test_values) < 2:
            continue
        print test_values
        false_count = 0
        possible = False
        for x in test_values:
            if x == False or x is None:
                false_count += 1
                continue
            if orig_text in x.replace(' ', ''):
                possible = True
        if not possible:
            continue
        false_count = false_count * 2 - (len(test_values) * 1.0) + (len(test_values) - false_count) / (len(test_values) * 1.0)
        if false_count < greatest_false:
            best_match = test_values
            greatest_false = false_count
    print best_match
    return best_match


def recursive_match(path, i, j, current_element):
    if i == len(path) - 1:
        return current_element.string
    node = path[i]
    tag_type_elements = current_element.find_all(node[0])
    if i == j:
        return [recursive_match(path, i + 1, j, next_element) for next_element in tag_type_elements]
    else:
        if len(tag_type_elements) <= node[2]:
            
#print tag_type_elements, node[2], node[0], i, len(path)
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


def clean_up_soup(soup, is_parser):
    invalid_tags = ['a','b','i','u']
    """
    for tag in soup.find_all(True):
        if tag.name in invalid_tags:
            tag.replace_with(tag.encode_contents())
    """
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

