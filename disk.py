import tkinter as tk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
from configparser import ConfigParser
import os
import getpass

#variables
fs = 12
fc = '#ffffff'
filename = None
config = ConfigParser()
user = getpass.getuser()

#make config file and directory if no directory/file 
if os.path.isdir('/Users/' + user + '/Library/Application Support/disk') == False:
  os.mkdir('/Users/' + user + '/Library/Application Support/disk')
if os.path.isfile('/Users/' + user + '/Library/Application Support/disk/config.ini') == False:
  open('/Users/' + user + '/Library/Application Support/disk/config.ini', mode='w').close()

#functions
def setconfig():
  config.read('/Users/' + user + '/Library/Application Support/disk/config.ini')
  if not config.has_section('settings'):
    config.add_section('settings')
  config.set('settings', 'fontsize', str(fs))
  config.set('settings', 'fontcolor', fc)
  with open('/Users/' + user + '/Library/Application Support/disk/config.ini', 'w') as file:
    config.write(file)

def loadconfig():
  global fs
  global fc
  config.read('/Users/' + user + '/Library/Application Support/disk/config.ini')
  try:
    fontsize = config.get('settings', 'fontsize')
    fontcolor = config.get('settings', 'fontcolor')
    fs = int(fontsize)
    fc = fontcolor
  except:
    setconfig

def configmenu():
  window = tk.Tk()
  window.title('Preferences')
  window.resizable(False, False)
  window.geometry('500x400')
  cfs = tk.Button(window, text='Change font size', command=changefontsize)
  cfc = tk.Button(window, text='Change font color', command=changefontcolor)
  cfc.pack(padx=100, pady=30)
  cfs.pack(padx=100, pady=30)
  window.mainloop()

def openfile():
  global filename
  filename = fd.askopenfile(mode='r')
  if not filename == None:
    try:
      text = filename.read()
      editor.delete(0.0, tk.END)
      editor.insert(0.0, text)
      root.title(filename.name + ' - disk')
    except:
      mb.showerror(title='Error!', message='We cannot read this file, please open another file.')

def deletefile():
  ans = mb.askokcancel('Deleting file', 'Are you sure you want to delete this file?')
  if ans == True and filename != 'Untitled':
    os.remove(filename.name)
    editor.delete(0.0, tk.END)
    newfile
  elif filename == 'Untitled':
    mb.showerror('Error!', 'This file is not created yet so you cannot delete this file!')

def changefontsize():
  global fs
  fs = sd.askinteger(title='Changing font size', prompt='Change font size to:')
  editor.config(font=('Menlo', fs))
  setconfig()

def changefontcolor():
  global fc
  color = cc.askcolor()
  fc = color[1]
  editor.config(fg=fc)
  setconfig()

def savefile():
  global filename
  text = editor.get(0.0, tk.END)
  try:
    f = open(filename.name, "w")
    f.write(text)
    f.close()
  except:
    mb.showerror(title='Error!', message='This file has not been created yet, Please use save as... instead!')

def newfile():
  global filename
  filename = 'Untitled'
  editor.delete(0.0, tk.END)
  root.title(filename + ' - disk')

def saveas():
  filedir = fd.asksaveasfile(mode='w', defaultextension='.txt')
  text = editor.get(0.0, tk.END)
  filedir.write(text)

root = tk.Tk()
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
#adding menus to window menu
menubar.add_cascade(label='File', menu=filemenu)
root.config(bg='#333333', menu=menubar)
#set preferences menu
root.createcommand('::tk::mac::ShowPreferences', configmenu)
#on delete window quit the app
root.protocol('WM_DELETE_WINDOW', root.destroy)
#load configuration
loadconfig()
#widgets
editor = tk.Text(master=root, width=1920, height=1080, bg='#333333', font=('Menlo', fs), highlightbackground='#333333', highlightthickness=0, fg=fc, undo=True, insertbackground='#ffffff')
editor.pack()
#initalize new file
newfile()
root.title(filename + ' - disk')
root.mainloop()
