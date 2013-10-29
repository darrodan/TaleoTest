import os
import sys
from flask import Flask, render_template, make_response
from flask import request
from flask import Response
from time import clock, time
from werkzeug.useragents import UserAgent

import logging
import urlparse
import json
import datetime as dt
import requests

file_handler = logging.FileHandler('./app.log')
USE_X_FORWARDED_HOST = True

app = Flask(__name__)
debug = False

kinveyBaseURL = 'https://baas.kinvey.com'
kinveyAppKey = 'kid_PPxAbHjIxJ'
kinveyAppSecret = '9ac1e39ec57a443e98950b9af6c18c86'
kinveyUsername = 'nymblenec'
kinveyPassword = 'pwd4nymble'
kinveyInitialized = False
whitelistCache = []
debugSwitch = False
domainOverride = False

#
# General logging method for NEC
# 
def neclogger(sMsg,debugMode,debugStatement):
    
    if not debugStatement:
            print sMsg
            sys.stdout.flush()
            return
    if debugMode:
        s = "CHQ DEBUG: " + str(sMsg)
        sys.stdout.flush()
        print s
    return

@app.route('/')
def home_url():
    # print 'Hit on default url'
    # print  request.url
    
 
    taleo_data = 'Taleo Test'
    neclogger(request.query_string, True, True)

    
    return render_template('home.html', taleo_data=request.query_string)

    d = os.environ.get('DEBUG', False)
    print d
    if d:
        print request.query_string
        print debug
        print domainOverride
        
    
    data = 'Nymble NEC'
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    
    return resp

@app.route('/taleotest')
def taleo_test():   
 
    taleo_data = 'Taleo Test'
    neclogger(request.query_string, True, True)

    print "make_response..."
    resp = make_response(render_template('home.html', taleo_data=request.query_string),200)
    print "after make_response"
    resp.headers['X-Frame-Options'] = 'ALLOW'
    return resp


    # return render_template('home.html', taleo_data=request.query_string)

    # d = os.environ.get('DEBUG', False)
    # print d
    # if d:
    #    print request.query_string
    #    print debug
    #    print domainOverride
        
    
    # data = 'Nymble NEC'
    # js = json.dumps(data)
    # resp = Response(js, status=200, mimetype='application/json')
    
    # return resp


@app.route('/favicon.ico')
def favicon():
    
    _here = os.path.dirname(__file__)
    _icon = open(os.path.join(_here, 'static', 'favicon.ico')).read()    
    data = _icon
    resp = Response(data, content_type='image/x-icon', status=200)
    
    return resp

#
# authorization URL for blitz.io to hit NEC for load testing
#
@app.route('/mu-2cc5c638-f7c471ad-be42f5c0-991d1532')
def blitz_url():
    data = 42
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    
    return resp    

#
# Taleo Test App
#
@app.route('/a/taleo')
def a_taleo():
    
    # get the query string        
    qsdata= request.query_string
    qs = urlparse.parse_qs(qsdata)
    # write log entry
    neclogger(qsdata,True, True)

    data = qsdata
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    
    return resp
   
        
