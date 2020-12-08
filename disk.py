import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.simpledialog import askinteger, askstring
from tkinter.messagebox import askyesno, showerror, askokcancel, showinfo
from tkinter.colorchooser import askcolor
from tkinter.font import families
from configparser import ConfigParser
from os import path, mkdir, remove, system
from random import randint
from sys import platform
from appdirs import user_data_dir

#variables
ic = '#fff'
fs = 12
fc = '#ffffff'
bg = '#333333'
font = 'Menlo'
zoomed = False
filename = None
config = ConfigParser()

#make config file and directory if no directory/file 
if not path.isdir(user_data_dir('disk', 'sertdfyguhi')):
  mkdir(user_data_dir('disk', 'sertdfyguhi'))
if not path.isfile(user_data_dir('disk', 'sertdfyguhi') + '/config.ini'):
  open(user_data_dir('disk', 'sertdfyguhi') + '/config.ini', mode='w').close()

#functions
def setconfig():
  config.read(user_data_dir('disk', 'sertdfyguhi') + '/config.ini')
  if not config.has_section('settings'):
    config.add_section('settings')
  config.set('settings', 'fontsize', str(fs))
  config.set('settings', 'fontcolor', fc)
  config.set('settings', 'font', font)
  config.set('settings', 'bg', bg)
  config.set('settings', 'ic', ic)
  with open(user_data_dir('disk', 'sertdfyguhi') + '/config.ini', 'w') as file:
    config.write(file)

def loadconfig():
  global fs
  global fc
  global font
  global bg
  global ic
  config.read(user_data_dir('disk', 'sertdfyguhi') + '/config.ini')
  try:
    fontsize = config.get('settings', 'fontsize')
    fc = config.get('settings', 'fontcolor')
    font = config.get('settings', 'font')
    bg = config.get('settings', 'bg')
    ic = config.get('settings', 'ic')
    fs = int(fontsize)
  except:
    setconfig()

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
    editor.config(font=(font, fs))
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

def resetconfig():
  global fc
  global fs
  global font
  global bg
  yn = askyesno('Reset to default settings', 'Are you sure you want to reset your settings?')
  if yn == True:
    fc = '#fff'
    fs = '12'
    font = 'Menlo'
    bg = '#333333'
    editor.config(font=(font, fs), fg=fc, bg=bg)
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
  global filename
  try:
    filedir = asksaveasfile(mode='w', defaultextension='.txt')
    text = editor.get(0.0, tk.END)
    filedir.write(text)
    file = open(filedir.name, 'r')
    editor.delete(0.0, tk.END)
    editor.insert(0.0, file.read())
    filename = file
    root.title(filename.name + ' - disk')
  except:
    pass

def fontfamilies():
  window = tk.Tk()
  window.resizable(False, False)
  listbox = tk.Listbox(window)
  for family in [*families()]:
    listbox.insert(tk.END, family)
  listbox.pack()
  window.title('Font families')
  window.mainloop()

def randomnum():
  window = tk.Tk()

  def rannum():
    try:
      e1 = int(entry1.get())
      e2 = int(entry2.get())
      editor.insert(tk.END, randint(e1, e2))
      window.destroy()
    except:
      showerror('Error!', 'Min or max cannot be empty, any alphabet or symbol, it can only be a number.')

  entry1 = tk.Entry(window)
  entry1label = tk.Label(window, text='Min: ')
  entry2 = tk.Entry(window)
  entry2label = tk.Label(window, text='Max: ')
  ok = tk.Button(window, text='OK', command=rannum)
  cancel = tk.Button(window, text='Cancel', command=window.destroy)
  entry1label.pack(side=tk.LEFT)
  entry1.pack(side=tk.LEFT)
  entry2label.pack(side=tk.LEFT)
  entry2.pack(side=tk.LEFT)
  ok.pack(side=tk.LEFT)
  cancel.pack(side=tk.LEFT)
  window.resizable(False, False)
  window.title('Random number')
  window.mainloop()

def changebg():
  global bg
  color = askcolor()
  if not color == (None, None):
    bg = color[1]
    editor.config(bg=bg)
    setconfig()

def copy():
  try:
    selected = editor.selection_get()
    root.clipboard_clear()
    root.clipboard_append(selected)
  except:
    pass
  root.update()

def changeic():
  global ic
  color = askcolor()
  if not color == (None, None):
    ic = color[1]
    editor.config(insertbackground=ic)
    setconfig()

def paste():
  try:
    clipboard = root.clipboard_get()
    editor.insert(tk.END, clipboard)
  except:
    pass

def zoom():
  global zoomed
  if zoomed == False:
    zoomed = True
    root.state('zoomed')
  else:
    zoomed = False
    root.state('normal')

def lowercase():
  text = editor.get(0.0, tk.END)
  editor.delete(0.0, tk.END)
  editor.insert(0.0, text.lower())

def uppercase():
  text = editor.get(0.0, tk.END)
  editor.delete(0.0, tk.END)
  editor.insert(0.0, text.upper())

def reverse():
  rtext = editor.get(0.0, tk.END)[::-1]
  editor.delete(0.0, tk.END)
  editor.insert(0.0, rtext.replace('\n', '', 1))

def length():
  showinfo('Length of text', len(editor.get(1.0, tk.END)))

def terminal():
  if platform == 'darwin':
    system('open -a Terminal -n')
  elif platform == 'win32':
    system('start cmd')
  elif platform == 'linux':
    system('gnome-terminal')


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
#window menu
winmenu = tk.Menu(menubar)
winmenu.add_command(label='Minimize', accelerator='cmd+m', command=root.iconify)
winmenu.add_command(label='Zoom', command=zoom)
#add menus to pref menu
prefmenu.add_cascade(label='Font', menu=fontmenu)
prefmenu.add_command(label='Change background', command=changebg)
prefmenu.add_command(label='Chnage insert color', command=changeic)
prefmenu.add_command(label='Reset to default settings', command=resetconfig)
#load configuration
loadconfig()
#widgets
editor = tk.Text(master=root, width=1920, height=1080, bg=bg, font=(font, fs), highlightthickness=0, fg=fc, undo=True, insertbackground=ic)
editor.pack()
#text menu
textmenu = tk.Menu(menubar)
textmenu.add_command(label='Undo', accelerator='cmd+z', command=editor.edit_undo)
textmenu.add_command(label='Redo', accelerator='cmd+shift+z', command=editor.edit_redo)
textmenu.add_separator()
textmenu.add_command(label='Cut', accelerator='cmd+x', command=lambda: editor.event_generate('<<Cut>>'))
textmenu.add_command(label='Copy', accelerator='cmd+c', command=copy)
textmenu.add_command(label='Paste', accelerator='cmd+v', command=paste)
textmenu.add_command(label='Select all', accelerator='cmd+a', command=lambda: editor.tag_add('sel', 0.0, tk.END))
textmenu.add_separator()
textmenu.add_command(label='Clear', command=lambda: editor.delete(0.0, tk.END))
textmenu.add_command(label='Random number', command=randomnum)
textmenu.add_command(label='Reverse text', command=reverse)
textmenu.add_command(label='Length of text', command=length)
textmenu.add_command(label='Convert lowercase', command=lowercase)
textmenu.add_command(label='Convert uppercase', command=uppercase)
textmenu.add_command(label='New terminal window', command=terminal)
#adding menus to window menu
menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label='Text', menu=textmenu)
menubar.add_cascade(label='Preferences', menu=prefmenu)
menubar.add_cascade(label='Window', menu=winmenu)
#initalize new file
newfile()
root.title(filename + ' - disk')
root.mainloop()
