'''
Created on 16 Apr 2017

@author: rweffercifue
'''
import json

DEFAULT_LANG = "es_ES"
language = DEFAULT_LANG
messages = {}

def load(language=DEFAULT_LANG):
    global messages
    with open("files/lang/%s.json" % language) as f:
        messages = json.load(f)

load()