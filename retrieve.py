"""
This program retrieves information from 30Boxes and formats it for our use. 
"""

import urllib2
#from bs4 import BeautifulSoup

API_KEY = "8416207-a37caedee730d39c3677d808ee478806"

def main():
        token = urllib2.urlopen("http://30boxes.com/api/api.php?method=user.Authorize"
                               + "&apiKey=" + API_KEY
                               + "&applicationName=clembough"
                               + "&applicationLogoUrl=http%3A%2F%2Fchicago.racked.com%2Fuploads%2Fbaby%20Clembough.png")
        print token.read()
	
if __name__ == "__main__":
	main()
