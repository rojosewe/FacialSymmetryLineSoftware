'''
Created on Aug 6, 2017

@author: root
'''
import json
from os.path import expanduser
import os

class Conf:
    
    _conf = None

    @staticmethod
    def loadConf():
        with open('files/conf.json') as f:
            Conf._conf = json.load(f)
            if not "home_file" in Conf._conf or not os.path.isfile(Conf._conf["home_file"]):
                Conf._conf["home_file"] = expanduser("~")
                
    @staticmethod
    def isIn(key):
        if Conf._conf is None:
            Conf.loadConf()
        return key in Conf._conf
    
    @staticmethod
    def get(key):
        if Conf._conf is None:
            Conf.loadConf()
        return Conf._conf[key]
    
    @staticmethod
    def set(key, value):
        if Conf._conf is None:
            Conf.loadConf()
        Conf._conf[key] = value
        with open('files/conf.json', "w+") as f:
            json.dump(Conf._conf, f)