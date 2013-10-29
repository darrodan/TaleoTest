import datetime
import json

logdata2 = '{ "date": "2013-06-20", "time": "19:48:56.285726", "ip": "150.198.1.213", "platform": "windows", "browser": "chrome", "version": "27.0.1453.110", "transition": "fadeout", "pagetime": 10637, "iframe": "False", "authdomain": "www.tacticalsoftware.com", "documentWait": 42 }'


class NECLogEntry:
    'Default NEC Log Entry'
 
    def __init__(self):
        

#        self.date = datetime.datetime.strptime("2013-06-28","%Y-%m-%d")
#        self.time = datetime.datetime.strptime("14:12:44.130688","%H:%M:%S.%f")
#        self.ip = "64.160.7.210"
#        self.platform = "macos"
#        self.browser = "firefox"
#        self.version = "21.0"
#        self.eventType = "timer"
#        self.authdomain = "www.tacticalsoftware.com"
#        self.total = 31
#        self.jqueryLoad = 21
#        self.documentWait = 268
#        self.pagetime = 98809
#        self.replaceurl = "nymble/html/leaderboard-header-ad2.html"
#        self.iframe = False
#        self.transition = "fadeout"
#        
        self.date = ""
        self.time = ""
        self.ip = ""
        self.platform = ""
        self.browser = ""
        self.version = ""
        self.eventType = ""
        self.authdomain = ""
        self.total = -1
        self.jqueryLoad = -1
        self.documentWait = -1
        self.pagetime = -1
        self.replaceurl = ""
        self.iframe = None
        self.transition = ""

       
    def printit(self):

        varnames = vars(self).keys()
        for v in varnames:
            value = getattr(self, v)
            print "NECLogEntry:  Key = " + str(v) + "   Value = " + str(value)
        return True
    
    def update(self,s):
    
        varnames = vars(self).keys()
#        print varnames
        s1 = json.loads(s)
        i = 0
        for key, value in s1.iteritems():
            match = False
            if self.matchvar(key):
                match = True
                #print "found a match for key = " + str(key) + "Value = " + str(value)
                #print "setattr"
                setattr(self, key, value)
        return True
        
    def get_json(self):
        
        s = ""
        varnames = vars(self).keys()
        for v in varnames:
            value = getattr(self, v)
            if isinstance(value, int):
                if s == "":
                    s = '{ "' + v + '": ' + str(value)
                else:
                    s = s + ', "' + v + '": ' + str(value)
            else:                
                if s == "":
                    s = '{ "' + v + '": "' + str(value) + '"'
                else:
                    s = s + ', "' + v + '": "' + str(value) + '"'
                
        s = s + ' }'
        return (s)

    def get_csv(self):

        s = ""
        varnames = vars(self).keys()
        for v in varnames:
            value = getattr(self, v)
            s = s + str(value) + '\t'
        return (s)
    
    def matchvar(self, s):
        varnames = vars(self).keys()
        for v in varnames:
            if s == v:
                #print "found match: " + s
                return True
        return False
        
    
l = NECLogEntry()
l.update(logdata2)
l.printit()

s = l.get_json()
cs = l .get_csv()

print s
print cs

#print vars(NECLogEntry()).keys()

l.printit()
