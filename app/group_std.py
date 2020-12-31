import backend
import psycopg2
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter import messagebox

class GroupStd:
  def __init__(self, master):
    self.master = master
    self.tree_title = Label(master, text='Grup Ogrenci Tablosu')
    master.grid_rowconfigure(2, minsize=40)  
    master.grid_rowconfigure(4, minsize=30) 
    b_width = 20
    b1 = Button(master, text='Ekle', width=b_width, command=lambda: self.openGrpStdWindow(1))
    b2 = Button(master, text='Guncelle', width=b_width, command=lambda: self.openGrpStdWindow(2))
    b3 = Button(master, text='Sil', width=b_width, command=lambda: self.deleteGrpStd())
    b4 = Button(master, text='Grupsuz Ogrenciler', width=b_width, command=lambda: self.noGrpStd())
    self.buttons = [b1, b2, b3, b4]
    i1 = Label(master, text='Ogrenci Sayisi: ')
    self.t1 = Label(master, text='')
    i2 = Label(master, text='Ogrenci: ')
    self.t2 = Label(master, text='')
    self.labels = [i1, i2]
    self.infos = [self.t1,self.t2]
    # TREEVIEW
    self.tree_title = Label(master, text='Gruplardaki Ogrenciler')
    self.tree = Treeview(master, show='headings')
    self.tree['columns'] = ("1", "2") 
    self.tree.heading('#1', text='Grup ID')
    self.tree.heading('#2', text='Ogrenci No')
    self.tree.column('1', width = 60)
    self.tree.column('2', width = 60)
    self.style_tree = Style()
    self.style_tree.configure('Treeview', rowheight=20)
    self.tree.bind('<ButtonRelease-1>', self.selectGrpStdRow)
    self.sb = Scrollbar(master, orient ='vertical', command = self.tree.yview) 
    self.tree.configure(yscrollcommand = self.sb.set)
    self.tree_window = [self.tree, self.tree_title, self.sb]
    

    self.tree2_title = Label(master, text='Grupsuz Ogrenciler')
    self.tree2 = Treeview(master, show='headings')
    self.tree2['columns'] = ("1", "2", "3")
    self.tree2.heading('#1', text='Ad')
    self.tree2.heading('#2', text='Soyad')
    self.tree2.heading('#3', text='Ogrenci No')
    self.tree2.column('1', width = 40)
    self.tree2.column('2', width = 40)
    self.tree2.column('3', width = 60)
    self.style_tree2 = Style()
    self.style_tree2.configure('Treeview', rowheight=20)
    self.sb2 = Scrollbar(master, orient ='vertical', command = self.tree2.yview) 
    self.tree2.configure(yscrollcommand = self.sb2.set)
    self.tree2_window = [self.tree2, self.tree2_title, self.sb2]

    # TOGGLE HIDE/ REVEAL
    self.hidden = True

  def hide(self):
    self.hidden = False
    self.toggle(self.buttons, self.tree_window, self.tree2_window, self.infos, self.labels)

  def toggle(self, buttons, tree_win, tree2_win, infos, labels):
    if self.hidden:
      tree_win[0].grid(row=7, column=1, columnspan=2, rowspan=4, sticky='nsew')
      tree_win[1].grid(row=6, column=1, sticky='sw')
      self.master.grid_rowconfigure(6, minsize=30) 
      tree_win[2].grid(row=7, column=3, sticky='nsw')
      tree2_win[0].grid(row=7, column=4, columnspan=2, rowspan=4, sticky='nsew')
      tree2_win[1].grid(row=6, column=4, sticky='sw')
      tree2_win[2].grid(row=7, column=6, sticky='nsw')
      for i in range(4):
        buttons[i].grid(row=3, column=i+1, sticky='nsew')
      for i in range(2):
        infos[i].grid(row=i+4, column=2, sticky='w')
        labels[i].grid(row=i+4, column=1, sticky='w')
    else:
      for i in range(4):
        buttons[i].grid_remove()
      for i in range(2):
        infos[i].grid_remove()
        labels[i].grid_remove()
      tree_win[0].grid_remove()
      tree_win[1].grid_remove()
      tree_win[2].grid_remove()
      tree2_win[0].grid_remove()
      tree2_win[1].grid_remove()
      tree2_win[2].grid_remove()
    self.hidden = not self.hidden


  # ******************* CHECK CONDITIONS ***************** 
  def checkSelection(self):
    self.checkSelectResult = True
    if len(self.tree.set(self.tree.selection()))==0:
      messagebox.showerror(parent=self.master, title='Grup yok', message='Grup seciniz')
      self.checkSelectResult = False
    return self.checkSelectResult

  # ******************* VIEW TABLE ************************
  def viewGrpStd(self):
    self.tree.delete(*self.tree.get_children())       # empty table on every execution
    for row in backend.showGrpStd():
      self.tree.insert('', END, values=row)

  def noGrpStd(self):
    self.tree2.delete(*self.tree2.get_children())       # empty table on every execution
    for row in backend.noGrpStd():
      self.tree2.insert('', END, values=row)

  def selectGrpStdRow(self, event):
    # get row values on selection
    current_item = self.tree.item(self.tree.focus())
    self.grp_id = current_item['values'][0]
    self.std_no = current_item['values'][1]
    std_count = backend.getStdCount(self.grp_id)
    self.std_name  = ' '.join(list(backend.getStdName(self.std_no)))
    self.t1.config(text=std_count)
    self.t2.config(text=self.std_name)
    
  def getEntryValues(self):
    grp_id = self.grp_text.get()
    std_no = self.std_text.get()
    return [grp_id, std_no]
  
  def insertGrpStd(self):
    try:
      entry_values = self.getEntryValues()
      query = backend.insertGrpStd(entry_values)
      messagebox.showinfo(parent=self.new_window, title='Success', message=query)
      self.viewGrpStd()        
      self.new_window.destroy()
    except Exception as e:
      messagebox.showerror(parent=self.new_window, title='Error', message=e)

  def updateGrpStd(self):
    if self.checkSelectResult: 
      try:
        entry_values = self.getEntryValues()
        entry_values.append(self.grp_id)
        query = backend.updateGrpStd(entry_values)
        messagebox.showinfo(parent=self.new_window, title='Success', message=query)
        self.viewGrpStd()        # update table view
        self.new_window.destroy()
      except Exception as e:
        messagebox.showerror(parent=self.new_window, title='Error', message=e)

  def deleteGrpStd(self):
    if self.checkSelection(): 
      confirm = messagebox.askyesno(parent=self.master, title='Grup siliniyor', message='Secilen grup silinsin mi?')
      if confirm == True:
        try:
          query = backend.deleteGrpStd(self.tree.set(self.tree.selection())['1'])      #delete function in backend gets ssn as input
          messagebox.showinfo(parent=self.master, title='Success', message=query)    #print trigger sql notice in messagebox
          self.viewGrpStd()          # update table view
          return 0
        except Exception as e:
          messagebox.showerror(parent=self.master, title='Error', message=e)

  def openGrpStdWindow(self, button_id):  
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
      title('Gruba Ogrenci Ekle')
      b1 = Button(self.new_window, text='Ekle', width=20, command=self.insertGrpStd).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')
      l1 = Label(self.new_window, text='Seviyedeki Ogrenciler: ').grid(row=3, column=1, sticky='w')
      def stdInfo(s):
        # update students option menu based on what is selected in level option
        self.std = backend.getAllStdInfo(self.level_text.get())
        self.std_text = StringVar(self.new_window)
        self.std_text.set(self.std[0]) # default value
        self.std_entry = OptionMenu(self.new_window, self.std_text, self.std[0], *self.std)
        self.std_entry.grid(row=3, column=2, sticky="nsew")

      l0 = Label(self.new_window, text='Seviye seciniz: ').grid(row=2, column=1, sticky='w')
      level = backend.getStdLevel()
      self.level_text = StringVar(self.new_window)
      self.level_text.set('Seciniz') # default value
      self.level_entry = OptionMenu(self.new_window, self.level_text, 'Seciniz', *level, command=stdInfo)
      self.level_entry.grid(row=2, column=2, sticky="nsew")
      
      l2 = Label(self.new_window, text='Grup seciniz: ').grid(row=4, column=1, sticky='w')
      group_id = backend.getAllGrpId()
      self.grp_text = StringVar(self.new_window)
      self.grp_text.set('Seciniz') # default value
      self.grp_entry = OptionMenu(self.new_window, self.grp_text, 'Seciniz', *group_id)
      self.grp_entry.grid(row=4, column=2, sticky="nsew")
    else:
      title('Grup Ogrenci Yenile')
      b1 = Button(self.new_window, text='Yenile', width=20, command=self.updateGrpStd).grid(row=7, column=1, sticky='nsew')
      b2 = Button(self.new_window, text='Iptal', width=20, command=self.new_window.destroy).grid(row=7, column=2, sticky='nsew')
      
      l1 = Label(self.new_window, text='Ogrenci: ').grid(row=3, column=1, sticky='w')
      self.std = backend.getAllStd()
      self.std_text = StringVar(self.new_window)
      self.std_text.set(self.std_name) # default value
      self.std_entry = OptionMenu(self.new_window, self.std_text, self.std_name, *self.std)
      self.std_entry.grid(row=3, column=2, sticky="nsew")
      
      l2 = Label(self.new_window, text='Grup: ').grid(row=4, column=1, sticky='w')
      group_id = backend.getAllGrpId()
      self.grp_text = StringVar(self.new_window)
      self.grp_text.set(self.grp_id) # default value
      self.grp_entry = OptionMenu(self.new_window, self.grp_text, self.grp_id,  *group_id)
      self.grp_entry.grid(row=4, column=2, sticky="nsew")
  