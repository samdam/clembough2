"""
Saw someone do this once
"""

import oauth2 as oauth
import urlparse
from bs4 import BeautifulSoup


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

    print "Request Token:"
    print "    - oauth_token        = %s" % request_token['oauth_token']
    print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']

    #redirect to the provider
    authorize_url =      'https://api.linkedin.com/uas/oauth/authorize'
    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

    #?
    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
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
    
    url = 'http://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,headline,industry,summary,specialties,location:(name)))?first-name=' + names[0] + '&last-name=' + names[1]

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
    print contentBS
    #candidates = contentBS.find_all('person')
    #for person in candidates:
        #print person.find('first-name'), ' ', person.find('last-name')
        #id = person.find('id')
        #print id
        #print id.string
        #print person.find('http://api.linkedin.com/v1/people/id=' + id.string)



def main():
    name = raw_input('Who?      ')
    api_call(getOAuthToken(), name)

if __name__== "__main__":
    main()
