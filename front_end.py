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
        #Make a menu bar
        self.make_menu(master)
        
        #Space for user input
        self.make_input_bar(master)
        
        #Space for label to let individual know progress
        self.make_label(master)
        
        self.make_error_label(master)
        
        #Load all the GIF Pics and start running the image
        self.photo_index = 0
        self.pictures = self.load_photos(master)
        self.run_gif(master)
        
        #Bind the enter button to new input
        master.bind("<Return>", lambda event: self.new_input(event, master))
        self.cur = 99
        
        
        #Create the attender
        self.attender = attendance()
        
    def make_label(self, master):
        self.label = tk.Label(master, bg='gray15', fg='white', font=("Helvetica", 80))
        self.label.pack(anchor=tk.CENTER)
        
    def make_error_label(self, master):
        self.error_label = tk.Label(master, bg='gray15', fg='red', font=('Helvetica', 30))
        #self.error_label.pack()
        
    def make_input_bar(self, master):
        self.text_entry = tk.Entry(master, show='*', bg='gray15',bd='0', fg='white', justify='center', font=("Helvetica", 30))
        self.text_entry.pack(expand=True, anchor=tk.CENTER)
        
        
    def new_input(self, event, master):
        new_id = self.text_entry.get()
        self.text_entry.delete(0, 'end')
        self.name = self.attender.run(new_id)
        """"EDIT MADE TO RETURN NONE, CAN HANDLE THINGS NOT FOUND IN DICT"""
        if self.name == None:
            return
        self.label.configure(text=self.name + " checked in")
        self.error_label.configure(text="Whoops")
        master.after(100, self.clear_text, master)
        
    def clear_text(self, master):
        if self.name + " checked in" != self.label.cget("text"):
            return
        if self.cur == 14:
            self.cur = 99
            return
        self.label.configure(fg='gray%d'%(self.cur))
        self.cur -= 1
        master.after(35, self.clear_text, master)
         
        
        
    def load_photos(self, master):
        photos = []
        for i in range(0, 90):
            photos.append(tk.PhotoImage(file='gifImages/tmp-%d.gif'%(i)))
        self.w = tk.Label(master, image=photos[0], bg='gray15', anchor=tk.N)
        self.w.photo = photos[0]
        self.w.pack(expand=True)
        return photos
        
    def run_gif(self, master):
        if self.photo_index == 90:
            self.photo_index = 0
        self.w.photo = self.pictures[self.photo_index]
        self.w.config(image=self.pictures[self.photo_index])
        self.w.pack(expand=True)
        self.photo_index += 1
        master.after(50, self.run_gif, master)
        
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