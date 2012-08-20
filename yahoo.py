"""
this contains the classes for Yahoo! Finance quotes and stories, plus associated functions for obtaining them
"""

import json
import urllib2
import AlchemyAPI
from bs4 import BeautifulSoup

# Quote: contains a list of quotes and a list of stories for a given company.
class Quote:
    def __init__(self, ticker):
        self._data = []
        self._stories = []
        self.look_up(ticker)

    def __str__(self):
        string = ''
        for datum in self._data:
            string += datum + '\n'

        string += '\n News: \n'
        for i in range (5):
            string += self._stories[i].__str__() + '\n'
        return string

    # look_up: get stock quotes and stories for the company.
    # takes company ticker.
    # modifies self._data and self._stories
    def look_up(self, ticker):
        #get stock quotes
        requests = [['n','Name'],['s','Ticker'],['p','Previous Close'],['c','Change/% Change'],
                    ['w','52w Range'],['v','Volume'],['j1','Market Cap'],['r','P/E Ratio'],
                    ['e','EPS'],['d','Dividend'],['y','Yield'],['x','Stock Exchange']]
        for request in requests:
            stat = request[1] + ': '
            datum = urllib2.urlopen('http://finance.yahoo.com/d/quotes.csv?s='
                               + ticker + '&f=' + request[0]).read()
            datum = datum.rstrip('\n')
            datum = datum.replace('"', '')
            datum = stat.ljust(20) + datum
            self._data.append(datum)

        # get stories
        newsXML = urllib2.urlopen('http://finance.yahoo.com/rss/headline?s=' + ticker).read()
        newsBS = BeautifulSoup(newsXML).find_all('item')
        news = rarefyBS(newsBS)
        for item in news:
            self._stories.append(Story([item[0], item[1], item[2], item[4]]))

# Story: represents a story from Yahoo! Finance.
# contains headline, text, link, date
class Story:
    def __init__(self, elements):
        self._elements = []
        for element in elements:
            if element == None:
                self._elements.append('None')
            else:
                self._elements.append(element)

    def __str__(self):
        string = ''
        for element in self._elements:
            string += element + '\n'
        return string

# comORorg: if getTicker doesn't find a match, tell user, otherwise get quotes and stories
# takes company name.
# returns Quote class object for the company.
def comORorg(company):
    ticker = getTicker(company)
    if ticker == 'none' or not ticker.isalpha():
        return 'No info available from Yahoo! Finance.'
    else:
        return Quote(ticker)

# rarefyBS: convert a Beautiful Soup object to a list of strings.
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

    if 'symbol' in tickerSrch:
        trunc1 = tickerSrch.split('","name', 1)[0]
        trunc2 = trunc1.split('symbol":"', 1)[1]
        return trunc2
    else:
        return 'none'

def askUser():
    company = raw_input('What company? ')
    return company

def main():
    print comORorg(askUser())

if __name__ == "__main__":
    main()
