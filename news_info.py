"""
this file is a class that gets news on the company given
takes code from warmup.py in heatr
"""

import urllib2
from bs4 import BeautifulSoup

def makeQuery(company):
    searchString = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27"
    company = company.replace("&", " ")
    words = company.split()
    for i in range(len(words)):
        if i < len(words) - 1:
            searchString += (words[i] + "%20")
        else:
            searchString += (
                words[i] +
                "%27&NewsCategory=%27rt_Business%27&NewsSortBy=%27Relevance%27&$top=15&$format=Atom")
    return searchString

def makeCrainsQuery(comString):
    searchString = "http://search.chicagobusiness.com/search?q="
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

class NewsInfo:

    def __init__(self, company):
        """ company is a string, the name of the company we want to learn
        about """
        self._com = company
        self._soup = None
        self._csoup = None
        self._info = []
        self._cinfo = []
        
    def getStories(self):
        searchString = makeQuery(self._com)
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

    def getCrainStories(self):
        searchString = makeCrainsQuery(self._com)
        self._csoup = BeautifulSoup(urllib2.urlopen(searchString).read())

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

    def searchCSoup(self):
       tags = ["span", "p"]
       info = self._csoup("span")
       for span in info:
           if not span['class'] == unicode("ez-link-span"):
               info.remove(span)
            

def main():
    news = NewsInfo("Ideo")
    news.getCrainStories()
    print news.searchCSoup()
##    news.getStories()
##    info = news.searchSoup(["d:title", "d:description", "d:url"])
##    for item in info:
##        print item

if __name__ == "__main__":
    main()
