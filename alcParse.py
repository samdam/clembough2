"""
this file takes information retrieved from retrieve.py and uses ALchemy API
to parse the information into search terms.
"""
from bs4 import BeautifulSoup
import retrieve
import AlchemyAPI
import datetime

entityTypes = ["Person", "Orginization", "Company", "Facility"]

def makeAlcObj():
    #PRE: none
    #POST: makes an alchemy api object and loads the api key. 
    alcObj = AlchemyAPI.AlchemyAPI()
    alcObj.loadAPIKey("api_key.txt")
    return alcObj

def searchSoup(entities, bsObj, eventString, alc):
    name = None
    for kind in bsObj("type"):
        if str(kind.string) == "Person":
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
    s = s.strip('1234567890-: ,.')
    for word in stopwords:
        if " " + word + " " in s or s.startswith(word + ' ') or s.endswith(
            " " + word):
            s = s.replace(word, "")
    s = s.strip('1234567890-: ,.')
    return s

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
             '--', '-', 'many', 'here', 'meeting', 'lunch', 'none', 'Meeting',
             "None", "Lunch", "blah", "notes"]

yes = ["Yes", "yes", "y", "Y"]
no = ["No", "no", "n", "N"]

def getResponse(message):
    response = raw_input(message).strip()
    if response in yes:
        return True
    elif response in no:
        return False
    else:
        print "Please answer yes or no"
        return getResponse(message)
    
def main():
    deploy = retrieve.Retriever()
    response = getResponse("Hello, I'm Clembough2! Are you a new user? (y/n) ")
    if response:
        deploy.authorize()
    response = getResponse(
        "Would you like me to look at your whole calendar? (y/n) ")
    if not response:
        events = deploy.getEvents(datetime.date.today())
    else:
        events = deploy.getEvents()
    
    alc = makeAlcObj()

    eventStrings = []
    
    for i in range(len(events)):
        eventStrings.append("")
        for detail in events[i]:
            eventStrings[i] += str(detail) + " "

    bsList = []
    eventData = []
    for i in range(len(eventStrings)):
        bsList.append(BeautifulSoup(
            alc.TextGetRankedNamedEntities(eventStrings[i])))
        name, eventStrings[i], bsList[i] = searchSoup(eventData, bsList[i],
                                                           eventStrings[i], alc)
        
##    for event in eventData:
##        print event
##    print "\n"
##    for event in eventStrings:
##        print event

    for i in range(len(eventStrings)):
        eventData[i] = (eventData[i], getCompanies(eventStrings[i]))

    for datum in eventData:
        print datum

    return eventData
    

if __name__ == "__main__":
    main()
