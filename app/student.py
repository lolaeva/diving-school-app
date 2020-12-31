import backend
import psycopg2
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox
'''
Student Table
'''
class Student:
  def __init__(self, master):
    self.master = master
    self.tree_title = Label(master, text='Ogrenci Tablosu')
    b_width = 20
    b1 = Button(master, text='Ekle', width=b_width, command=lambda: [self.openStdWindow(1)])
    b2 = Button(master, text='Guncelle', width=b_width, command=lambda: [self.openStdWindow(2), self.fillEntries()])
    b3 = Button(master, text='Sil', width=b_width, command=lambda : self.deleteStd())
    self.buttons = [b1, b2, b3]
    # TREEVIEW (TABLE)
    master.grid_rowconfigure(4, minsize=10)  # leave an empty row
    self.tree_title = Label(master, text='Ogrenciler')
    self.tree = Treeview(master, show='headings')
    self.tree['columns'] = ("1", "2", "3", "4", "5", "6") 
    self.tree.heading('#1', text='TC Kimlik No')
    self.tree.heading('#2', text='Ad')
    self.tree.heading('#3', text='Soyad')
    self.tree.heading('#4', text='Dogum Tarihi')
    self.tree.heading('#5', text='Seviye')
    self.tree.heading('#6', text='Referans No')
    self.tree.column('1', width = 80)
    self.tree.column('2', width = 80)
    self.tree.column('3', width = 80)
    self.tree.column('4', width = 60)
    self.tree.column('5', width = 20)
    self.tree.column('6', width = 40)
    self.style_tree = Style()
    self.style_tree.configure('Treeview', rowheight=20)
    # on row selection, bind elements in row to content function
    self.tree.bind('<ButtonRelease-1>', self.selectStudentRow)
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
      for i in range(3):
        buttons[i].grid(row=3, column=i+1, sticky='nsew')
      tree_win[1].grid(row=2, column=1, sticky='sw')
      tree_win[2].grid(row=5, column=6, sticky='ns')
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
      messagebox.showerror(parent=self.master, title='Ogrenci yok', message='Ogrenci seciniz')
      self.checkSelectResult = False
    return self.checkSelectResult

  # ******************* VIEW TABLE ************************
  def viewStd(self):
    self.tree.delete(*self.tree.get_children())       # empty table on every execution
    for row in backend.showStd():
      self.tree.insert('', END, values=row)

  def selectStudentRow(self, event):
    # get row values on selection
    current_item = self.tree.item(self.tree.focus())
    self.tc    = current_item['values'][0]
    self.fname = current_item['values'][1]
    self.lname = current_item['values'][2]
    self.bdate = current_item['values'][3]
    self.level = current_item['values'][4]
    self.refno = current_item['values'][5]

  # **************** INSERT UPDATE DELETE ********************
  def fillEntries(self):
    if not self.checkSelectResult:
      return 0
    # insert selected row values (from function selectRow) to entries to new window
    self.tc_entry.insert(0, self.tc)
    self.fname_entry.insert(0, self.fname)
    self.lname_entry.insert(0, self.lname)
    self.bdate_entry.insert(0, self.bdate)

  def getEntryValues(self):
    # get entry values for insertion and update
    tc    = self.tc_text.get()
    fname = self.fname_text.get()
    lname = self.lname_text.get()
    bdate = self.bdate_text.get()
    level = self.level_text.get()
    refname = self.refno_text.get().split()[0]
    reflname = self.refno_text.get().split()[1]
    return [tc, fname, lname, bdate, level, refname, reflname]
    
  def insertStd(self):
    self.fname_entry = ''
    self.lname_entry = ''
    self.tc_entry    = '' 
    self.bdate_entry = '' 
    self.level_entry = '' 
    try:
      entry_values = self.getEntryValues()
      query = backend.insertStd(entry_values)
      messagebox.showinfo(parent=self.new_window, title='Success', message=query)
      self.viewStd()        # update table view
      self.new_window.destroy()
    except Exception as e:
      messagebox.showerror(parent=self.new_window, title='Error', message=e)

  def updateStd(self):
    if self.checkSelectResult: 
      try:
        entry_values = self.getEntryValues()
        std_info = entry_values[:-2]
        ref_no = backend.getTrnNo(entry_values[-2], entry_values[-1])  # get ref no from refname
        std_info.append(ref_no)    # add all student values to one list
        query = backend.updateStd(std_info)
        messagebox.showinfo(parent=self.new_window, title='Success', message=query)
        self.viewStd()             # update table view
        self.new_window.destroy()
      except Exception as e:
        messagebox.showerror(parent=self.new_window, title='Error', message=e)

  def deleteStd(self):
    if self.checkSelection(): 
      confirm = messagebox.askyesno(parent=self.master, title='Ogrenci siliniyor', message='Secilen ogrenci silinsin mi?')
      if confirm == True:
        try:
          query = backend.deleteStd(self.tree.set(self.tree.selection())['1'])      #delete function in backend gets ssn as input
          messagebox.showinfo(parent=self.master, title='Success', message=query)    #print trigger sql notice in messagebox
          self.viewStd()          # update table view
          return 0
        except Exception as e:
          messagebox.showerror(parent=self.master, title='Error', message=e)

  # ********************** OPEN NEW WINDOW DOR INSERTION AND UPDATE *****************************
  def openStdWindow(self, button_id):  
    if button_id==2:
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
      title('Ogrenci Ekle')
      b1 = Button(self.new_window, text='Ekle', width=20, command=self.insertStd).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')
  
    else:
      title('Ogrenci Yenile')
      b1 = Button(self.new_window, text='Yenile', width=20, command=self.updateStd).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')

    # TC
    l1 = Label(self.new_window, text='TC No: ').grid(row=1, column=1, sticky='w')
    self.tc_text=StringVar()
    self.tc_entry = Entry(self.new_window,textvariable=self.tc_text,width=entry_width)
    self.tc_entry.grid(row=1, column=2, sticky="nsew")
    # first name
    l2 = Label(self.new_window, text='Ad: ').grid(row=2, column=1, sticky='w')
    self.fname_text=StringVar()
    self.fname_entry = Entry(self.new_window, textvariable=self.fname_text, width=entry_width)
    self.fname_entry.grid(row=2, column=2, sticky="nsew") 
    # last name
    l3 = Label(self.new_window, text='Soyad: ').grid(row=3, column=1, sticky='w')
    self.lname_text=StringVar()
    self.lname_entry = Entry(self.new_window,textvariable=self.lname_text,width=entry_width)
    self.lname_entry.grid(row=3, column=2, sticky="nsew")
    # birthdate
    l4 = Label(self.new_window, text='Dogum Tarihi: ').grid(row=4, column=1, sticky='w')
    self.bdate_text=StringVar()
    self.bdate_entry = Entry(self.new_window,textvariable=self.bdate_text,width=entry_width)
    self.bdate_entry.grid(row=4, column=2, sticky="nsew")
    # level
    l5 = Label(self.new_window, text='Seviye: ').grid(row=5, column=1, sticky='w')
    levels = backend.getStdLevel()
    self.level_text = StringVar(self.new_window)
    self.level_text.set(levels[0])
    self.level_entry = OptionMenu(self.new_window, self.level_text, levels[0], *levels)
    self.level_entry.grid(row=5, column=2, sticky="nsew")
    # refno
    l5 = Label(self.new_window, text='Referans Egitmen: ').grid(row=6, column=1, sticky='w')
    # get trainer name and surname from dropdown menu
    trainers = backend.getTrnName()
    self.refno_text = StringVar(self.new_window)
    self.refno_text.set(trainers[0]) # default value
    self.refno_entry = OptionMenu(self.new_window, self.refno_text, trainers[0], *trainers)
    self.refno_entry.grid(row=6, column=2, sticky="nsew")
    