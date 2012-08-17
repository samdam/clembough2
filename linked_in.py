"""
Saw someone do this once
"""

import oauth2 as oauth
import urlparse
from bs4 import BeautifulSoup

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __str__(self):
        string = ''
        if self.isEmpty == True:
            string += "No matches found on LinkedIn."
        else:
            for key in self.__dict__:
                if not key == 'isEmpty':
                    string += (key + ':').ljust(20) + self.__dict__[key] + '\n'
        return string

def getOAuthToken():
    #initialize the oauth client
    my_key = "qpquu715bd1y"
    my_secret = "xGmeUfgStvhJcPrf"

    consumer = oauth.Consumer(my_key, my_secret)
    client = oauth.Client(consumer)

    #get a request token
    request_token_url      = 'https://api.linkedin.com/uas/oauth/requestToken'
    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
 
    request_token = dict(urlparse.parse_qsl(content))

    #redirect to the provider
    print "Go to the following link in your browser, log in with your LinkedIn account and select authorize. If you do not have an account, use this one:"
    print "%s?oauth_token=%s" % ('https://api.linkedin.com/uas/oauth/authorize', request_token['oauth_token'])
    #?
    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    oauth_verifier = raw_input('What is the PIN? ')

    #get the access token
    access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
 
    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    access_token_stuff = [access_token['oauth_token'], access_token['oauth_token_secret']]
 
    print "Access Token:"
    print "    - oauth_token        = %s" % access_token_stuff[0]
    print "    - oauth_token_secret = %s" % access_token_stuff[1]
    print
    print "You may now access protected resources using the access tokens above."

    return access_token_stuff


def api_call(access_token_stuff, name):
    names = name.split()
    
    url = 'http://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,headline,industry,summary,specialties,location:(name)))?first-name='+ names[0] + '&last-name=' + names[1]

    # Create your consumer with the proper key/secret.
    consumer = oauth.Consumer(key="qpquu715bd1y", 
        secret="xGmeUfgStvhJcPrf")

    #request_token_url = "https://api.linkedin.com/uas/oauth/requestToken"
    token = oauth.Token(key=access_token_stuff[0],
                        secret=access_token_stuff[1])

    # Create our client.
    client = oauth.Client(consumer, token)

    # The OAuth Client request works just like httplib2 for the most part.
    resp, content = client.request(url, "GET")
    contentBS = BeautifulSoup(content)
    
    peopleBS = contentBS.find_all('person')
    
    people = []
    for personBS in peopleBS:
        person = Bunch(first_name= BS2string(personBS, 'first-name'),
                       last_name= BS2string(personBS, 'last-name'),
                       headline= BS2string(personBS, 'headline'),
                       industry= BS2string(personBS, 'industry'),
                       summary= BS2string(personBS, 'summary'),
                       specialties= BS2string(personBS, 'specialties'),
                       location= BS2string(personBS.find('location'), 'name'),
                       isEmpty= False)
        people.append(person)

    if len(people) > 0:
        return people
    else:
        return Bunch(isEmpty= True)

def disambiguate(people):
    pass

def BS2string(soup, tag):
    if soup.find(tag):
        return soup.find(tag).string
    return 'None'

def main():
    access_token = getOAuthToken()
    while (True):
        name = raw_input('Who?      ')
        if (name == 'done'):
            break
        peeps = api_call(access_token, name)
        for person in peeps:
            print person

if __name__== "__main__":
    main()
