#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 23:51:00 2017

@author: MoniAli
"""
import pickle as p

f = open('dataStore.p')
dictionary = p.load(f)
f.close()
l = []
for name in dictionary:
    print dictionary[name]
    b = raw_input("Would you like to erase?") == 'T'
    if b:
        l.append(name)
for name in l:
    dictionary.pop(name)
f = open('dataStore.p', 'w+')
p.dump(dictionary, f)
f.close()