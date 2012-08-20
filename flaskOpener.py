"""
Utilizes flask to open html files that display the calendar info
"""
from flask import Flask, render_template
import main
from string import Template

app = Flask(__name__)

@app.route('/')
def index():
    events = main.getEvents()
    app.jinja_env.globals['events'] = events
    eventsDict = dict(event1=events[0][0][0], event1href="/"+events[0][0][0],
                      event2=events[1][0][0], event2href="/"+events[1][0][0],
                      event3=events[2][0][0], event3href="/"+events[2][0][0],
                      event4=events[3][0][0], event4href="/"+events[3][0][0],
                      event5=events[4][0][0], event5href="/"+events[4][0][0])
    menuWriter(eventsDict)
    return render_template('presentation.html')

@app.route('/<path:name>/')
def summon_person(name):
    for event in app.jinja_env.globals['events']:
        if event[0][0] == name and event[1][1] == "No info available from Yahoo! Finance.":
            eventDict = dict(event_title=event[0][0]+" at "+event[0][1],
                             person=event[0][0], company=event[0][1],
                             job_title=event[1][0]['headline'], 
                             industry=event[1][0]['industry'],
                             summary=event[1][0]['summary'],
                             specialties=event[1][0]['specialties'],
                             location=event[1][0]['location'])
            eventNoStockWriter(eventDict)
            
    return render_template('event.html')
    
def menuWriter(eventsDict):
    ## eventDict is a dict of event names (person and place) and their links
    f = open("templates/htmlpresentation.txt", "r+")
    string = f.read()
    s = Template(string)
    string = s.safe_substitute(eventsDict)
    f.close()
    f = open("templates/presentation.html", 'w')
    f.write(string)
    f.close()
    return
    

def eventWithStockWriter(eventDict):
    ## eventDict is a dict of the event info including: event_title, person,
    ## company, imgsrc, name, job_title, industry, summary, specialties,
    ## location, 5 personal links (including link, title and desc) and 5
    ## company links (including link, title, and desc) and all stock info
    f = open("templates/eventwithstocktemplate.txt", "r+")
    string = f.read()
    s = Template(string)
    string = s.safe_substitute(eventDict)
    f.close()
    f = open("templates/event.html", 'w')
    f.write(string)
    f.close()
    return


def eventNoStockWriter(eventDict):
    ## eventDict is a dict of the event info including: event_title, person,
    ## company, imgsrc, name, job_title, industry, summary, specialties,
    ## location, 5 personal links (including link, title and desc) and 5
    ## company links (including link, title, and desc)
    f = open("templates/eventtemplate.txt", "r+")
    string = f.read()
    s = Template(string)
    string = s.safe_substitute(eventDict)
    f.close()
    f = open("templates/event.html", 'w')
    f.write(string)
    f.close()
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
