from os import system
import tkinter as tk
from ntpath import basename
from glob import glob
from tkinter.constants import S

class menu:
    def __init__(self, s):
        self.s = s

    def make(self):
        self.s.menubar = tk.Menu(self.s.root)
        #file menu
        self.s.filemenu = tk.Menu(self.s.menubar)
        self.s.filemenu.add_command(label='New file', command=self.s.func.newfile)
        self.s.filemenu.add_command(label='Open file', command=self.s.func.openfile)
        self.s.filemenu.add_command(label='Save file', command=self.s.func.savefile)
        self.s.filemenu.add_command(label='Save as...', command=self.s.func.saveas)
        self.s.filemenu.add_command(label='Delete file', command=self.s.func.deletefile)
        self.s.filemenu.add_separator()
        self.s.filemenu.add_command(label='Quit', command=self.s.root.quit)
        #pref menu
        self.s.prefmenu = tk.Menu(self.s.menubar)
        #font menu
        self.s.fontmenu = tk.Menu(self.s.prefmenu)
        self.s.fontmenu.add_command(label='Change font', command=self.s.func.changefont)
        self.s.fontmenu.add_command(label='Font families', command=self.s.func.fontfamilies)
        self.s.fontmenu.add_command(label='Change font size', command=self.s.func.changefontsize)
        self.s.fontmenu.add_command(label='Change font color', command=self.s.func.changefontcolor)
        #themes menu
        self.s.themesmenu = tk.Menu(self.s.prefmenu)
        for theme in glob(self.s.themesPath + '/*.theme'):
            print(theme)
            self.s.themesmenu.add_command(label=basename(theme), command=lambda: self.s.func.loadTheme(theme))
        self.s.themesmenu.add_command(label='Open themes directory', command=lambda: system('open ' + self.s.themesPath.replace(' ', '\\ ')))
        #add menus to pref menu
        self.s.prefmenu.add_cascade(label='Font', menu=self.s.fontmenu)
        self.s.prefmenu.add_cascade(label='Themes', menu=self.s.themesmenu)
        self.s.prefmenu.add_command(label='Open theme', command=self.s.func.themeload)
        self.s.prefmenu.add_command(label='Save theme', command=self.s.func.themesave)
        self.s.prefmenu.add_command(label='Change background', command=self.s.func.changebg)
        self.s.prefmenu.add_command(label='Change insert color', command=self.s.func.changeic)
        self.s.prefmenu.add_command(label='Reset to default settings', command=self.s.func.resetconfig)
        #window menu
        self.s.winmenu = tk.Menu(self.s.menubar)
        self.s.winmenu.add_command(label='Minimize', accelerator='cmd+m', command=self.s.root.iconify)
        self.s.winmenu.add_command(label='Zoom', command=self.s.func.zoom)
        #text menu
        self.s.textmenu = tk.Menu(self.s.menubar)
        self.s.textmenu.add_command(label='Undo', accelerator='cmd+z', command=self.s.editor.edit_undo)
        self.s.textmenu.add_command(label='Redo', accelerator='cmd+shift+z', command=self.s.editor.edit_redo)
        self.s.textmenu.add_separator()
        self.s.textmenu.add_command(label='Cut', accelerator='cmd+x', command=lambda: self.s.editor.event_generate('<<Cut>>'))
        self.s.textmenu.add_command(label='Copy', accelerator='cmd+c', command=self.s.func.copy)
        self.s.textmenu.add_command(label='Paste', accelerator='cmd+v', command=self.s.func.paste)
        self.s.textmenu.add_command(label='Select all', accelerator='cmd+a', command=lambda: self.s.editor.tag_add('sel', 0.0, tk.END))
        self.s.textmenu.add_separator()
        self.s.textmenu.add_command(label='Clear', command=lambda: self.s.editor.delete(0.0, tk.END))
        self.s.textmenu.add_command(label='Random number', command=self.s.func.randomnum)
        self.s.textmenu.add_command(label='Reverse text', command=self.s.func.reverse)
        self.s.textmenu.add_command(label='Length of text', command=self.s.func.length)
        self.s.textmenu.add_command(label='Word count', command=self.s.func.word_count)
        self.s.textmenu.add_command(label='Convert lowercase', command=self.s.func.lowercase)
        self.s.textmenu.add_command(label='Convert uppercase', command=self.s.func.uppercase)
        self.s.textmenu.add_command(label='Encode base64', command=self.s.func.enc_b64)
        self.s.textmenu.add_command(label='Decode base64', command=self.s.func.dec_b64)
        self.s.textmenu.add_command(label='Encode hex', command=self.s.func.enc_hex)
        self.s.textmenu.add_command(label='Decode hex', command=self.s.func.dec_hex)
        self.s.textmenu.add_command(label='New terminal window', command=self.s.func.terminal)
        
    def add(self):
        #adding menus to window menu
        self.s.menubar.add_cascade(label='File', menu=self.s.filemenu)
        self.s.menubar.add_cascade(label='Text', menu=self.s.textmenu)
        self.s.menubar.add_cascade(label='Preferences', menu=self.s.prefmenu)
        self.s.menubar.add_cascade(label='Window', menu=self.s.winmenu)
        #set menu as menubar
        self.s.root.config(menu=self.s.menubar)