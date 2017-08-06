'''
Created on 16 Apr 2017

@author: rweffercifue
'''
import json
from utils.conf import Conf as cf
DEFAULT_LANG = "es_ES"
language = DEFAULT_LANG
messages = {}

def load(language=DEFAULT_LANG):
    global messages
    language = cf.get("language") if cf.isIn("language") else DEFAULT_LANG
    with open("files/lang/%s.json" % language) as f:
        messages = json.load(f)
load()