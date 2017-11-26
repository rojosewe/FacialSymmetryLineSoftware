'''
Created on 17 Apr 2017

@author: rweffercifue
'''
import ngui
from utils import JsonLoader

JsonLoader.migrateDB()
ngui.start()
