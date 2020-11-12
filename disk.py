import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.simpledialog import askinteger, askstring
from tkinter.messagebox import showerror, askokcancel
from tkinter.colorchooser import askcolor
from tkinter.font import families
from configparser import ConfigParser
from os import path, mkdir, remove
from getpass import getuser

#variables
fs = 12
fc = '#ffffff'
font = 'Menlo'
filename = None
config = ConfigParser()
user = getuser()

#make config file and directory if no directory/file 
if path.isdir('/Users/' + user + '/Library/Application Support/disk') == False:
  mkdir('/Users/' + user + '/Library/Application Support/disk')
if path.isfile('/Users/' + user + '/Library/Application Support/disk/config.ini') == False:
  open('/Users/' + user + '/Library/Application Support/disk/config.ini', mode='w').close()

#functions
def setconfig():
  config.read('/Users/' + user + '/Library/Application Support/disk/config.ini')
  if not config.has_section('settings'):
    config.add_section('settings')
  config.set('settings', 'fontsize', str(fs))
  config.set('settings', 'fontcolor', fc)
  config.set('settings', 'font', font)
  with open('/Users/' + user + '/Library/Application Support/disk/config.ini', 'w') as file:
    config.write(file)

def loadconfig():
  global fs
  global fc
  global font
  config.read('/Users/' + user + '/Library/Application Support/disk/config.ini')
  try:
    fontsize = config.get('settings', 'fontsize')
    fc = config.get('settings', 'fontcolor')
    font = config.get('settings', 'font')
    fs = int(fontsize)
  except:
    setconfig

def openfile():
  global filename
  filename = askopenfile(mode='r')
  if not filename == None:
    try:
      text = filename.read()
      editor.delete(0.0, tk.END)
      editor.insert(0.0, text)
      root.title(filename.name + ' - disk')
    except:
      showerror(title='Error!', message='We cannot read this file, please open another file.')

def deletefile():
  ans = askokcancel('Deleting file', 'Are you sure you want to delete this file?')
  if ans == True and filename != 'Untitled':
    try:
      remove(filename.name)
      newfile()
    except:
      showerror('Error!', 'I do not have enough permission to delete this file!')
  elif filename == 'Untitled':
    showerror('Error!', 'This file is not created yet so you cannot delete this file!')

def changefontsize():
  global fs
  fs = askinteger(title='Changing font size', prompt='Change font size to:')
  if not fs == None:
    editor.config(font=('Menlo', fs))
    setconfig()

def changefontcolor():
  global fc
  color = askcolor()
  if not color == (None, None):
    fc = color[1]
    editor.config(fg=fc)
    setconfig()

def changefont():
  global font
  font = askstring('Choosing font', 'Type font name in prompt.')
  if not font == None:
    for i in families():
      if font == i:
        editor.config(font=(font, fs))
    setconfig()

def savefile():
  global filename
  text = editor.get(0.0, tk.END)
  try:
    f = open(filename.name, "w")
    f.write(text)
    f.close()
  except:
    showerror(title='Error!', message='This file has not been created yet, Please use save as... instead!')

def newfile():
  global filename
  filename = 'Untitled'
  editor.delete(0.0, tk.END)
  root.title(filename + ' - disk')

def saveas():
  filedir = asksaveasfile(mode='w', defaultextension='.txt')
  text = editor.get(0.0, tk.END)
  filedir.write(text)

def fontfamilies():
  window = tk.Tk()
  window.resizable(False, False)
  scrollbar = tk.Scrollbar(window)
  listbox = tk.Listbox(window, yscrollcommand=scrollbar.set)
  scrollbar.config(command=listbox.yview)
  for ele in [*families()]:
    listbox.insert(tk.END, ele)
  scrollbar.pack(side=tk.RIGHT)
  listbox.pack()
  window.title('Font families')
  window.mainloop()

root = tk.Tk()
root.geometry('550x320')
menubar = tk.Menu(root)
#file menu
filemenu = tk.Menu(menubar)
filemenu.add_command(label='New file', command=newfile)
filemenu.add_command(label='Open file', command=openfile)
filemenu.add_command(label='Save file', command=savefile)
filemenu.add_command(label='Save as...', command=saveas)
filemenu.add_command(label='Delete file', command=deletefile)
filemenu.add_separator()
filemenu.add_command(label='Quit', command=root.quit)
#pref menu
prefmenu = tk.Menu(menubar)
#font menu
fontmenu = tk.Menu(prefmenu)
fontmenu.add_command(label='Change font', command=changefont)
fontmenu.add_command(label='Font families', command=fontfamilies)
fontmenu.add_command(label='Change font size', command=changefontsize)
fontmenu.add_command(label='Change font color', command=changefontcolor)
root.config(bg='#333333', menu=menubar)
#add menus to pref menu
prefmenu.add_cascade(label='Font', menu=fontmenu)
#on delete window quit the app
root.protocol('WM_DELETE_WINDOW', root.destroy)
#load configuration
loadconfig()
#widgets
editor = tk.Text(master=root, width=1920, height=1080, bg='#333333', font=(font, fs), highlightbackground='#333333', highlightthickness=0, fg=fc, undo=True, insertbackground='#ffffff')
editor.pack()
#text menu
textmenu = tk.Menu(menubar)
textmenu.add_command(label='Clear', command=lambda: editor.delete(0.0, tk.END))
#adding menus to window menu
menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label='Text', menu=textmenu)
menubar.add_cascade(label='Preferences', menu=prefmenu)
#initalize new file
newfile()
root.title(filename + ' - disk')
root.mainloop()
