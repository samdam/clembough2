# -*- coding: utf-8 -*-
"""
this file is a class that gets news on the company given
takes code from warmup.py in heatr
"""

import urllib2
from bs4 import BeautifulSoup

tagObj = BeautifulSoup("<b></b>").b

def makeBingQuery(subject):
    searchString = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27"
    subject = subject.replace("&", " ")
    words = subject.split()
    for i in range(len(words)):
        if i < len(words) - 1:
            searchString += (words[i] + "%20")
        else:
            searchString += (
                words[i] +
                "%27&NewsCategory=%27rt_Business%27&NewsSortBy=%27Relevance%27&$top=15&$format=Atom")
    return searchString

def makeCrainsQuery(comString, city):
    if city.lower() == "chicago":
        searchString = "http://search.chicagobusiness.com/search?q="
    elif city.lower() == "new york":
        searchString = "http://www.crainsnewyork.com/search?Category=searchresults&q="
    else:
        return None
    com = comString.split()
    for i in range(len(com)):
        if i < len(com) - 1:
            searchString += (com[i] + "+")
        else:
            searchString += com[i]

    return searchString

def makeString(someList):
    newList = []
    for i in range(len(someList)):
        newList.append([])
        for item in someList[i]:
            newList[i].append(str(item.string.encode('utf-8')))
    return newList


badCharList = [['\xe2\x84\xa2', ''], ['\xe2\x80\x9c', '"'],
               ['\xe2\x80\x9d', '"'], ['\xe2\x80\x99', "'"],
               ['\xe2\x80\x93', '-'], ['\xe2\x80\x94', '--'], ["\'", '"']]
    
def removeUTF(someList):
    for i in range(len(someList)):
        for j in range(len(someList[i])):
            for char in badCharList:
                someList[i][j] = someList[i][j].replace(char[0], char[1])
    return someList

def contains(bsObj, attr):
    for att in bsObj.attrs:
        if att == attr:
            return True
    return False

class NewsInfo:

    def __init__(self, person, company):
        """ company is a string, the name of the company we want to learn
        about """
        self._per = person
        self._com = company
        self._soup = None
        self._csoup = None
        self._info = []
        self._cinfo = []

    def getStories(self):
        print "Results for Amy Schwartz:"
        print self.query(self._per,)
        print "Results for Ideo:"
        print self.query(self._com)
        
    def query(self, subject):
        searchString = makeBingQuery(subject)
        #sets up the ability to have username and password on the site
        #this code is from http://docs.python.org/howto/urllib2.html#id6
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, searchString, "adamgwilliam@gmail.com",
                              "BK2ctdIAXy+U5wzBCQ1UxrcPY9JTBhMaL5MYG8Yx5QA=")
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        opener.open(searchString)
        urllib2.install_opener(opener)

        self._soup = BeautifulSoup(urllib2.urlopen(searchString).read())

        return self.searchSoup(['d:url', 'd:title', 'd:description'])

    def getCrainStories(self, city):
        searchString = makeCrainsQuery(self._com, city)
        if not searchString == None:
            self._csoup = BeautifulSoup(urllib2.urlopen(searchString).read())

        if city.lower == 'new york':
            return self.searchNYCrains()
        elif city.lower == 'chicago':
            return self.searchChiCrains()
        else:
            return None

    def getSoup(self):
        return self._soup

    def getCSoup(self):
        return self._csoup

    def searchSoup(self, tags):
        """ tags is a list of the tags you are searching the soup for """
        info = []
        for i in range(len(self._soup(tags[0]))):
            info.append([])
            for tag in tags:
                info[i].append(self._soup(tag)[i])
        self._info = removeUTF(makeString(info))

        return self._info

    def searchChiCrains(self):
        div = self._csoup("div")
        toRemove = []
        for d in div:
            if contains(d, unicode('class')):
                for attr in d['class']:
                    if not attr == unicode('ez-main'):
                        toRemove.append(d)
            else:
                toRemove.append(d)
        for removal in toRemove:
            if removal in div:
                div.remove(removal)
        relevantInfo = []
        for i in range(len(div)):
            relevantInfo.append([])
            for content in div[i].contents:
                if not type(content) == type(tagObj):
                    div[i].contents.remove(content)
            for item in div[i].contents:
                if contains(item, unicode("href")):
                    relevantInfo[i].append(str(item['href']))
                if not item.find("span") == None:
                    relevantInfo[i].append(str(item.find("span").string))
                if item['class'] == [unicode('ez-desc')]:
                    foo = str(item)
                    foo = foo.replace('<p class="ez-desc">', '')
                    foo = foo.replace('<b>', '')
                    foo = foo.replace('</b>', '')
                    foo = foo.replace('</p>', '')
                    relevantInfo[i].append(foo.strip())

        return relevantInfo

    def searchNYCrains(self):
        div = self._csoup("div")
        toRemove = []
        for d in div:
            if contains(d, unicode('class')):
                for attr in d['class']:
                    if not attr == unicode('search_item'):
                        toRemove.append(d)
            else:
                toRemove.append(d)
        for removal in toRemove:
            if removal in div:
                div.remove(removal)
        relevantInfo = []
        for i in range(len(div)):
            relevantInfo.append([])
            for content in div[i].contents:
                if not type(content) == type(tagObj):
                    div[i].contents.remove(content)
            for item in div[i].contents:
                if item.name == "h3":
                    item = item.contents[0]
                if contains(item, unicode("href")):
                    relevantInfo[i].append(str(item['href']))
                    relevantInfo[i].append(str(item.string))
                if item.name == "p":
                    relevantInfo[i].append(str(item.string))

        return relevantInfo

def main():
    news = NewsInfo("Amy Schwartz", "Ideo")
    news.getStories()
    #news.getCrainStories('new york')

if __name__ == "__main__":
    main()
