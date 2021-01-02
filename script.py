"""
Author: Lola Khudoyberdieva 
Database Development: Ihsan Isik, Onur Can Erdem
Date: Dec 2020
An app that stores and modifies diving school database
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
    master.grid_columnconfigure(0, minsize=100)  # set leftmost column width
    master.grid_rowconfigure(0, minsize=20) 
    master.grid_rowconfigure(2, minsize=20)
    master.grid_rowconfigure(4, minsize=20)
    #*********** NAVIGATION ************
    self.header = Label(master, text='Öz Yıldız Dalış Okulu Bilgi Sistemi', font=(None, 12)).grid(row=1, column=1, columnspan=3, sticky='w')
    self.header_button1 = Button(master, text='Bilgi Sistemi', width=20, command=lambda: self.new_window('2', DatabaseWindow))
    self.header_button1.grid(row=3, column=1, sticky='w')
    self.header_button2 = Button(master, text='Yaklasan Etkinlikler', width=20, command=lambda: [self.toggle(1), self.view()])
    self.header_button2.grid(row=3, column=2, sticky='w')
    self.header_button2 = Button(master, text='Egitmen Ogrencileri', width=20, command=lambda: [self.toggle(2), self.having()])
    self.header_button2.grid(row=3, column=3, sticky='w')
    self.header_button4 = Button(master, text='Kapat', width=20, command=master.destroy)
    self.header_button4.grid(row=3, column=4, sticky='w')

    self.fr = Frame(master)
    self.fr.grid(row=5, column=1, columnspan=5, sticky='nsew')
    self.fr.rowconfigure(5, weight=1)
    self.fr.columnconfigure(1, weight=1)
    # **************************************************************************************
    # ************ VIEW TABLE *************************************************************
    self.tree_title = Label(self.fr, text='Gelecek 3 Gundeki Etkinlikler')
    self.tree = Treeview(self.fr, show='headings')
    self.tree['columns'] = ("1", "2", "3", "4") 
    self.tree.heading('#1', text='Grup ID')
    self.tree.heading('#2', text='Program Adi')
    self.tree.heading('#3', text='Gun')
    self.tree.heading('#4', text='Egitmeni')
    self.tree.column('1', width = 20)
    self.tree.column('2', width = 40)
    self.tree.column('3', width = 40)
    self.tree.column('4', width = 40)
    self.style_tree = Style()
    self.style_tree.configure('Treeview', rowheight=20)
    self.sb = Scrollbar(self.fr, orient ='vertical', command = self.tree.yview) 
    self.tree.configure(yscrollcommand = self.sb.set)
    self.tree_window = [self.tree, self.tree_title, self.sb]

    # **************************************************************************************
    # ************ HAVING TABLE *************************************************************
    self.tree2_title = Label(self.fr, text='Ogrenci Sayisi 5ten fazla olan Egitmenler')
    self.tree2 = Treeview(self.fr, show='headings')
    self.tree2['columns'] = ('1', '2', '3') 
    self.tree2.heading('#1', text='Adi')
    self.tree2.heading('#2', text='Soyadi')
    self.tree2.heading('#3', text='Ogrenci Sayisi')
    self.tree2.column('1', width = 40)
    self.tree2.column('2', width = 40)
    self.tree2.column('3', width = 20)
    self.style_tree2 = Style()
    self.style_tree2.configure('Treeview', rowheight=20)
    self.sb2 = Scrollbar(self.fr, orient ='vertical', command = self.tree2.yview) 
    self.tree2.configure(yscrollcommand = self.sb2.set)
    self.tree2_window = [self.tree2, self.tree2_title, self.sb2]
    self.hidden = True
    self.hidden2 = True
    

  def showViewTree(self):
    self.tree_window[0].grid(row=6, column=1, columnspan=4, rowspan=4, sticky='nsew')
    self.tree_window[1].grid(row=5, column=1, sticky='sw')
    self.tree_window[2].grid(row=6, column=5, sticky='nsw')

  def hideViewTree(self):
    self.tree_window[0].grid_remove()
    self.tree_window[1].grid_remove()
    self.tree_window[2].grid_remove()

  def showHavingTree(self):
    self.tree2_window[0].grid(row=6, column=1, columnspan=2, rowspan=4, sticky='nsew')
    self.tree2_window[1].grid(row=5, column=1, sticky='sw')
    self.tree2_window[2].grid(row=6, column=7, sticky='nsw')

  def hideHavingTree(self):
    self.tree2_window[0].grid_remove()
    self.tree2_window[1].grid_remove()
    self.tree2_window[2].grid_remove()

  def toggle(self, id):
    if id == 1:
      if self.hidden == True:
        if self.hidden2 == True:
          self.showViewTree()
          self.hidden = not self.hidden
        else:
          self.showViewTree()
          self.hideHavingTree()
          self.hidden = not self.hidden
          self.hidden2 = not self.hidden2
      else:
        self.hideViewTree()
        self.hidden = not self.hidden
    elif id == 2:
      if self.hidden2 == True:
        if self.hidden == True:
          self.showHavingTree()
          self.hidden2 = not self.hidden2
        else:
          self.showHavingTree()
          self.hideViewTree()
          self.hidden = not self.hidden
          self.hidden2 = not self.hidden2
      else:
        self.hideHavingTree()
        self.hidden2 = not self.hidden2


  def view(self):
    self.tree.delete(*self.tree.get_children())       # empty table on every execution
    for row in backend.view():
      self.tree.insert('', END, values=row)

  def having(self):
    self.tree2.delete(*self.tree2.get_children())       # empty table on every execution
    for row in backend.having():
      self.tree2.insert('', END, values=row)

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
    self.grp_button = Button(master, text='Grup Ogrenci',width=b_width, command=lambda:[GS.toggle(GS.buttons, GS.tree_window, GS.tree2_window, GS.infos, GS.labels), G.hide(), S.hide(), T.hide(), P.hide(), GS.viewGrpStd(), GS.noGrpStd()])
    self.grp_button.grid(row=1, column=5, sticky='nsew')

# **********************************************************************
# Tkinter Window
# **********************************************************************
if __name__ == "__main__":
  window = Tk()
  comp_app = MainWindow(window)
  window.mainloop() 