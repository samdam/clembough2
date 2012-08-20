"""
this is the main.py from which the program will run
"""

import alcParse
import news_info
import yahoo
import linked_in

# srch: appeal to various web resources for information and news stories on a given subject and their employer.
# takes event tuple containing a person's name and company, and an OAuth token for LinkedIn's api.
# returns an array of the results by source.
def srch(event, LI_acc_token):
    # Get info on the subject from LinkedIn.
    subject = linked_in.search_LI(LI_acc_token, event[0], event[1])
    
    # Get info/stories on the company from Yahoo! Finance.
    yahoo_quote = yahoo.comORorg(event[1])
    
    # Get stories on the subject/company from Bing.
    news = news_info.NewsInfo(event[0], event[1])
    bing_stories = news.getStories()

    # This would be how to call the Crain's api, but that code is unfinished.
    ##crain_stories = news.getCrainStories(subject.location.string.split()[0])

    return [subject, yahoo_quote, news, bing_stories]

# getEvents: get people/companies from the calendar and find info on them.
# returns a list of person/company tuples.
def getEvents():
    LI_acc_token = linked_in.getOAuthToken()
    events = []
    event_data = alcParse.main()
    for event in event_data:
        events.append([event, srch(event, LI_acc_token)])
    return events

def main():
    pass

if __name__ == "__main__":
    main()

"""
AREAS TO IMPROVE
Fix LI oauth
    allow immediate access for return users
    OR automate authorization
Better news
    check for redundancy
    crain's? / find similar
Better profile
    consider whole calendar
    get info from general web search
Use Google
    app-engine
    google calendar
"""
