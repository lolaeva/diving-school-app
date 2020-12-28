"""
Author: Lola
Date: Dec 2020
An app that stores and modifies simplified company database
"""
import os
import psycopg2
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox
import sys
import backend
from app.student import Student
from app.trainer import Trainer
from app.group import Group
from app.program import Program


# **********************************************************************
# Class object
# **********************************************************************
class MainWindow:
  def __init__(self, master):
    self.master = master
    master.title('Öz Yıldız Dalış Okulu Bilgi Sistemi')
    master.geometry('700x500')
    master.grid_columnconfigure(0, minsize=80)  # set leftmost column width
    master.grid_rowconfigure(0, minsize=20) 
    master.grid_rowconfigure(2, minsize=20) 
    #*********** NAVIGATION ************
    self.header = Label(master, text='Öz Yıldız Dalış Okulu Bilgi Sistemi', font=(None, 12)).grid(row=1, column=1, columnspan=3, sticky='w')
    self.header_button1 = Button(master, text='Bilgi Sistemi', width=20, command=lambda: self.new_window('2', DatabaseWindow))
    self.header_button1.grid(row=3, column=1, sticky='w')
    self.header_button2 = Button(master, text='Views', width=40)
    self.header_button2.grid(row=3, column=2, sticky='w')
    self.header_button2 = Button(master, text='Close', width=20, command=master.destroy)
    self.header_button2.grid(row=3, column=3, sticky='w')

  def new_window(self, level_no, _class):
    self.new = Toplevel(self.master)
    _class(self.new, level_no)

class DatabaseWindow:
  def __init__(self, master, level_no):
    self.master = master
    master.title('Öz Yıldız Dalış Okulu Bilgi Sistemi')
    master.geometry('700x500')
    master.grid_columnconfigure(0, minsize=80)  # set leftmost column width
    master.grid_rowconfigure(2, minsize=40)  # leave an empty row
    S = Student(master) # Student Page
    G = Group(master)   # Group Page
    P = Program(master)
    T = Trainer(master)
    #*********** NAVIGATION ************
    self.header = Label(master, text='Öz Yıldız Dalış Okulu Bilgi Sistemi', font=(None, 12)).grid(row=0, column=2, columnspan=3, sticky='w')
    self.header_button = Button(master, text='Ana Sayfa', width=20, command=master.destroy)
    self.header_button.grid(row=0, column=1)
    master.grid_rowconfigure(0, minsize=50)
    b_width = 22
    self.std_button = Button(master, text='Öğrenci',width=b_width, command=lambda:[S.toggle(S.buttons, S.tree_window), T.hide(), P.hide(), G.hide(), S.viewStd()])
    self.std_button.grid(row=1, column=1, sticky='nsew')
    self.trn_button = Button(master, text='Eğitmen',width=b_width, command=lambda:[T.toggle(T.buttons, T.tree_window), S.hide(), P.hide(), G.hide(), T.viewTrn()])
    self.trn_button.grid(row=1, column=2, sticky='nsew')
    self.prg_button = Button(master, text='Program',width=b_width, command=lambda:[P.toggle(P.buttons, P.tree_window, P.infos), S.hide(), T.hide(), G.hide(), P.viewPrg()])
    self.prg_button.grid(row=1, column=3, sticky='nsew')
    self.grp_button = Button(master, text='Grup',width=b_width, command=lambda:[G.toggle(G.buttons, G.tree_window, G.infos), S.hide(), T.hide(), P.hide(), G.viewGrp()])
    self.grp_button.grid(row=1, column=4, sticky='nsew')

# **********************************************************************
# Tkinter Window
# **********************************************************************
if __name__ == "__main__":
  window = Tk()
  comp_app = MainWindow(window)
  window.mainloop() 