# -*- coding: utf-8 -*-
"""
this file is a class that gets news on the company given
takes code from warmup.py in heatr
"""

import urllib2
from bs4 import BeautifulSoup

tagObj = BeautifulSoup("<b></b>").b #used to find tag object type

def makeBingQuery(subject, params):
    #PRE: subject is the thing we want to search, params is the way we want to search it
    # Params must be a string either "News" or "Web"
    #POST: returns a string representing a url which is the bing search api
    searchString = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/" + params + "?Query=%27%22"
    subject = subject.replace("&", " ")
    words = subject.split()
    for i in range(len(words)):
        if i < len(words) - 1:
            searchString += (words[i] + "%20")
        else:
            searchString += (
                words[i] +
                "%22%27&$top=15&$format=Atom")
    return searchString

def makeCrainsQuery(comString, city):
    #PRE: comString is the company name, city is the city they are located in
    #POST: decides which city to look for (chicago or new york) and returns the 
    # string representing the url for the page we wish to search, crains chicago
    # or crains new york. this was not implimented in the final copy. useful tho.
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
    #PRE: someList is a list of non string objects
    #POST: returns the objects as strings
    newList = []
    for i in range(len(someList)):
        newList.append([])
        for item in someList[i]:
            newList[i].append(str(item.string.encode('utf-8')))
    return newList

# used in an attmept to remove unicode characters that it does not recognize. 
badCharList = [['\xe2\x84\xa2', ''], ['\xe2\x80\x9c', '"'],
               ['\xe2\x80\x9d', '"'], ['\xe2\x80\x99', "'"],
               ['\xe2\x80\x93', '-'], ['\xe2\x80\x94', '--'], ["\'", '"']]
#used with above to remove unrecognized unicode chars    
def removeUTF(someList):
    for i in range(len(someList)):
        for j in range(len(someList[i])):
            for char in badCharList:
                someList[i][j] = someList[i][j].replace(char[0], char[1])
    return someList

def contains(bsObj, attr): 
    #PRE: bsObj is a beutiful soup Object, attr are attributes in an html tag
    #POST: returns true if attr is in the attributes for the BSOBJ, false otherwise
    for att in bsObj.attrs:
        if att == attr:
            return True
    return False

class NewsInfo:
    #This class is used to find news stories about a company and or a person. 

    def __init__(self, person, company):
        """ company is a string, the name of the company we want to learn
        about """
        self._per = person #the name of the person
        self._com = company #name of the company
        self._soup = None #bs for bing news
        self._csoup = None #bs for crains
        self._info = [] #bing news stories
        self._cinfo = [] #crains stories

    def getStories(self):
        #This gets news stroes about the company, and news and web stories about 
        #the person and the company. it gets 5 of each.
        stories = []
        count = 0
        for item in self.query(self._com, "News"):
            if count < 5:
                stories.append(item)
                count += 1
        count = 0
        for item in self.query(self._per + " " + self._com, "News"):
            if count < 5:
                stories.append(item)
                count += 1
        count = 0
        for item in self.query(self._per + " " + self._com, "Web"):
            if count < 5:
                stories.append(item)
                count += 1
        return stories
        
    def query(self, subject, params):
        #this actually queries bing. makes a searchstring out of subject and
        #an params. 
        searchString = makeBingQuery(subject, params)
        #sets up the ability to have username and password on the site
        #this code is from http://docs.python.org/howto/urllib2.html#id6
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, searchString, "adamgwilliam@gmail.com",
                              "BK2ctdIAXy+U5wzBCQ1UxrcPY9JTBhMaL5MYG8Yx5QA=")
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        opener.open(searchString)
        urllib2.install_opener(opener)
        
        #makes a bs obj out of the url opened by the searchstring. 
        self._soup = BeautifulSoup(urllib2.urlopen(searchString).read())

        #returns the url, title, and description of each story returned. 
        return self.searchSoup(['d:url', 'd:title', 'd:description'])

    def getCrainStories(self, city):
        #checks the city and then makes a search based on which city is used. 
        searchString = makeCrainsQuery(self._com, city)
        if not searchString == None: 
            self._csoup = BeautifulSoup(urllib2.urlopen(searchString).read()) #opens the page
        if city.lower == 'new york': #if ny
            return self.searchNYCrains() #search ny
        elif city.lower == 'chicago': #if chicago
            return self.searchChiCrains() #search chicago
        else:
            return []

    def getSoup(self):
        return self._soup

    def getCSoup(self):
        return self._csoup

    def searchSoup(self, tags):
        """ tags is a list of the tags you are searching the soup for """
        # searchs through the beautiful soup for the tags
        info = []
        for i in range(len(self._soup(tags[0]))):
            info.append([])
            for tag in tags:
                info[i].append(self._soup(tag)[i])
        self._info = removeUTF(makeString(info))

        return self._info

    def searchChiCrains(self):
        #searches through chicago crains soup. 
        div = self._csoup("div") #id's stories by div
        toRemove = []
        for d in div:
            if contains(d, unicode('class')): #makes sure they are the correct tags
                for attr in d['class']:
                    if not attr == unicode('ez-main'):
                        toRemove.append(d) #otherwise remove them
            else:
                toRemove.append(d)
        for removal in toRemove: #remove them from div
            if removal in div:
                div.remove(removal)
        relevantInfo = []
        for i in range(len(div)): #search through div
            relevantInfo.append([])
            for content in div[i].contents: #search through the contents of each story
                if not type(content) == type(tagObj): #remove useless content
                    div[i].contents.remove(content)
            for item in div[i].contents: #check each story that remains
                if contains(item, unicode("href")):
                    relevantInfo[i].append(str(item['href'])) #find the url
                if not item.find("span") == None:
                    relevantInfo[i].append(str(item.find("span").string)) #find the story
                if item['class'] == [unicode('ez-desc')]: #find the desc
                    foo = str(item) #changes it to a string 
                    foo = foo.replace('<p class="ez-desc">', '')#remove html chars
                    foo = foo.replace('<b>', '')
                    foo = foo.replace('</b>', '')
                    foo = foo.replace('</p>', '')
                    relevantInfo[i].append(foo.strip()) #take the remaining story

        return relevantInfo #return stories. 

    def searchNYCrains(self):
        #similar process to above, but slightly different for the different 
        #formatting on NY crains website
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
    #used to test process. 
    news = NewsInfo("Amy Schwartz", "Ideo")
    stories = news.getStories()
    for story in stories:
        print story
    for story in news.getCrainStories('chicago'):
        print story

if __name__ == "__main__":
    main()
