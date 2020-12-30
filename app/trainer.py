import backend
import psycopg2
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox

class Trainer:
  def __init__(self, master):
    # TRAINER DATABASE
    self.master = master
    self.tree_title = Label(master, text='Egitmen Tablosu')
    b_width = 20
    b1 = Button(master, text='Ekle', width=b_width, command=lambda: self.openTrnWindow(1))
    b2 = Button(master, text='Guncelle', width=b_width, command=lambda: [self.openTrnWindow(2), self.fillEntries()])
    b3 = Button(master, text='Sil', width=b_width, command=lambda: self.deleteTrn())
    self.buttons = [b1, b2, b3]
    # TREEVIEW
    master.grid_rowconfigure(4, minsize=10)  # leave an empty row
    # self.tree_title = Label(master, text='Ogrenciler')
    self.tree = Treeview(master, show='headings')
    self.tree['columns'] = ("1", "2", "3", "4", "5", "6") 
    self.tree.heading('#1', text='TC Kimlik No')
    self.tree.heading('#2', text='Ad')
    self.tree.heading('#3', text='Soyad')
    self.tree.heading('#4', text='Maas')
    self.tree.heading('#5', text='Seviye')
    self.tree.heading('#6', text='Komisyon')
    self.tree.column('1', width = 80)
    self.tree.column('2', width = 80)
    self.tree.column('3', width = 80)
    self.tree.column('4', width = 60)
    self.tree.column('5', width = 30)
    self.tree.column('6', width = 30)
    self.style_tree = Style()
    self.style_tree.configure('Treeview', rowheight=20)
    # on row selection, bind elements in row to content function
    self.tree.bind('<ButtonRelease-1>', self.selectTrainerRow)
    self.sb = Scrollbar(master, orient ='vertical', command = self.tree.yview) 
    self.tree.configure(yscrollcommand = self.sb.set)
    self.tree_window = [self.tree, self.tree_title, self.sb]

    # TOGGLE HIDE/ REVEAL
    self.hidden = True
  # when other table buttons are clicked, hide this table
  def hide(self):
    self.hidden = False
    self.toggle(self.buttons, self.tree_window)

  def toggle(self, buttons, tree_win):
    if self.hidden:
      tree_win[0].grid(row=5, column=1, columnspan=5, rowspan=4, sticky='nsew')
      tree_win[1].grid(row=2, column=1, sticky='sw')
      tree_win[2].grid(row=5, column=6, sticky='ns')
      for i in range(3):
        buttons[i].grid(row=3, column=i+1, sticky='nsew')
    else:
      for i in range(3):
        buttons[i].grid_remove()
      tree_win[0].grid_remove()
      tree_win[1].grid_remove()
      tree_win[2].grid_remove()
    self.hidden = not self.hidden

  # ******************* CHECK CONDITIONS ***************** 
  def checkSelection(self):
    self.checkSelectResult = True
    if len(self.tree.set(self.tree.selection()))==0:
      messagebox.showerror(parent=self.master, title='Egitmen yok', message='Egitmen seciniz')
      self.checkSelectResult = False
    return self.checkSelectResult

  # ******************* VIEW TABLE ************************
  def viewTrn(self):
    self.tree.delete(*self.tree.get_children())       # empty table on every execution
    for row in backend.showTrn():
      self.tree.insert('', END, values=row)

  def selectTrainerRow(self, event):
    # get row values on selection
    current_item = self.tree.item(self.tree.focus())
    self.tc    = current_item['values'][0]
    self.fname = current_item['values'][1]
    self.lname = current_item['values'][2]
    self.salary = current_item['values'][3]
    self.level = current_item['values'][4]
    self.coms = current_item['values'][5]
  
  def fillEntries(self):
    if not self.checkSelectResult:
      return 0
    # insert selected row values (from function selectRow) to entries to new window
    self.tc_entry.insert(0, self.tc)
    self.fname_entry.insert(0, self.fname)
    self.lname_entry.insert(0, self.lname)
    self.salary_entry.insert(0, self.salary)
    self.coms_entry.insert(0, self.coms)

  def getEntryValues(self):
    tc    = self.tc_text.get()
    fname = self.fname_text.get()
    lname = self.lname_text.get()
    salary = self.salary_text.get()
    level = self.level_text.get()
    coms = self.coms_text.get()
    return [tc, fname, lname, salary, level, coms]

  def insertTrn(self):
    self.tc_entry     = ''
    self.fname_entry  = ''
    self.lname_entry  = ''
    self.salary_entry = ''
    self.level_entry  = ''
    self.coms_entry   = ''
    try:
      entry_values = self.getEntryValues()
      query = backend.insertTrn(entry_values)
      messagebox.showinfo(parent=self.master, title='Success', message=query)
      self.viewTrn()        # update table view
      self.new_window.destroy()
    except Exception as e:
      messagebox.showerror(parent=self.master, title='Error', message=e)

  def updateTrn(self):
    if self.checkSelectResult: 
      try:
        entry_values = self.getEntryValues()
        query = backend.updateTrn(entry_values)
        messagebox.showinfo(parent=self.master,title='Success', message=query)
        self.viewTrn()        # update table view
        self.new_window.destroy()
      except Exception as e:
        messagebox.showerror(parent=self.master, title='Error', message=e)
 
  def deleteTrn(self):
    if self.checkSelection(): 
      confirm = messagebox.askyesno(parent=self.master,title='Egitmen siliniyor', message='Secilen egitmen silinsin mi?')
      if confirm == True:
        try:
          query = backend.deleteTrn(self.tree.set(self.tree.selection())['1'])      #delete function in backend gets ssn as input
          messagebox.showinfo(parent=self.master, title='Success', message=query)    #print trigger sql notice in messagebox
          self.viewTrn()          # update table view
          return 0
        except Exception as e:
          messagebox.showerror(parent=self.master, title='Error', message=e)

  def openTrnWindow(self, button_id):  
    if button_id==2:  # for update check selection
      if not self.checkSelection():
        return 0
    # open a new window that used for both insert and update
    self.new_window = Toplevel(self.master)
    self.new_window.geometry('420x280')
    self.new_window.grid_columnconfigure(0, minsize=60)  # set leftmost column width
    self.new_window.grid_rowconfigure(0, minsize=30)
    entry_width = 25          # set entry width
    label_width = 25
    def title(txt):
      self.new_window.title = txt
      l0 = Label(self.new_window, text=txt, font=(None, 12)).grid(row=0, column=1, sticky='w')
    
    if button_id==1:          # set title depending on insert or update
      title('Egitmen Ekle')
      b1 = Button(self.new_window, text='Ekle', width=20, command=self.insertTrn).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')

    else:
      title('Egitmen Yenile')
      b1 = Button(self.new_window, text='Yenile', width=20, command=self.updateTrn).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')

    # TC
    l3 = Label(self.new_window, text='TC No: ').grid(row=1, column=1, sticky='w')
    self.tc_text=StringVar()
    self.tc_entry = Entry(self.new_window,textvariable=self.tc_text,width=entry_width)
    self.tc_entry.grid(row=1, column=2, sticky="nsew")
    # first name
    l1 = Label(self.new_window, text='Ad: ').grid(row=2, column=1, sticky='w')
    self.fname_text=StringVar()
    self.fname_entry = Entry(self.new_window, textvariable=self.fname_text, width=entry_width)
    self.fname_entry.grid(row=2, column=2, sticky="nsew") 
    # last name
    l2 = Label(self.new_window, text='Soyad: ').grid(row=3, column=1, sticky='w')
    self.lname_text=StringVar()
    self.lname_entry = Entry(self.new_window,textvariable=self.lname_text,width=entry_width)
    self.lname_entry.grid(row=3, column=2, sticky="nsew")
    # birthdate
    l4 = Label(self.new_window, text='Maasi: ').grid(row=4, column=1, sticky='w')
    self.salary_text=StringVar()
    self.salary_entry = Entry(self.new_window,textvariable=self.salary_text,width=entry_width)
    self.salary_entry.grid(row=4, column=2, sticky="nsew")
    # level
    l5 = Label(self.new_window, text='Seviye: ').grid(row=5, column=1, sticky='w')
    levels = backend.getTrnLevel()
    self.level_text = StringVar(self.new_window)
    self.level_text.set(levels[0])  # default value
    self.level_entry = OptionMenu(self.new_window, self.level_text, levels[0], *levels)
    self.level_entry.grid(row=5, column=2, sticky="nsew")
    # coms
    l5 = Label(self.new_window, text='Komisyon: ').grid(row=6, column=1, sticky='w')
    self.coms_text=StringVar()
    self.coms_entry = Entry(self.new_window, textvariable=self.coms_text,width=entry_width)
    self.coms_entry.grid(row=6, column=2, sticky="nsew")