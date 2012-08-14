"""
this is the main.py from which the program will run
"""

import alcParse
import news_info
import yahoo
import linked_in
from string import Template

def srch(event, LI_acc_token):
    print event
    
    subject = linked_in.api_call(LI_acc_token, event[0])
    print subject
    
    yahoo_quote = yahoo.comORorg(event[1])
    print yahoo_quote
    
    news = news_info.NewsInfo(event[0], event[1])
    
    bing_stories = news.getStories()
    print "Articles from Bing: "
    if bing_stories == None:
        print "None found."
    else:
        if len(bing_stories) >= 5:
            for i in range(5):
                for piece in bing_stories[i]:
                    print piece
        else:
            for story in bing_stories:
                for piece in story:
                    print piece

"""    crain_stories = news.getCrainStories(subject.location.string.split()[0])
    if not crain_stories == None:
        print "Crain's stories: "
        for story in crain_stories:
            print story
    else:
        print "No Crain's stories found."
    """

def main():
    events = [("google", "http://wwww.google.com"),
              ("facebook", "http://www.facebook.com"),
              ("gizmodo", "http://www.gizmodo.com"),
              ("twitter", "http://www.twitter.com")]
    f = open("htmlpresentation.txt", "r+")
    string = f.read()
    s = Template(string)
    string = s.safe_substitute(event1=events[0][0], event1href=events[0][1],
                      event2=events[1][0], event2href=events[1][1],
                      event3=events[2][0], event3href=events[2][1],
                      event4=events[3][0], event4href=events[3][1])
    f.close()
    f = open("presentation.html", 'w')
    f.write(string)
    f.close()
##    event_data = alcParse.main()
##    LI_acc_token = linked_in.getOAuthToken()
##    for event in event_data:
##        srch(event, LI_acc_token)

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
