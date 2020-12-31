"""
Author: Group 
Date: Dec 2020
An app that stores and modifies simplified company database
"""

import psycopg2
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox
import backend
from app.student import Student
from app.trainer import Trainer
from app.group import Group
from app.program import Program
from app.group_std import GroupStd
import datetime

# **********************************************************************
# Class object
# **********************************************************************
class MainWindow:
  def __init__(self, master):
    self.master = master
    master.title('Öz Yıldız Dalış Okulu Bilgi Sistemi')
    master.geometry('750x500')
    master.grid_columnconfigure(0, minsize=120)  # set leftmost column width
    master.grid_rowconfigure(0, minsize=20) 
    master.grid_rowconfigure(2, minsize=20)
    master.grid_rowconfigure(4, minsize=20)
    #*********** NAVIGATION ************
    self.header = Label(master, text='Öz Yıldız Dalış Okulu Bilgi Sistemi', font=(None, 12)).grid(row=1, column=1, columnspan=3, sticky='w')
    self.header_button1 = Button(master, text='Bilgi Sistemi', width=20, command=lambda: self.new_window('2', DatabaseWindow))
    self.header_button1.grid(row=3, column=1, sticky='w')
    self.header_button2 = Button(master, text='Yaklasan Etkinlikler', width=20, command=lambda: [self.toggle(self.tree_window), self.view()])
    self.header_button2.grid(row=3, column=2, sticky='w')
    self.header_button4 = Button(master, text='Close', width=20, command=master.destroy)
    self.header_button4.grid(row=3, column=3, sticky='w')
    # **************************************************************************************
    # ************ VIEW TABLE *************************************************************
    self.tree_title = Label(master, text='Gelecek 3 Gundeki Etkinlikler')
    self.tree = Treeview(master, show='headings')
    self.tree['columns'] = ("1", "2", "3", "4") 
    self.tree.heading('#1', text='Grup ID')
    self.tree.heading('#2', text='Program Adi')
    self.tree.heading('#3', text='Gun')
    self.tree.heading('#4', text='Egitmeni')
    self.tree.column('1', width = 20)
    self.tree.column('2', width = 40)
    self.tree.column('3', width = 60)
    self.tree.column('4', width = 80)
    self.style_tree = Style()
    self.style_tree.configure('Treeview', rowheight=20)
    self.sb = Scrollbar(master, orient ='vertical', command = self.tree.yview) 
    self.tree.configure(yscrollcommand = self.sb.set)
    self.tree_window = [self.tree, self.tree_title, self.sb]
    self.hidden = True
  
  def toggle(self, tree_win):
    if self.hidden:
      tree_win[0].grid(row=6, column=1, columnspan=3, rowspan=4, sticky='nsew')
      tree_win[1].grid(row=5, column=1, sticky='sw')
      tree_win[2].grid(row=6, column=4, sticky='nsw')
    else:
      tree_win[0].grid_remove()
      tree_win[1].grid_remove()
      tree_win[2].grid_remove()
    self.hidden = not self.hidden
    
  def view(self):
    self.tree.delete(*self.tree.get_children())       # empty table on every execution
    for row in backend.view():
      self.tree.insert('', END, values=row)
    
  def new_window(self, level_no, _class):
    self.new = Toplevel(self.master)
    _class(self.new, level_no)

class DatabaseWindow:
  def __init__(self, master, level_no):
    self.master = master
    master.title('Öz Yıldız Dalış Okulu Bilgi Sistemi')
    master.geometry('800x500')
    master.grid_columnconfigure(0, minsize=60)  # set leftmost column width
    master.grid_rowconfigure(2, minsize=40)  # leave an empty row
    S = Student(master) # Student Page
    G = Group(master)   # Group Page
    P = Program(master)
    T = Trainer(master)
    GS = GroupStd(master)
    #*********** NAVIGATION ************
    b_width = 20
    self.header = Label(master, text='Öz Yıldız Dalış Okulu Bilgi Sistemi', font=(None, 12)).grid(row=0, column=2, columnspan=3, sticky='w')
    self.header_button = Button(master, text='Ana Sayfa', width=b_width, command=master.destroy)
    self.header_button.grid(row=0, column=1)
    master.grid_rowconfigure(0, minsize=50)
    self.std_button = Button(master, text='Öğrenci',width=b_width, command=lambda:[S.toggle(S.buttons, S.tree_window), GS.hide(), T.hide(), P.hide(), G.hide(), S.viewStd()])
    self.std_button.grid(row=1, column=1, sticky='nsew')
    self.trn_button = Button(master, text='Eğitmen',width=b_width, command=lambda:[T.toggle(T.buttons, T.tree_window), GS.hide(), S.hide(), P.hide(), G.hide(), T.viewTrn()])
    self.trn_button.grid(row=1, column=2, sticky='nsew')
    self.prg_button = Button(master, text='Program',width=b_width, command=lambda:[P.toggle(P.buttons, P.tree_window, P.infos),GS.hide(),  S.hide(), T.hide(), G.hide(), P.viewPrg()])
    self.prg_button.grid(row=1, column=3, sticky='nsew')
    self.grp_button = Button(master, text='Grup',width=b_width, command=lambda:[G.toggle(G.buttons, G.tree_window, G.infos), GS.hide(), S.hide(), T.hide(), P.hide(), G.viewGrp()])
    self.grp_button.grid(row=1, column=4, sticky='nsew')
    self.grp_button = Button(master, text='Grup Ogrenci',width=b_width, command=lambda:[GS.toggle(GS.buttons, GS.tree_window, GS.tree2_window, GS.infos, GS.labels), G.hide(), S.hide(), T.hide(), P.hide(), GS.viewGrpStd()])
    self.grp_button.grid(row=1, column=5, sticky='nsew')

# **********************************************************************
# Tkinter Window
# **********************************************************************
if __name__ == "__main__":
  window = Tk()
  comp_app = MainWindow(window)
  window.mainloop() 