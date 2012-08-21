"""
Utilizes flask to open html files that display the calendar info
"""
from flask import Flask, render_template
import main
from string import Template

app = Flask(__name__)

@app.route('/')
def index(): #first step, shows the first 5 meetings etc on calendar
    events = main.getEvents() #gets the events
    app.jinja_env.globals['events'] = events #sets is as a global variable for second step
    eventsDict = dict()
    length = len(events)
    if length > 5:
        length = 5
    for i in range(length):
        print i
        eventsDict['event' + str(i+1)] = events[i][0][0]
        eventsDict['event' + str(i+1) + 'href'] = "/person=" + events[i][0][0]
        # ^ creates dict for replacing variables in the html menu
    menuWriter(eventsDict) #make menu
    return render_template('presentation.html') #render menu

@app.route('/<path:name>/')
def summon_person(name): #makes the data sheet about an event
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 ) #used to remove unrecognized unicode chars
    for event in app.jinja_env.globals['events']:
        #first checks that its the correct event and if it has stock data
        if 'person=' + event[0][0] == name and event[1][1] == "No info available from Yahoo! Finance." and event[1][0] != "No matches found on LinkedIn.":
            #if not, makes a dictionary from the event data
            eventDict = dict(event_title=(event[0][0]+" at "+event[0][1]).translate(trans_table),
                             person=event[0][0].translate(trans_table), company=event[0][1].translate(trans_table),
                             job_title=str(event[1][0]['headline']).translate(trans_table), 
                             industry=str(event[1][0]['industry']).translate(trans_table),
                             summary=str(event[1][0]['summary']).translate(trans_table),
                             specialties=str(event[1][0]['specialties']).translate(trans_table),
                             location=str(event[1][0]['location']).translate(trans_table))
            length = len(event[1][3])
            length2 = -1
            if length > 5:
                length2 = length - 5
            for i in range(length):
                eventDict['clink' + str(i+1)] = event[1][3][i][0]
                eventDict['ctitle' + str(i+1)] = event[1][3][i][1]
                eventDict['cdesc' + str(i+1)] = event[1][3][i][2]
            if length2 > 0:
                for i in range(length2):
                    eventDict['plink' + str(i+1)] = event[1][3][i+5][0]
                    eventDict['ptitle' + str(i+1)] = event[1][3][i+5][1]
                    eventDict['pdesc' + str(i+1)] = event[1][3][i+5][2]
            eventNoStockWriter(eventDict) #writes the html
        elif 'person=' + event[0][0] == name and event[1][0] != "No matches found on LinkedIn.": #if it does have stock data
            #writes the dict for the html page with stock data
            print 'person=' + event[0][0] == name
            print event[1][0] == "No matches found on LinkedIn."
            eventDict = dict(event_title=(event[0][0]+" at "+event[0][1]).translate(trans_table),
                             person=event[0][0].translate(trans_table), company=event[0][1].translate(trans_table),
                             job_title=str(event[1][0]['headline']).translate(trans_table), 
                             industry=str(event[1][0]['industry']).translate(trans_table),
                             summary=str(event[1][0]['summary']).translate(trans_table),
                             specialties=str(event[1][0]['specialties']).translate(trans_table),
                             location=str(event[1][0]['location']).translate(trans_table),
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
            length = len(event[1][3])
            length2 = -1
            if length > 5:
                length2 = length - 5
            for i in range(length):
                eventDict['clink' + str(i+1)] = event[1][3][i][0]
                eventDict['ctitle' + str(i+1)] = event[1][3][i][1]
                eventDict['cdesc' + str(i+1)] = event[1][3][i][2]
            if length2 > 0:
                for i in range(length2):
                    eventDict['plink' + str(i+1)] = event[1][3][i+5][0]
                    eventDict['ptitle' + str(i+1)] = event[1][3][i+5][1]
                    eventDict['pdesc' + str(i+1)] = event[1][3][i+5][2]
            eventWithStockWriter(eventDict) #write html page
        elif event[1][0] == "No matches found on LinkedIn.":
            eventDict = dict(event_title=(event[0][0]+" at "+event[0][1]).translate(trans_table),
                             person=event[0][0].translate(trans_table), company=event[0][1].translate(trans_table))
            length = len(event[1][3])
            length2 = -1
            if length > 5:
                length2 = length - 5
            for i in range(length):
                eventDict['clink' + str(i+1)] = event[1][3][i][0]
                eventDict['ctitle' + str(i+1)] = event[1][3][i][1]
                eventDict['cdesc' + str(i+1)] = event[1][3][i][2]
            if length2 > 0:
                for i in range(length2):
                    eventDict['plink' + str(i+1)] = event[1][3][i+5][0]
                    eventDict['ptitle' + str(i+1)] = event[1][3][i+5][1]
                    eventDict['pdesc' + str(i+1)] = event[1][3][i+5][2]
            eventNoStockWriter(eventDict) #writes the html
            
    return render_template('event.html') #render the html page
    
def menuWriter(eventsDict):
    ## eventDict is a dict of event names (person and place) and their links
    ## writes the html menu page based on a the template htmlprsentation.txt
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
    ## writes the html data sheet for events with stock data
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
    ## writes the html data sheet for events without stock data. 
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
    app.run(host='0.0.0.0', port=5000, debug=True) #run on 23.23.237.182:5000