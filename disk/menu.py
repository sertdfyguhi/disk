from os import system
import sys
import tkinter as tk
from ntpath import basename
from glob import glob

def menu(self):
  self.menubar = tk.Menu(self.root)
  #file menu
  self.filemenu = tk.Menu(self.menubar)
  self.filemenu.add_command(label='New file', command=self.func.newfile)
  self.filemenu.add_command(label='Open file', command=self.func.openfile)
  self.filemenu.add_command(label='Save file', command=self.func.savefile)
  self.filemenu.add_command(label='Save as...', command=self.func.saveas)
  self.filemenu.add_command(label='Delete file', command=self.func.deletefile)
  self.filemenu.add_separator()
  self.filemenu.add_command(label='Quit', command=self.root.quit)
  #pref menu
  self.prefmenu = tk.Menu(self.menubar)
  #font menu
  self.fontmenu = tk.Menu(self.prefmenu)
  self.fontmenu.add_command(label='Change font', command=self.func.changefont)
  self.fontmenu.add_command(label='Font families', command=self.func.fontfamilies)
  self.fontmenu.add_command(label='Change font size', command=self.func.changefontsize)
  self.fontmenu.add_command(label='Change font color', command=self.func.changefontcolor)
  #themes menu
  self.themesmenu = tk.Menu(self.prefmenu)
  for theme in glob(self.themesPath + '/*.theme'):
    print(theme)
    self.themesmenu.add_command(label=basename(theme), command=lambda: self.func.loadTheme(theme))
  self.themesmenu.add_command(label='Open themes directory', command=lambda: system('open ' + self.themesPath.replace(' ', '\\ ')))
  #add menus to pref menu
  self.prefmenu.add_cascade(label='Font', menu=self.fontmenu)
  self.prefmenu.add_cascade(label='Themes', menu=self.themesmenu)
  self.prefmenu.add_command(label='Open theme', command=self.func.themeload)
  self.prefmenu.add_command(label='Save theme', command=self.func.themesave)
  self.prefmenu.add_command(label='Change background', command=self.func.changebg)
  self.prefmenu.add_command(label='Change insert color', command=self.func.changeic)
  self.prefmenu.add_command(label='Reset to default settings', command=self.func.resetconfig)
  #window menu
  self.winmenu = tk.Menu(self.menubar)
  self.winmenu.add_command(label='Minimize', accelerator='cmd+m', command=self.root.iconify)
  self.winmenu.add_command(label='Zoom', command=self.func.zoom)
  #text menu
  self.textmenu = tk.Menu(self.menubar)
  self.textmenu.add_command(label='Undo', accelerator='cmd+z', command=self.editor.edit_undo)
  self.textmenu.add_command(label='Redo', accelerator='cmd+shift+z', command=self.editor.edit_redo)
  self.textmenu.add_separator()
  self.textmenu.add_command(label='Cut', accelerator='cmd+x', command=lambda: self.editor.event_generate('<<Cut>>'))
  self.textmenu.add_command(label='Copy', accelerator='cmd+c', command=self.func.copy)
  self.textmenu.add_command(label='Paste', accelerator='cmd+v', command=self.func.paste)
  self.textmenu.add_command(label='Select all', accelerator='cmd+a', command=lambda: self.editor.tag_add('sel', 0.0, tk.END))
  self.textmenu.add_separator()
  self.textmenu.add_command(label='Clear', command=lambda: self.editor.delete(0.0, tk.END))
  self.textmenu.add_command(label='Random number', command=self.func.randomnum)
  self.textmenu.add_command(label='Reverse text', command=self.func.reverse)
  self.textmenu.add_command(label='Length of text', command=self.func.length)
  self.textmenu.add_command(label='Convert lowercase', command=self.func.lowercase)
  self.textmenu.add_command(label='Convert uppercase', command=self.func.uppercase)
  self.textmenu.add_command(label='New terminal window', command=self.func.terminal)
  #adding menus to window menu
  self.menubar.add_cascade(label='File', menu=self.filemenu)
  self.menubar.add_cascade(label='Text', menu=self.textmenu)
  self.menubar.add_cascade(label='Preferences', menu=self.prefmenu)
  self.menubar.add_cascade(label='Window', menu=self.winmenu)
  #set menu as menubar
  self.root.config(menu=self.menubar)