#
# Main method for logging NEC entries
#
@app.route('/a/neclog')
def a_nec_log():
    
    # timer code 
    if debug == True:
        start = time()       
    
    domainMatch = None

    global kinveyInitialized
    global whitelistCache

    # check whitelist if not already initialized
    
    if not kinveyInitialized:
        kinveyURL = kinveyBaseURL + '/appdata/' + kinveyAppKey +  '/' +'whitelist/'
        #app.logger.info(kinveyURL)
        r = requests.get(kinveyURL, auth=(kinveyUsername, kinveyPassword))
        neclogger(r.text, debug, True)
        kinveyInitialized = True
        
        s = r.text
        entries = json.loads(s)
        for entry in entries:
            whitelistEntry = entry.get('url', None)
            if whitelistEntry:
                whitelistCache.append(whitelistEntry)
                neclogger("Entry = " + whitelistEntry, debug, True)
                            
    rurl = request.url
    o = urlparse.urlparse(rurl)
    requestDomain = None
    requestDomain = o.netloc
    neclogger(requestDomain, debug, True)

    for entry in whitelistCache:
        if entry == requestDomain:
            domainMatch = True
            break
        
    if domainOverride:
        msg = "Overriding domain blocking"
        neclogger(msg, debug, False)
    else:
        if not domainMatch:
            msg = "No match for requesting domain: " + requestDomain
            neclogger(msg,debug, False)
            #app.logger.info(msg)
            rc = 'NYMBLE202'
            data = rc
            js = json.dumps(data)
            result = js
            resp = Response(result, status=202, mimetype='application/javascript')
            return resp
            
 
    if debug == True:
        end = time()
        t = "kinvey lookup elapsed time = " + str(end - start)
        neclogger(t,debug, True)
        #app.logger.info(t)
  
    # get the query string        
    qsdata= request.query_string
    qs = urlparse.parse_qs(qsdata)
    
    # process the user-agent info
    ua = request.headers.get('User-Agent')    
    neclogger("Useragent is:=== " + ua,debug, True)
    platform = None
    browser = None
    version = None
    if ua:
        useragent = UserAgent(ua)
        if useragent.platform:
            platform = useragent.platform
        if useragent.browser:
            browser = useragent.browser
        if useragent.version:
            version = useragent.version
    s_a = "platform," + platform + ",browser," + browser + ",version," + version + ","
    js_a = '"platform": "' + platform + '", "browser": "' + browser + '", "version": "' + version + '"'
              
    # get the client IP address        
    ip = request.remote_addr 
    if ip and'X-Forwarded-For' in request.headers:
        ip_adds = request.headers['X-Forwarded-For'].split(",")   
        ip = ip_adds[0]
    else:
        ip = "0.0.0.0"
    
    # add ip and user-agent data to logging record
    s = "ip," + ip + ","
    json_s = '"ip": "' + ip + '"'
    
    s = s + s_a
    json_s = json_s + ', ' + js_a
    
    s1 = ""
    json_s1 = ""
    cb = ""
    
    # process the query string, return the callback function if provided as a jsonp convenience
    
    if qs:
        keys = qs.keys()
        i = 0
        
        for k in keys:
            # print k, "..."
            # print qs.get(k)
            
            v = qs.get(k)
            if k == 'callback':
                # print k + " = " + v[0]
                cb = v[0]
            s1 = s1 + k + "," + v[i] + ","
            json_s1 = json_s1 + ', "' + k + '": "' + v[i] + '"'
        s = s + s1
        json_s = json_s + json_s1
    st = dt.datetime.now().strftime("date,%Y-%m-%d,time,%H:%M:%S.%f,")
    json_st = dt.datetime.now().strftime('"date": "%Y-%m-%d", "time": "%H:%M:%S.%f", ')
    s = "NECLog: " + st + s
    json_s = 'JSON_NECLog:' + ' { ' + json_st + json_s + ' }'
    
    # write log entry
    neclogger(s,debug, False)
    neclogger(json_s,debug, False)
    
    
    rc = 'NYMBLE200'
    data = rc
    js = json.dumps(data)
    if cb != '':
        result = cb + '(' + js + ')'
        resp = Response(result, status=200, mimetype='application/javascript')
    else:
        result = js
        resp = Response(result, status=200, mimetype='application/json')
    
    if debug == True:
        end = time()
        t = "final elapsed time = ", end - start
        neclogger(t,debug, True)
    return resp
#
# main app init
#app.logger.addHandler(file_handler)
#
app.logger.setLevel(logging.INFO)
port = int(os.environ.get('PORT', 5000))
app.logger.info('Starting up')

d = os.environ.get('DEBUG', False)

if d == "ON":
    debugSwitch = True
    debug = True
else:
    debugSwitch = False
    debug = False
        
d = os.environ.get('DOMAINOVERRIDE', False)
if d == "ON":
    domainOverride = True
    neclogger("domain override is on",debug, False)
else:
    domainOverride = False


# run if not being invoked via gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port,debug=debugSwitch)
    #cProfile.run(host='0.0.0.0',port=port,debug=True)


    