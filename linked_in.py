"""
this contains the functions necessary to get a LinkedIn user's profile info
"""

import oauth2 as oauth
import urlparse
from bs4 import BeautifulSoup

# Bunch: Represents a LinkedIn profile.
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        string = ''
        if self.isEmpty == True:
            string += "No matches found on LinkedIn."
        else:
            for key in self.__dict__:
                if not (key == 'isEmpty' or key == 'positions'):
                    field = 'unavailable'
                    if not self.__dict__[key] == None:
                        field = self.__dict__[key] 
                    string += (key + ':').ljust(20) + field + '\n'
        return string

# getOAuthToken: Get user's permission to access LinkedIn. User must follow a link to get a PIN, which they give to the program.
# returns OAuth access token and token secret.
def getOAuthToken():
    # initialize the oauth client
    my_key = "qpquu715bd1y"
    my_secret = "xGmeUfgStvhJcPrf"

    consumer = oauth.Consumer(my_key, my_secret)
    client = oauth.Client(consumer)

    # get a request token
    request_token_url      = 'https://api.linkedin.com/uas/oauth/requestToken'
    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
 
    request_token = dict(urlparse.parse_qsl(content))

    # direct user to link
    print "Go to the following link in your browser, log in with your LinkedIn account and select authorize."
    print "%s?oauth_token=%s" % ('https://api.linkedin.com/uas/oauth/authorize', request_token['oauth_token'])

    # obtain PIN from user
    oauth_verifier = raw_input('What is the PIN? ')

    # get the access token
    access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
 
    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    access_token_stuff = [access_token['oauth_token'], access_token['oauth_token_secret']]
 
    return access_token_stuff

# search_LI: Search subject's name on LinkedIn. Find a match with the correct company.
# takes OAuth access token and token secret as tuple, plus subject's name and company.
# returns Bunch object containing the subject's LinkedIn info, or a blank Bunch object if no matches are found.
def search_LI(access_token_stuff, name, company):
    names = name.split()
  
    url = 'http://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,headline,industry,summary,specialties,location:(name),positions))?first-name=' + names[0] + '&last-name=' + names[1]

    consumer = oauth.Consumer(key="qpquu715bd1y", 
        secret="xGmeUfgStvhJcPrf")

    token = oauth.Token(key=access_token_stuff[0],
                        secret=access_token_stuff[1])

    client = oauth.Client(consumer, token)

    # call LinkedIn's REST api
    resp, content = client.request(url, "GET")
    contentBS = BeautifulSoup(content)

    # parse results
    peopleBS = contentBS.find_all('person')
    people = []
    for personBS in peopleBS:
        LIcompany = None
        #if not personBS.find('positions') == None:
        if len(personBS.find('positions')) > 0:
            LIcompany = BS2string(personBS.find('positions').find('position').find('company'), 'name')
        person = Bunch(first_name= BS2string(personBS, 'first-name'),
                       last_name= BS2string(personBS, 'last-name'),
                       headline= BS2string(personBS, 'headline'),
                       industry= BS2string(personBS, 'industry'),
                       summary= BS2string(personBS, 'summary'),
                       specialties= BS2string(personBS, 'specialties'),
                       location= BS2string(personBS.find('location'), 'name'),
                       company= LIcompany,
                       isEmpty= False)
        if (not person.company == None):
            if (person.company.lower() in company.lower()) or (company.lower() in person.company.lower()):
                people.append(person)
    if len(people) > 0:
        return people[0].__dict__
    else:
        return Bunch(isEmpty= True)

# BS2string: searches Beautiful Soup object for a tag and returns it as a string.
# takes a BS object and the tag to search for.
# returns desired content as a string.
def BS2string(soup, tag):
    if not soup == None:
        if soup.find(tag):
            return soup.find(tag).string
    return 'None'

def main():
    pass
    

if __name__== "__main__":
    main()
