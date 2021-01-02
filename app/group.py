import backend
import psycopg2
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox

class Group:
  def __init__(self, master):
    self.master = master
    self.tree_title = Label(master, text='Grup Tablosu')
    master.grid_rowconfigure(2, minsize=40)  
    master.grid_rowconfigure(4, minsize=30) 
    b_width = 20
    b1 = Button(master, text='Ekle', width=b_width, command=lambda: self.openGrpWindow(1))
    b2 = Button(master, text='Guncelle', width=b_width, command=lambda: [self.openGrpWindow(2), self.fillEntries()])
    b3 = Button(master, text='Sil', width=b_width, command=lambda: self.deleteGrp())
    self.buttons = [b1, b2, b3]
    i1 = Label(master, text='Dahil Oldugu Program: ')
    self.t1 = Label(master, text='')
    self.t2 = Label(master, text='')
    self.infos = [i1,self.t1,self.t2]
    # TREEVIEW
    self.tree_title = Label(master, text='Ogrenciler')
    self.tree = Treeview(master, show='headings')
    self.tree['columns'] = ("1", "2", "3", "4") 
    self.tree.heading('#1', text='Grup ID')
    self.tree.heading('#2', text='Program ID')
    self.tree.heading('#3', text='Egitmen No')
    self.tree.heading('#4', text='Gun')
    self.tree.column('1', width = 60)
    self.tree.column('2', width = 60)
    self.tree.column('3', width = 60)
    self.tree.column('4', width = 60)
    self.style_tree = Style()
    self.style_tree.configure('Treeview', rowheight=20)
    # on row selection, bind elements in row to content function
    self.tree.bind('<ButtonRelease-1>', self.selectGroupRow)
    self.sb = Scrollbar(master, orient ='vertical', command = self.tree.yview) 
    self.tree.configure(yscrollcommand = self.sb.set)
    self.tree_window = [self.tree, self.tree_title, self.sb]
    # TOGGLE HIDE/ REVEAL
    self.hidden = True
  # when other table buttons are clicked, hide this table
  def hide(self):
    self.hidden = False
    self.toggle(self.buttons, self.tree_window, self.infos)

  def toggle(self, buttons, tree_win, infos):
    if self.hidden:
      tree_win[0].grid(row=6, column=1, columnspan=6, rowspan=4, sticky='nsew')
      tree_win[1].grid(row=2, column=1, sticky='sw')
      tree_win[2].grid(row=6, column=6, sticky='ns')
      for i in range(3):
        buttons[i].grid(row=3, column=i+1, sticky='nsew')
      for i in range(2):
        infos[i].grid(row=4, column=i+1, sticky='w')
      infos[2].grid(row=5, column=1, columnspan=3, sticky='w')
    else:
      for i in range(3):
        buttons[i].grid_remove()
      for i in range(3):
        infos[i].grid_remove()
      tree_win[0].grid_remove()
      tree_win[1].grid_remove()
      tree_win[2].grid_remove()
    self.hidden = not self.hidden

  # ******************* CHECK CONDITIONS ***************** 
  def checkSelection(self):
    self.checkSelectResult = True
    if len(self.tree.set(self.tree.selection()))==0:
      messagebox.showerror(parent=self.master, title='Grup yok', message='Grup seciniz')
      self.checkSelectResult = False
    return self.checkSelectResult

  # ******************* VIEW TABLE ************************
  def viewGrp(self):
    self.tree.delete(*self.tree.get_children())       # empty table on every execution
    for row in backend.showGrp():
      self.tree.insert('', END, values=row)

  def selectGroupRow(self, event):
    # get row values on selection
    current_item = self.tree.item(self.tree.focus())
    self.grp_id = current_item['values'][0]
    self.prg_id = current_item['values'][1]
    self.trn_no = current_item['values'][2]
    self.day = current_item['values'][3]
    # grp_trn = ' '.join(list(backend.showGrpInfo(self.grp_id)))
    self.t2.config(text = backend.getTrnNameSalary(self.grp_id))
    self.t1.config(text=backend.getPrgName(self.grp_id))

  def fillEntries(self):
    if not self.checkSelectResult:
      return 0
    # insert selected row values (from function selectRow) to entries to new window
    self.grp_id_entry.insert(0, self.grp_id)
    self.prg_id_entry.insert(0, self.prg_id)
    self.trn_no_entry.insert(0, self.trn_no)
    self.day_entry.insert(0, self.day)

  def getEntryValues(self):
    grp_id = self.grp_id_text.get()
    prg_id = self.prg_id_text.get()
    trn_fname = self.trn_no_text.get().split()[0]
    trn_lname = self.trn_no_text.get().split()[1]
    day = self.day_text.get()
    return [grp_id, prg_id, day, trn_fname, trn_lname]

  def insertGrp(self):
    self.grp_id_entry = ''
    self.prg_id_entry = ''
    self.day_entry    = ''
    try:
      entry_values = self.getEntryValues()
      query = backend.insertGrp(entry_values)
      messagebox.showinfo(parent=self.new_window, title='Success', message=query)
      self.viewGrp()        
      self.new_window.destroy()
    except Exception as e:
      messagebox.showerror(parent=self.new_window, title='Error', message=e)

  def updateGrp(self):
    if self.checkSelectResult: 
      try:
        entry_values = self.getEntryValues()
        grp_info = entry_values[:-2]
        trn_no = backend.getTrnNo(entry_values[-2], entry_values[-1])
        grp_info.append(trn_no)
        query = backend.updateGrp(grp_info)
        messagebox.showinfo(parent=self.new_window, title='Success', message=query)
        self.viewGrp()        # update table view
        self.new_window.destroy()
      except Exception as e:
        messagebox.showerror(parent=self.new_window, title='Error', message=e)

  def deleteGrp(self):
    if self.checkSelection(): 
      confirm = messagebox.askyesno(parent=self.master, title='Grup siliniyor', message='Secilen grup silinsin mi?')
      if confirm == True:
        try:
          query = backend.deleteGrp(self.tree.set(self.tree.selection())['1'])      #delete function in backend gets ssn as input
          messagebox.showinfo(parent=self.master, title='Success', message=query)    #print trigger sql notice in messagebox
          self.viewGrp()          # update table view
          return 0
        except Exception as e:
          messagebox.showerror(parent=self.master, title='Error', message=e)

  def openGrpWindow(self, button_id):  
    if button_id==2: # for update pop up window
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
      title('Grup Ekle')
      b1 = Button(self.new_window, text='Ekle', width=20, command=self.insertGrp).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')
    else:
      title('Grup Yenile')
      b1 = Button(self.new_window, text='Yenile', width=20, command=self.updateGrp).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')

    # GROUP ID
    l1 = Label(self.new_window, text='Group ID: ').grid(row=1, column=1, sticky='w')
    self.grp_id_text=StringVar()
    self.grp_id_entry = Entry(self.new_window, textvariable=self.grp_id_text, width=entry_width)
    self.grp_id_entry.grid(row=1, column=2, sticky="nsew") 
    # PROGRAM ID
    l2 = Label(self.new_window, text='Program ID: ').grid(row=2, column=1, sticky='w')
    self.prg_id_text=StringVar()
    self.prg_id_entry = Entry(self.new_window,textvariable=self.prg_id_text,width=entry_width)
    self.prg_id_entry.grid(row=2, column=2, sticky="nsew")
    # TRAINER
    l3 = Label(self.new_window, text='Egitmen No: ').grid(row=3, column=1, sticky='w')
    trainers = backend.getTrnName()
    self.trn_no_text = StringVar(self.new_window)
    self.trn_no_text.set(trainers[0])
    self.trn_no_entry = OptionMenu(self.new_window, self.trn_no_text, trainers[0], *trainers)
    self.trn_no_entry.grid(row=3, column=2, sticky="nsew")
    # DAY OF WEEK
    l4 = Label(self.new_window, text='Gun: ').grid(row=4, column=1, sticky='w')
    self.day_text=StringVar()
    self.day_entry = Entry(self.new_window,textvariable=self.day_text,width=entry_width)
    self.day_entry.grid(row=4, column=2, sticky="nsew")
   