#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 15:56:04 2017

@author: MoniAli
"""
import Tkinter as tk
from attendance import attendance


class Reader(object):
        
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()
        
        self.make_menu(master)
        self.pictures = self.load_photos()
        self.run_gif(master)
        
    def load_photos(self):
        pass
        
    def run_gif(self, master):
        photo = tk.PhotoImage(file='giphy.gif')
        self.w = tk.Label(master, image=photo, bg='gray15')
        self.w.photo = photo
        self.w.pack(fill="none", expand=True)
        
    def make_menu(self, master):
        
        self.menu = tk.Menu(master)
        
        master.config(menu=self.menu)
        
        filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu = filemenu)
        filemenu.add_command(label="Change Google Spreadsheet", command=self.change_spreadsheet)
        filemenu.add_command(label="Change Worksheet", command=self.change_worksheet)
        filemenu.add_command(label="Change Event", command=self.change_event)
        filemenu.add_separator()
        filemenu.add_command(label="Add Users", command=self.add_users)
        filemenu.add_command(label="Edit Users", command=self.edit_users)
        
    
    def change_event(self):
        pass
    
    def change_worksheet(self):
        pass
    
    def change_spreadsheet(self):
        pass
    
    def edit_users(self):
        print "We editing"
        
    def add_users(self):
        print "We adding"
    
        
if __name__ == "__main__":
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(("%dx%d")%(width, height))
    root.configure(background='gray15')
    Reader(root)
    root.mainloop()