"""
this file
"""

import urllib2
import AlchemyAPI
from bs4 import BeautifulSoup

def alchemy():
    pass

#find quotes and news stories about a company
def yahoo(company):
    #ticker = getTicker(company)
    ticker = 'yhoo'
    newsXML = urllib2.urlopen('http://finance.yahoo.com/rss/headline?s='
                           + ticker).read()
    newsBS = BeautifulSoup(newsXML).find_all('item')
    news = rarefyBS(newsBS)
    #printNews(news)

    quotesXML = urllib2.urlopen('http://finance.yahoo.com/rss/quote?s='
                           + ticker).read()
    print quotesXML
    #newsBS = BeautifulSoup(newsXML).find_all('item')
    #news = rarefyBS(newsBS)
    #printNews(news)

def printNews(news):
    for story in news:
        for element in story:
            print element
        print '\n'

#remove tags from a BS.find() list
def rarefyBS(BSlist):
    info = []
    
    for item in BSlist:
        elements = []
        for element in item:
            elements.append(getString(element.string))
        info.append(elements)
                
    return info 

def getString(s):
    #PRE: s is a naviagableString
    #POST: returns the string alone of s
    s = unicode(s).encode('utf-8')    
    s = str(s)
    s = cleanse(s)
    return s

def cleanse(s):
    #PRE: s is a unicode string encoded to utf-8
    #POST: returns the string without and unicode characters.
    unreadableChars = [["\xC2\xAB", '"'], ["\xC2\xBB", '"'],
                       ["\xE2\x80\x98", "'"], ["\xE2\x80\x99", "'"],
                       ["\xE2\x80\x9A", "'"], ["\xE2\x80\x9B", "'"],
                       ["\xE2\x80\x9C", '"'], ["\xE2\x80\x9D", '"'],
                       ["\xE2\x80\x9E", '"'], ["\xE2\x80\x9F", '"'],
                       ["\xE2\x80\xB9", "'"], ["\xE2\x80\xBA", "'"],
                       ["\xe2\x80\x93", "-"], ["\xc2\x80\x99S", ""]]
    for char in unreadableChars:
        s.replace(char[0], char[1])
    return s 

#obtain ticker from company name
def getTicker(company):
    tickerSrch = urllib2.urlopen(
        'http://d.yimg.com/autoc.finance.yahoo.com/autoc?' + company +
        '=yahoo&callback=YAHOO.Finance.SymbolSuggest.ssCallback').read()
    print tickerSrch
    return 'yhoo'

def main():
    yahoo('yahoo')
    #getTicker('google')


if __name__ == "__main__":
    main()
