"""
This program retrieves information from 30Boxes and formats it for our use. 
"""

import urllib2
import datetime
from bs4 import BeautifulSoup

API_KEY = "8416207-a37caedee730d39c3677d808ee478806"


def makeDate(uni):
    """ uni is a unicode string represetning a date and time, this function turns it into a datetime object"""
    dateandtime = str(uni).split()
    date = dateandtime[0].split("-")
    time = dateandtime[1].split(":")
    for i in range(3):
        date[i] = int(date[i])
        time[i] = int(time[i])
    when = datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2])
    return when   

class Retriever:

    AUTH = "8416207-6e8d246b24a6c74c173156105fee6be8"

    isNewUser = False

    def __init__(self):
        self._events = []
        self.makeUrl()

    def makeUrl(self):
        if self.AUTH != None:
            self._url = "http://30boxes.com/api/api.php?method=events.Get&apiKey=" + API_KEY + "&authorizedUserToken=" + self.AUTH

    def newUser(self):
        self.isNewUser = True
    
    def authorize(self):
        """ this function gets an authorization url and directs the user to open it and retrieve the authorization key.
        there is for sure a better way to do this. TODO """
        self._url = "http://30boxes.com/api/api.php?method=user.Authorize&apiKey=" + API_KEY + \
            "&applicationName=Clembough&applicationLogoUrl=http%3A%2F%2Fbit.ly%2FLIqYrc"
        print "Please go to " + self._url
        self.AUTH = raw_input("What is the key? ")

    def activate(self):
        eventSoup = BeautifulSoup(urllib2.urlopen(self._url).read())
        summaries = eventSoup("summary")
        notes = eventSoup("notes")
        date = eventSoup("start")
        for i in range(len(summaries)):
            self._events.append((str(summaries[i].string), str(notes[i].string), makeDate(date[i].string)))

    def getEvents(self):
        if self.AUTH == None or self.isNewUser == True:
            self.authorize()
        self.activate()
        return self._events
        
def main():
    get = Retriever()
    print get.getEvents()
	
if __name__ == "__main__":
	main()
