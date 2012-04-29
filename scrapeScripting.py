def main():
    urllibDemo()
    directoryDemo()
    beautifulSoupDemo()
    osStuff()

import urllib2
#To note here:
#urllib2.urlopen(url)
#for line in webPag.read().split('\n')
def urllibDemo():
    url = "http://sectionswap.com"
    webPage = urllib2.urlopen(url)
    webPageArray = webPage.read().split("\n")
    counter = 0
    for line in webPageArray:
        if counter < 5:
            print line
        counter+=1


import os
wsj = 'wallStreetJournal'
#To note here:
#for root, dirs, files in os.walk(directory in current directory): returns queried, list of dirs, and list of files in the queried directory
# Also f = open(root + '/' +  file, 'r')
#os.walk is recursive
def directoryDemo():
    for root, dirs, files in os.walk(wsj):
        for dir in dirs:
            print dir
        for file in files:
            combined = root + '/' + file
            print root + '/' + file
            f = open(combined, 'r')
            counter = 0
            for line in f.readlines():
                if counter < 5:
                    print line
                counter += 1
            print '\n\n'
    #Another way. Lists all files and dirs in directory
    listing = os.listdir(wsj)
    oneFile = wsj + '/' + listing[1]

from bs4 import BeautifulSoup
def beautifulSoupDemo():
    #f.write(string)
    #f = open('/tmp/workfile', 'w')
    listing = os.listdir(wsj)
    html = wsj + '/' + listing[1]
    if os.path.isdir(html):
        return
    f = open(html, 'r')
    soup = BeautifulSoup(f.read())
    print soup.prettify()
    print 'Soup finished \n\n\n\n'
    print soup.title
    print soup.title.string
    print html

    #Gets the title
    for h1 in soup.find_all('h1'):
        print h1.string.replace('\n', ' ')
    print '\n\n\n'
    
    story_body = soup.find(id="article_story_body")
    #story_body = soup.find(class="article")
    print story_body.get_text()
    f.close()
#print story_body.string

#os's directory is always directory of script. cd has no effect
def osStuff():
    os.system('echo "hello world!"')

if __name__ == "__main__":
    main()
