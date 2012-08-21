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
        eventsDict['event' + str(i)] = events[i][0][1]
        eventsDict['event' + str(i) + 'href'] = "/" + events[i][0][0]
        # ^ creates dict for replacing variables in the html menu
    menuWriter(eventsDict) #make menu
    return render_template('presentation.html') #render menu

@app.route('/<path:name>/')
def summon_person(name): #makes the data sheet about an event
    trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 ) #used to remove unrecognized unicode chars
    for event in app.jinja_env.globals['events']:
        #first checks that its the correct event and if it has stock data
        if event[0][0] == name and event[1][1] == "No info available from Yahoo! Finance." and event[1][0] != None:
            #if not, makes a dictionary from the event data
            eventDict = dict(event_title=(event[0][0]+" at "+event[0][1]).translate(trans_table),
                             person=event[0][0].translate(trans_table), company=event[0][1].translate(trans_table),
                             job_title=str(event[1][0]['headline']).translate(trans_table), 
                             industry=str(event[1][0]['industry']).translate(trans_table),
                             summary=str(event[1][0]['summary']).translate(trans_table),
                             specialties=str(event[1][0]['specialties']).translate(trans_table),
                             location=str(event[1][0]['location']).translate(trans_table),
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
            eventNoStockWriter(eventDict) #writes the html
        elif event[0][0] == name and event[1][0] != None: #if it does have stock data
            #writes the dict for the html page with stock data
            eventDict = dict(event_title=(event[0][0]+" at "+event[0][1]).translate(trans_table),
                             person=event[0][0].translate(trans_table), company=event[0][1].translate(trans_table),
                             job_title=str(event[1][0]['headline']).translate(trans_table), 
                             industry=str(event[1][0]['industry']).translate(trans_table),
                             summary=str(event[1][0]['summary']).translate(trans_table),
                             specialties=str(event[1][0]['specialties']).translate(trans_table),
                             location=str(event[1][0]['location']).translate(trans_table),
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
            eventWithStockWriter(eventDict) #write html page
        else: 
            return "No Linked In Data"
            
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