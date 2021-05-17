from sys import platform
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfile, askopenfilename, asksaveasfile
from tkinter.simpledialog import askinteger, askstring
from tkinter.messagebox import askyesno, showerror, askokcancel, showinfo
from tkinter.colorchooser import askcolor
from tkinter.font import families
from os import remove, system
from random import randint
from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify

class functions:
    def __init__(self, s):
        self.s = s

    def _replace_all(self, text):
        self.s.editor.delete(0.0, tk.END)
        self.s.editor.insert(0.0, text)

    def setconfig(self):
        self.s.config.read(self.s.configPath + '/config.ini')
        if not self.s.config.has_section('settings'):
            self.s.config.add_section('settings')
        self.s.config.set('settings', 'fontsize', str(self.s.fs))
        self.s.config.set('settings', 'fontcolor', self.s.fc)
        self.s.config.set('settings', 'font', self.s.font)
        self.s.config.set('settings', 'bg', self.s.bg)
        self.s.config.set('settings', 'ic', self.s.ic)
        with open(self.s.configPath + '/config.ini', 'w') as file:
            self.s.config.write(file)

    def loadconfig(self):
        self.s.config.read(self.s.configPath + '/config.ini')
        try:
            fontsize = self.s.config.get('settings', 'fontsize')
            self.s.fc = self.s.config.get('settings', 'fontcolor')
            self.s.font = self.s.config.get('settings', 'font')
            self.s.bg = self.s.config.get('settings', 'bg')
            self.s.ic = self.s.config.get('settings', 'ic')
            self.s.fs = int(fontsize)
        except:
            self.setconfig()

    def loadTheme(self, path):
        try:
            self.s.config.read(path)
            fontsize = self.s.config.get('settings', 'fontsize') or self.s.fs
            self.s.fc = self.s.config.get('settings', 'fontcolor') or self.s.fc
            self.s.font = self.s.config.get('settings', 'font') or self.s.font
            self.s.bg = self.s.config.get('settings', 'bg') or self.s.bg
            self.s.ic = self.s.config.get('settings', 'ic') or self.s.ic
            self.s.fs = int(fontsize)
            self.s.editor.config(bg=self.s.bg, font=(self.s.font, self.s.fs), fg=self.s.fc, insertbackground=self.s.ic)
            self.setconfig()
        except:
            showerror('Oops.. Something went wrong while loading this theme.')

    def saveTheme(self, path, name):
        try:
            themePath = path + '/' + name + '.theme'
            f = open(themePath, 'w')
            self.s.config.read(path)
            self.s.config.set('settings', 'fontsize', str(self.s.fs))
            self.s.config.set('settings', 'fontcolor', self.s.fc)
            self.s.config.set('settings', 'font', self.s.font)
            self.s.config.set('settings', 'bg', self.s.bg)
            self.s.config.set('settings', 'ic', self.s.ic)
            self.s.config.write(f)
            system('open ' + themePath)
        except:
            showerror('Oops.. Something went wrong while saving this theme.')

    def themeload(self):
        f = askopenfilename()
        self.loadTheme(f)

    def themesave(self):
        d = askdirectory()
        name = askstring('Saving theme', 'Please choose a name for your theme.')
        self.saveTheme(d, name)

    def openfile(self):
        self.s.filename = askopenfile(mode='r')
        if not self.s.filename == None:
            try:
                text = self.s.filename.read()
                self._replace_all(text)
                self.s.root.title(self.s.filename.name + ' - disk')
            except:
                showerror(title='Error!', message='We cannot read this file, please open another file.')

    def deletefile(self):
        ans = askokcancel('Deleting file', 'Are you sure you want to delete this file?')
        if ans == True and self.s.filename != 'Untitled':
            try:
                remove(self.s.filename.name)
                self.newfile()
            except:
                showerror('Error!', 'I do not have enough permission to delete this file!')
        elif self.s.filename == 'Untitled':
            showerror('Error!', 'This file is not created yet so you cannot delete this file!')

    def changefontsize(self):
        self.s.fs = askinteger(title='Changing font size', prompt='Change font size to:')
        if not self.s.fs == None:
            self.s.editor.config(font=(self.s.font, self.s.fs))
            self.setconfig()

    def changefontcolor(self):
        color = askcolor()
        if not color == (None, None):
            self.s.fc = color[1]
            self.s.editor.config(fg=self.s.fc)
            self.setconfig()

    def changefont(self):
        f = askstring('Choosing font', 'Type font name in prompt. (It is case-sensitive.)')
        if not f == None:
            if f in families():
                self.s.font = f
                self.s.editor.config(font=(self.s.font, self.s.fs))
                self.setconfig()

    def resetconfig(self):
        yn = askyesno('Reset to default settings', 'Are you sure you want to reset your settings?')
        if yn == True:
            self.s.ic = '#fff'
            self.s.fs = 12
            self.s.fc = '#ffffff'
            self.s.bg = '#333333'
            self.s.font = 'Menlo'
            self.s.editor.config(font=(self.s.font, self.s.fs), fg=self.s.fc, bg=self.s.bg, insertbackground=self.s.ic)
            self.setconfig()

    def savefile(self):
        text = self.s.editor.get(0.0, tk.END)
        try:
            f = open(self.s.filename.name, "w")
            f.write(text)
            f.close()
        except:
            showerror(title='Error!', message='This file has not been created yet, Please use save as... instead!')

    def newfile(self):
        self.s.filename = 'Untitled'
        self.s.editor.delete(0.0, tk.END)
        self.s.root.title(self.s.filename + ' - disk')

    def saveas(self):
        try:
            filedir = asksaveasfile(mode='w', defaultextension='.txt')
            text = self.s.editor.get(0.0, tk.END)
            filedir.write(text)
            file = open(filedir.name, 'r')
            self._replace_all(file.read())
            self.s.filename = file
            self.s.root.title(self.s.filename.name + ' - disk')
        except Exception as e:
            showerror('Error!', 'Something went wrong while trying to save! \'' + str(e) + '\'')

    def fontfamilies(self):
        window = tk.Tk()
        window.resizable(False, False)
        listbox = tk.Listbox(window)
        for family in [*families()]:
            listbox.insert(tk.END, family)
        listbox.pack()
        window.title('Font families')
        window.mainloop()

    def randomnum(self):
        window = tk.Tk()

        def rannum():
            try:
                e1 = int(entry1.get())
                e2 = int(entry2.get())
                self.s.editor.insert(tk.END, randint(e1, e2))
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

    def changebg(self):
        color = askcolor()
        if not color == (None, None):
            self.s.bg = color[1]
            self.s.editor.config(bg=self.s.bg)
            self.setconfig()

    def copy(self):
        try:
            selected = self.s.editor.selection_get()
            self.s.root.clipboard_clear()
            self.s.root.clipboard_append(selected)
        except:
            pass

    def changeic(self):
        color = askcolor()
        if not color == (None, None):
            self.s.ic = color[1]
            self.s.editor.config(insertbackground=self.s.ic)
            self.setconfig()

    def paste(self):
        try:
            clipboard = self.s.root.clipboard_get()
            self.s.editor.insert(tk.END, clipboard)
        except:
            pass

    def zoom(self):
        if self.s.zoomed == False:
            self.s.zoomed = True
            self.s.root.state('zoomed')
        else:
            self.s.zoomed = False
            self.s.root.state('normal')

    def lowercase(self):
        text = self.s.editor.get(0.0, tk.END)
        self._replace_all(text.lower())

    def uppercase(self):
        text = self.s.editor.get(0.0, tk.END)
        self._replace_all(text.upper())

    def reverse(self):
        rtext = self.s.editor.get(0.0, tk.END)[::-1]
        self._replace_all(rtext.replace('\n', '', 1))

    def length(self):
        showinfo('Length of text', len(self.s.editor.get(0.0, tk.END)) - 1)

    def terminal(self):
        if platform == 'darwin':
            system('open -a Terminal -n')
        elif platform == 'win32':
            system('start cmd')
        elif platform == 'linux':
            system('gnome-terminal')

    def word_count(self):
        text = self.s.editor.get(0.0, tk.END)
        split = text.split(' ')
        new = [el for el in split if any(i.lower() in 'abcdefghijklmnopqrstuvwxyz' for i in el)]

        showinfo('Word count', str(len(new)))

    def enc_b64(self):
        text = self.s.editor.get(0.0, tk.END)
        self._replace_all(b64encode(text.encode('ascii')).decode('ascii'))

    def dec_b64(self):
        text = self.s.editor.get(0.0, tk.END)
        self._replace_all(b64decode(text.encode('ascii')).decode('ascii'))

    def enc_hex(self):
        text = self.s.editor.get(0.0, tk.END)
        try:
            self._replace_all(hexlify(text.encode('ascii')).decode('ascii'))
        except Exception as e:
            showerror('Error!', str(e))

    def dec_hex(self):
        text = self.s.editor.get(0.0, tk.END)
        try:
            self._replace_all(unhexlify(text.encode('ascii')).decode('ascii'))
        except Exception as e:
            showerror('Error!', str(e))