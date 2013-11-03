import os
import sys
from flask import Flask, render_template, make_response
from flask import request
from flask import Response
from time import clock, time
from werkzeug.useragents import UserAgent
from urlparse import urlparse, parse_qs

import logging
import json
import datetime as dt
import requests
import httplib

file_handler = logging.FileHandler('./app.log')
USE_X_FORWARDED_HOST = True

app = Flask(__name__)
debug = False

httplib.HTTPConnection.debuglevel = 1

kinveyBaseURL = 'https://baas.kinvey.com'
kinveyAppKey = 'kid_PPxAbHjIxJ'
kinveyAppSecret = '9ac1e39ec57a443e98950b9af6c18c86'
kinveyUsername = 'nymblenec'
kinveyPassword = 'pwd4nymble'
kinveyInitialized = False
whitelistCache = []
debugSwitch = False
domainOverride = False

taleoAPIUsername = 'chequedtaleoapitest'
taleoAPIPassword = 'pwd4taleoapi'
taleoAPICompany = 'CHEQUED'

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

def taleoAPISetup():

    dispatcherURL = "https://tbe.taleo.net/MANAGER/dispatcher/api/v1/serviceUrl/CHEQUED"
    testURL = "https://app.chequed.com"
    currentAPIURL = None
    loginURL = "https://ch.tbe.taleo.net/CH07/ats/api/v1/login"
    basicHeaders = '{"Content-type": "application/json"}'
    taleoHeaders = '"Content-type": "application/json", "Cookie": "authToken={authToken}"'
    
    
    print dispatcherURL
    print basicHeaders
    baseHeader = json.loads(basicHeaders)
    print baseHeader
    r = requests.get(dispatcherURL, headers=baseHeader)
    print r
    print r.json()
    print r.text
    
    s = r.text
    responseEntries = json.loads(s)
    respEntry = responseEntries['response']
    print respEntry
    currentAPIURL = respEntry['URL']
    print currentAPIURL
    
    if currentAPIURL:
        loginURL = currentAPIURL + "/login"
    else:
        neclogger("no api url", True, True)
        return False
    
    userName = "chequedtaleoapitest"
    password = "pwd4taleoapi"
    orgCode = "CHEQUED"
    #loginParams = '"orgCode":" ' + orgCode + '",' + '"userName":" + userName + '"," + '"password":"' + password + '"'
    loginParams = '?orgCode=' + orgCode + '&userName=' + userName + '&password=' + password
 
    print loginParams
    print loginURL
    
    r = requests.post(loginURL+loginParams,headers=json.loads(basicHeaders))
    print r
    print r.json()
    print r.text

    s = r.text
    responseEntries = json.loads(s)
    respEntry = responseEntries['response']
    print "respEntry"
    print respEntry
    authToken = respEntry['authToken']
    print "authToken"
    print authToken

    print "taleoHeaders"
    s = taleoHeaders.format(**locals())
    print s
    
   # neclogger(r.json, True, True)
    return True
    
#curl -k -X POST "https://ch.tbe.taleo.net/CH07/ats/api/v1/login?orgCode=CHEQUED&userName=chequedtaleoapitest&password=pwd4taleoapi"
 
 #"Content-Type: application/json" -H "Cookie: authToken=webapi2-1796325871408428851"
 
#{"response":{"URL":"https://ch.tbe.taleo.net/CH07/ats/api/v1/"},"status":{"detail":{},"success":true}}macbook-pro-dev:apites

 #  docs = docs.rstrip("\r\n")
 #   d = '{ "docs": [' + docs + ' ]}'
 #   #print d
    # jd = json.loads(d)
 #   headers = {'content-type': 'application/json'}, {'Cookie': 'authToken='}
    #print bulkdocsURL
    #print alldocsURL
  #  r = requests.post(bulkdocsURL, auth=('rodan','pwd4nsyrt'), headers=headers, data=d)



@app.route('/taleotest')
def taleo_test():   
 
    taleo_data = 'Taleo Test'
    neclogger(request.query_string, True, True)
    
    print "test google"
    dispatcherHeaders = {'Content-type': 'application/json'}
    r = requests.get("http://www.google.com",headers=dispatcherHeaders)
    print r
    #print r.json
    #chequedDispatcherURL = ""
    #loginURL = chequedDispatcherURL + '/login'

    taleoAPISetup()
    
    qs = request.query_string
    print qs
    
    qs = parse_qs(qs, keep_blank_values=True)
    print qs

    print "make_response..."
    return render_template('home.html', taleo_data=request.query_string)
    resp = make_response(render_template('home.html', taleo_data=request.query_string),200)
    print "after make_response"
    resp.headers['X-Frame-Options'] = 'ALLOW'
    print resp
    print resp.headers
    print resp.data
    return resp

# curl -k -X POST "https://ch.tbe.taleo.net/CH07/ats/api/v1/login?orgCode=CHEQUED&userName=chequedtaleoapitest&password=pwd4taleoapi"

# curl https://tbe.taleo.net/MANAGER/dispatche1/serviceUrl/CHEQUED
# {"response":{"URL":"https://ch.tbe.taleo.net/CH07/ats/api/v1/"},"status":{"detail":{},"success":true}}macbook-pro-dev:apitest


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

logging.basicConfig() 
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# run if not being invoked via gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port,debug=debugSwitch)
    #cProfile.run(host='0.0.0.0',port=port,debug=True)


    