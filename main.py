"""
this is the main.py from which the program will run
"""

import alcParse
import news_info
import yahoo
import linked_in

def srch(event, LI_acc_token):
    subject = linked_in.api_call(LI_acc_token, event[0])
    
    yahoo_quote = yahoo.comORorg(event[1])
    
    news = news_info.NewsInfo(event[0], event[1])
    
    bing_stories = news.getStories()

    ##crain_stories = news.getCrainStories(subject.location.string.split()[0])

    return [subject, yahoo_quote, news, bing_stories]

def getEvents():
    event_data = alcParse.main()
    events = []
    LI_acc_token = linked_in.getOAuthToken()
    for event in event_data:
        events.append([event, srch(event, LI_acc_token)])
    return events

def main():
    event_data = alcParse.main()
    LI_acc_token = linked_in.getOAuthToken()
    for event in event_data:
        srch(event, LI_acc_token)

if __name__ == "__main__":
    main()

"""
Fix LI oauth:
    allow immediate access for return users
    OR automate authorization
Fix display:
    separate events
    group company news stories
    grid
    templating language for html
Better news
    check for redundancy
    find more relevant to subject
    search subject
    crain's? / find similar
Better profile
    consider whole calendar
    disambiguate subject
        web search
            web +company +location
        check images?
Conquer Google
    ??
"""
