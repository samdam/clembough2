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
    #return str(events)

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
                             location=event[1][0]['location'],
                             clink1=event[1][3][0][0], ctitle1=event[1][3][0][1], cdesc1=event[1][3][0][2],
                             clink2=event[1][3][1][0], ctitle2=event[1][3][1][1], cdesc2=event[1][3][1][2],
                             clink3=event[1][3][2][0], ctitle3=event[1][3][2][1], cdesc3=event[1][3][2][2],
                             clink4=event[1][3][3][0], ctitle4=event[1][3][3][1], cdesc4=event[1][3][3][2],
                             clink5=event[1][3][4][0], ctitle5=event[1][3][4][1], cdesc5=event[1][3][4][2],
                             plink1=event[1][3][5][0], ptitle1=event[1][3][5][1], pdesc1=event[1][3][5][2],
                             plink2=event[1][3][6][0], ptitle2=event[1][3][6][1], pdesc2=event[1][3][6][2],
                             plink3=event[1][3][7][0], ptitle3=event[1][3][7][1], pdesc3=event[1][3][7][2],
                             plink4=event[1][3][8][0], ptitle4=event[1][3][8][1], pdesc4=event[1][3][8][2],
                             plink5=event[1][3][9][0], ptitle5=event[1][3][9][1], pdesc5=event[1][3][9][2])
            eventNoStockWriter(eventDict)
        elif event[0][0] == name:
            eventDict = dict(event_title=event[0][0]+" at "+event[0][1],
                             person=event[0][0], company=event[0][1],
                             job_title=event[1][0]['headline'], 
                             industry=event[1][0]['industry'],
                             summary=event[1][0]['summary'],
                             specialties=event[1][0]['specialties'],
                             location=event[1][0]['location'],
                             clink1=event[1][3][0][0], ctitle1=event[1][3][0][1], cdesc1=event[1][3][0][2],
                             clink2=event[1][3][1][0], ctitle2=event[1][3][1][1], cdesc2=event[1][3][1][2],
                             clink3=event[1][3][2][0], ctitle3=event[1][3][2][1], cdesc3=event[1][3][2][2],
                             clink4=event[1][3][3][0], ctitle4=event[1][3][3][1], cdesc4=event[1][3][3][2],
                             clink5=event[1][3][4][0], ctitle5=event[1][3][4][1], cdesc5=event[1][3][4][2],
                             plink1=event[1][3][5][0], ptitle1=event[1][3][5][1], pdesc1=event[1][3][5][2],
                             plink2=event[1][3][6][0], ptitle2=event[1][3][6][1], pdesc2=event[1][3][6][2],
                             plink3=event[1][3][7][0], ptitle3=event[1][3][7][1], pdesc3=event[1][3][7][2],
                             plink4=event[1][3][8][0], ptitle4=event[1][3][8][1], pdesc4=event[1][3][8][2],
                             plink5=event[1][3][9][0], ptitle5=event[1][3][9][1], pdesc5=event[1][3][9][2],
                             ticker=event[1][1][1].split(':')[1],
                             previous_close=event[1][1][2].split(':')[1],
                             change=event[1][1][3].split(':')[1],
                             fifty_two_w_range=event[1][1][4].split(':')[1],
                             volume=event[1][1][5].split(':')[1],
                             market_cap=event[1][1][6].split(':')[1],
                             p_over_e=event[1][1][7].split(':')[1],
                             eps=event[1][1][8].split(':')[1],
                             dividend=event[1][1][9].split(':')[1],
                             y=event[1][1][10].split(':')[1],
                             stock_x=event[1][1][11].split(':')[1])
            eventWithStockWriter(eventDict)
            
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