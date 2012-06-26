"""
this file
"""

import json
import urllib2
import AlchemyAPI
from bs4 import BeautifulSoup


#find quotes and news stories about a company
def yahoo(company):
    ticker = getTicker(company)
    if ticker == 'none':
        print 'No info about that company from yahoo finance.'
    else:
        printNews(ticker)

        quotes = urllib2.urlopen('http://finance.yahoo.com/d/quotes.csv?s='
                           + ticker + '&f=nscvx').read()
        printQuotes(ticker)

def printNews(ticker):
    newsXML = urllib2.urlopen('http://finance.yahoo.com/rss/headline?s='
                           + ticker).read()
    newsBS = BeautifulSoup(newsXML).find_all('item')
    news = rarefyBS(newsBS)
    for story in news:
        for element in story:
            print element
        print '\n'

def printQuotes(ticker):
    requests = [['n','Name'],['s','Ticker'],['p','Previous Close'],['c','Change/% Change'],
                ['w','52w Range'],['v','Volume'],['j1','Market Cap'],['r','P/E Ratio'],
                ['e','EPS'],['d','Dividend'],['y','Yield'],['x','Stock Exchange']]
    for request in requests:
        quote = urllib2.urlopen('http://finance.yahoo.com/d/quotes.csv?s='
                           + ticker + '&f=' + request[0]).read()
        quote = quote.rstrip('\n')
        quote = quote.replace('"', '')
        datum = request[1] + ': '
        print datum.ljust(20), quote

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
        t = s.replace(char[0], char[1])
    return t

#obtain ticker from company name
def getTicker(company):
    companyURL = company.replace(' ', '%20')
    tickerSrch = urllib2.urlopen(
        'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' + companyURL
        + '&callback=YAHOO.Finance.SymbolSuggest.ssCallback').read()
    #print tickerSrch
    
    if 'symbol' in tickerSrch:
        trunc1 = tickerSrch.split('","name', 1)[0]
        #print trunc1
        trunc2 = trunc1.split('symbol":"', 1)[1]
        #print trunc2
        return trunc2
    else:
        return 'none'

def main():
    yahoo('yahoo')
    #getTicker("yahoo")


if __name__ == "__main__":
    main()
