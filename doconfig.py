#!/usr/bin/python

class Medoc:
    def setMedoc(self, obj):
        self.name = obj[0]
        self.frequency = obj[1]
        self.tmp = obj[2].split("-")
        for h in self.tmp:
            self.hours.append(h)
        
    def __init__(self):
        self.name = ''
        self.frequency = 0
        self.hours = []

def conf_open():
    filename = "/var/www/html/obsy.conf"
    
    with open(filename, "r") as f:
        confList = f.read().splitlines()
    
    confList = filter(None, confList)
    return confList


def get_conf(confList):
    objs = []

    for e in confList:
        obj = e.split("+")
        objs.append(obj)
    
    return objs


def doThisShit(oB):
    medoc = Medoc()
    medoc.setMedoc(oB)
    print 'name: ' + medoc.name
    print 'freq: ' + str(medoc.frequency)
    for h in medoc.hours:
        print 'hour: ' + h
    print ''


