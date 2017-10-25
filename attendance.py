#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This code is property of Moni (Munsoor Ali)

Any unlawful distribution, usage, or tampering  
will be dealt with the full extent of the law

@author Moni Ali (Munsoor Ali)
"""

import time
import gspread
import getpass
import datetime
import threading
import pickle as p
from Queue import Queue
from oauth2client.service_account import ServiceAccountCredentials


class attendance(object):
    def __init__(self):
 
        self.start_time = datetime.datetime.now() #Get the starting time
        
        self.filename = 'dataStore.p' #default datastore
        
        self.id_list = Queue() #queue to process
        
        self.checked = [] #Lets collect the swipes with timestamps to store in log file
        
        self.id_name_dict = self.read() #Dictionary mapping of hashed IDs to names
        
        self.start_threads() #Begins pool of 5 threads ready to process anything in Queue

        self.sheet = self.google_connect()
        
        self.column = self.find_column()
        
        #Allow time for threads to be initiated and google sheet to connect
        time.sleep(.05)
    
        #Main input loop
        self.run()
        
              
        
      
    def run(self):
        #Loop to continuously gain input from brothers
        while True:
            new_id = (getpass.getpass("Please swipe a JAC card or enter your ID #: "))
            if new_id == 'exit':
                break
            
            #Lets format our JAC # and hash them
            if len(new_id) != 9:
                new_id = hash(new_id[1:10])
            else:
                new_id = hash(new_id)
            
            
            if self.id_name_dict.has_key(new_id):
                self.id_list.put(self.id_name_dict[new_id])
            else:
                name = raw_input("Please enter your name as it appears in the Google Drive ")
                #Exit option
                if name == 'exit':
                    break
                self.id_name_dict[new_id] = name
                self.id_list.put(self.id_name_dict[new_id])
                
            #Lets assume this new addition will be properly checked in by other thread
            self.checked.append((self.id_name_dict[new_id], datetime.datetime.now()))
           
        #Dump the object for later recovery
        f = open(self.filename, 'w+')
        p.dump(self.id_name_dict, f)
        f.close()
    
        self.format_log()
    
    def processor(self):
        while True:
            self.lock.acquire()
            while self.id_list.empty():
                time.sleep(.01)
            current_id = self.id_list.get()
            self.lock.release()
            try:
                cell = self.sheet.find(current_id)
                self.sheet.update_cell(cell.row, self.column, 1)
            except gspread.exceptions.CellNotFound as e:
                print str(e) + " was not found in the Google Sheet"
            #update google sheet if it exists
   
    def format_log(self):
        pm = self.start_time.hour > 12
        
        f = open(self.logname, 'w+')
        
        f.write("Event began at " + str(self.start_time.hour%12) + ":" + str(self.start_time.minute).zfill(2))
        f.write(" PM") if pm else f.write(" AM")
        f.write("\n\n")
        
        self.checked.sort()
        
        for person in self.checked:
            f.write(str(person[0]) + " arrived at " + str(person[1].hour%12) + ":" + str(person[1].minute).zfill(2))
            f.write(" PM") if pm else f.write(" AM")
            f.write('\n')
        
        
    def find_column(self):
        while True:
            try:
                column_name = raw_input("What is the name of todays event? ")
                self.logname = column_name + "_logfile.txt"
                cell = self.sheet.find(column_name)
                return cell.col
            except gspread.exceptions.CellNotFound as e:
                print str(e) + " is not a valid column in the Google Sheet"
    
    def google_connect(self):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        
        
        sheet = client.open("Fall 2017 Attendance Spreadsheet.xlsx")
        
        while True:
            try:
                sheet_name = raw_input("Please enter the title of the worksheet you would like to update: ")
                w_sheet = sheet.worksheet(sheet_name)
                break
            except gspread.exceptions.WorksheetNotFound as e:
                print str(e) + " is not a valid worksheet in this spreadsheet"
                
        return w_sheet
        
    
    def start_threads(self):
        self.lock = threading.Lock()
        self.threads = []
        for i in range(5):
            t = threading.Thread(target = self.processor)
            self.threads.append(t)
        for thread in self.threads:
            thread.daemon = True #Temporary, add stop events later
            thread.start()
        
    def read(self):
        try:
            f = open(self.filename)
            id_name_dict = p.load(f)
            f.close()
            return id_name_dict
        except IOError:
            return {}

if __name__ == '__main__':
    print "Welcome to the attendance program"
    attendance()