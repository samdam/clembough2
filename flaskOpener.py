"""
Utilizes flask to open html files that display the calendar info
"""
from flask import Flask, render_template
import main
from string import Template

app = Flask(__name__)

@app.route('/')
def index():
    stuff = main.getEvents()
    redirect(stuff[0])
    events = main.getEventsPart2(stuff)
    
    return events
##    menuWriter(eventsDict)
##    return render_template('presentation.html')
##
##@app.route('/<path:url>/')
##def get_url(url):
##    if not url.startswith('http://'):
##        url = 'http://' + url
##    urls = turn_on_heat(url)
##    create_template(urls)
##    return render_template('printer.html')
##
##def create_template(urls):
##    htmlDoc = '<!DOCTYPE html> <html> <body> <h1>Try some of these!</h1> <p>'
##    for url in urls:
##        htmlDoc = htmlDoc + ' <a href="' + url[0] + '" target="_blank">' + url[1] + \
##                  '<a> <br /> <p> ' + url[2] + '</p>'
##    htmlDoc += '</p> </body> </html>'
##    filename = "templates/printer.html"
##    f = open(filename, 'w')
##    f.write(htmlDoc)
##    f.close()
##    return
##
##def turn_on_heat(url):
##    heater = WarmUp(url)
##    answer = heater.process()
##    return answer

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
