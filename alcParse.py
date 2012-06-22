"""
this file takes information retrieved from retrieve.py and uses ALchemy API
to parse the information into search terms.
"""
from bs4 import BeautifulSoup
import retrieve
import AlchemyAPI
import datetime #TODO: ask if they want the whole calendar, or just today

entityTypes = ["Person", "Orginization", "Company", "Facility"]

def makeAlcObj():
    #PRE: none
    #POST: makes an alchemy api object and loads the api key. 
    alcObj = AlchemyAPI.AlchemyAPI()
    alcObj.loadAPIKey("api_key.txt")
    return alcObj

def searchSoup(entityType, entities, bsObj, eventString, alc):
    for kind in bsObj("type"):
        if str(kind.string) == entityType:
            for sib in kind.next_siblings:
                if "text" in str(sib):
                    name = str(sib.string)
                    eventString = eventString.replace(name, '')
                    bsObj = BeautifulSoup(
                        alc.TextGetRankedNamedEntities(eventString))
                    entities.append(name)
    return (entities, eventString, bsObj)

def getCompanies(s):
    """finds the company name in the string"""
    s = s.strip('1234567890-: ')
    for word in stopwords:
        if " " + word + " " in s or s.startswith(word + ' ') or s.endswith(
            " " + word):
            s = s.replace(word, "")
    print s

stopwords = ['a','able','about','across','after','all','almost','also','am',
             'among','an','and','any','are','as','at','be','because','been',
             'but','by','can','cannot','could','dear','did','do','does',
             'either','else','ever','every','for','from','get','got','had',
             'has','have','he','her','hers','him','his','how','however','i',
             'if','in','into','is','it','its',"it\xe2\x80\x99s",'just','least',
             'let','like','likely','may','me','might','most','must','my',
             'neither','no','nor','not','of','off','often','on','only','or',
             'other','our','own','rather','said','say','says','she','should',
             'since','so','some','than','that','the','their','them','then',
             'there','these','they','this','tis','to','too','twas','us',
             'wants','was','we','were','what','when','where','which','while',
             'who','whom','why','will','with','would','yet','you','your',
             '--', '-', 'many', 'here', 'meeting', 'lunch', 'none', 'Meeting']
    
def main():
    deploy = retrieve.Retriever()
    #TODO: ask/find out if new user
    #TODO: if new user, get new AUTH
    events = deploy.getEvents()
    
    alc = makeAlcObj()

    eventStrings = []
    
    for i in range(len(events)):
        eventStrings.append("")
        for detail in events[i]:
            eventStrings[i] += str(detail) + " "

    bsList = []
    eventData = []
    for event in eventStrings:
        getCompanies(event)
    for i in range(len(eventStrings)):
        bsList.append(BeautifulSoup(
            alc.TextGetRankedNamedEntities(eventStrings[i])))
    
##        for entity in entityTypes:
##            print bsList[i].prettify()
##            eventData, eventStrings[i], bsList[i] = searchSoup(entity,
##                                                    eventData,
##                                                    bsList[i],
##                                                    eventStrings[i],
##                                                    alc)

    for datum in eventData:
        print datum
    

if __name__ == "__main__":
    main()
