import backend
import psycopg2
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox

class Program:
  def __init__(self, master):
    self.master = master
    self.tree_title = Label(master, text='Program Tablosu')
    b_width = 20
    b1 = Button(master, text='Ekle', width=b_width, command=lambda: self.openPrgWindow(1))
    b2 = Button(master, text='Guncelle', width=b_width, command=lambda: [self.openPrgWindow(2), self.fillEntries()])
    b3 = Button(master, text='Sil', width=b_width, command=lambda: self.deletePrg())
    self.buttons = [b1, b2, b3]
    i1 = Label(master, text='Toplam Odenen Ucret: ')
    self.t1 = Label(master, text='')
    i2 = Label(master, text='Bulunan Gruplar: ')
    self.t2 = Label(master, text='')
    self.infos = [i1,self.t1,i2,self.t2]
    # TREEVIEW
    self.tree = Treeview(master, show='headings')
    self.tree['columns'] = ("1", "2", "3", "4", "5") 
    self.tree.heading('#1', text='Program ID')
    self.tree.heading('#2', text='Program Adi')
    self.tree.heading('#3', text='Ucret')
    self.tree.heading('#4', text='Min Egitmen Seviye')
    self.tree.heading('#5', text='Min Ogrenci Seviye')
    self.tree.column('1', width = 60)
    self.tree.column('2', width = 60)
    self.tree.column('3', width = 80)
    self.tree.column('4', width = 40)
    self.tree.column('5', width = 40)
    self.style_tree = Style()
    self.style_tree.configure('Treeview', rowheight=20)
    # on row selection, bind elements in row to content function
    self.tree.bind('<ButtonRelease-1>', self.selectProgramRow)
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
      tree_win[0].grid(row=5, column=1, columnspan=5, rowspan=4, sticky='nsew')
      tree_win[1].grid(row=2, column=1, sticky='sw')
      tree_win[2].grid(row=5, column=6, sticky='ns')
      for i in range(3):
        buttons[i].grid(row=3, column=i+1, sticky='nsew')
      for i in range(4):
        infos[i].grid(row=4, column=i+1, sticky='w')
      
    else:
      for i in range(3):
        buttons[i].grid_remove()
      for i in range(4):
        infos[i].grid_remove()
      tree_win[0].grid_remove()
      tree_win[1].grid_remove()
      tree_win[2].grid_remove()
    self.hidden = not self.hidden

  # ******************* CHECK CONDITIONS ***************** 
  def checkSelection(self):
    self.checkSelectResult = True
    if len(self.tree.set(self.tree.selection()))==0:
      messagebox.showerror(parent=self.master, title='Program yok', message='Program seciniz')
      self.checkSelectResult = False
    return self.checkSelectResult

  # ******************* VIEW TABLE ************************
  def viewPrg(self):
    self.tree.delete(*self.tree.get_children())       # empty table on every execution
    for row in backend.showPrg():
      self.tree.insert('', END, values=row)

  def selectProgramRow(self, event):
    current_item = self.tree.item(self.tree.focus())
    self.prg_id = current_item['values'][0]
    self.prg_name = current_item['values'][1]
    self.price = current_item['values'][2]
    self.min_trn_level = current_item['values'][3]
    self.min_std_level = current_item['values'][4]
    prg_grp = [str(i) for i in backend.showPrgInfo(self.prg_id)]
    self.t2.config(text = prg_grp)
    self.t1.config(text = backend.getTotalPrice(self.prg_id))

  def fillEntries(self):
    if not self.checkSelectResult:
      return 0
    self.prg_id_entry.insert(0, self.prg_id)
    self.prg_name_entry.insert(0, self.prg_name)
    self.price_entry.insert(0, self.price)

  def getEntryValues(self):
    prg_id = self.prg_id_text.get()
    prg_name = self.prg_name_text.get()
    price = self.price_text.get()
    min_trn_level = self.min_trn_level_text.get()
    min_std_level = self.min_std_level_text.get()
    return [prg_id, prg_name, min_std_level, min_trn_level, price]

  def insertPrg(self):
    self.prg_id_entry        = ''
    self.prg_name_entry      = ''
    self.price_entry         = ''
    try:
      entry_values = self.getEntryValues()
      query = backend.insertPrg(entry_values)
      messagebox.showinfo(parent=self.new_window,title='Success', message=query)
      self.viewPrg()        
      self.new_window.destroy()
    except Exception as e:
      messagebox.showerror(parent=self.new_window,title='Error', message=e)

  def updatePrg(self):
    if self.checkSelectResult: 
      try:
        entry_values = self.getEntryValues()
        query = backend.updatePrg(entry_values)
        messagebox.showinfo(parent=self.new_window,title='Success', message=query)
        self.viewPrg()      
        self.new_window.destroy()
      except Exception as e:
        messagebox.showerror(parent=self.new_window,title='Error', message=e)
  
  def deletePrg(self):
    if self.checkSelection(): 
      confirm = messagebox.askyesno(parent=self.master, title='Program siliniyor', message='Secilen program silinsin mi?')
      if confirm == True:
        try:
          query = backend.deletePrg(self.tree.set(self.tree.selection())['1'])      #delete function in backend gets ssn as input
          messagebox.showinfo(parent=self.master, title='Success', message=query)    #print trigger sql notice in messagebox
          self.viewPrg()          # update table view
          return 0
        except Exception as e:
          messagebox.showerror(parent=self.master, title='Error', message=e)

  # ********************** OPEN NEW WINDOW DOR INSERTION AND UPDATE *****************************
  def openPrgWindow(self, button_id): 
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
      title('Program Ekle')
      b1 = Button(self.new_window, text='Ekle', width=20, command=self.insertPrg).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')
    else:
      title('Program Yenile')
      b1 = Button(self.new_window, text='Yenile', width=20, command=self.updatePrg).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')

    l1 = Label(self.new_window, text='Program ID: ').grid(row=1, column=1, sticky='w')
    self.prg_id_text=StringVar()
    self.prg_id_entry = Entry(self.new_window, textvariable=self.prg_id_text, width=entry_width)
    self.prg_id_entry.grid(row=1, column=2, sticky="nsew") 
    l2 = Label(self.new_window, text='Program Ismi: ').grid(row=2, column=1, sticky='w')
    self.prg_name_text=StringVar()
    self.prg_name_entry = Entry(self.new_window,textvariable=self.prg_name_text,width=entry_width)
    self.prg_name_entry.grid(row=2, column=2, sticky="nsew")

    l3 = Label(self.new_window, text='Ucret: ').grid(row=3, column=1, sticky='w')
    self.price_text=StringVar(self.new_window)
    self.price_entry = Entry(self.new_window,textvariable=self.price_text, width=entry_width)
    self.price_entry.grid(row=3, column=2, sticky="nsew")
    
    trainers = backend.getTrnLevel()
    l4 = Label(self.new_window, text='Min Egitmen Seviye: ').grid(row=4, column=1, sticky='w')
    self.min_trn_level_text  = StringVar(self.new_window)
    self.min_trn_level_text.set(trainers[0])
    self.min_trn_level_entry = OptionMenu(self.new_window, self.min_trn_level_text, trainers[0], *trainers)
    self.min_trn_level_entry.grid(row=4, column=2, sticky="nsew")
    
    students = backend.getStdLevel()
    l5 = Label(self.new_window, text='Min Ogrenci Seviye: ').grid(row=5, column=1, sticky='w')
    self.min_std_level_text  = StringVar(self.new_window)
    self.min_std_level_text.set(students[0])
    self.min_std_level_entry = OptionMenu(self.new_window, self.min_std_level_text, students[0], *students)
    self.min_std_level_entry.grid(row=5, column=2, sticky="nsew")
    
   