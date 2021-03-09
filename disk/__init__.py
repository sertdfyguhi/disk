import tkinter as tk
from configparser import ConfigParser
from .func import functions
from .menu import menu
from appdirs import user_data_dir


class tkWindow:
	def __init__(self):
		self.ic = '#fff'
		self.fs = 12
		self.fc = '#ffffff'
		self.bg = '#333333'
		self.font = 'Menlo'
		self.zoomed = False
		self.filename = None
		self.configPath = user_data_dir('disk', 'hdwyx')
		self.config = ConfigParser()
		self.root = tk.Tk()
		self.root.geometry('550x320')
		self.func = functions(self)
		#load configuration
		self.func.loadconfig()
		self.editor = tk.Text(master=self.root, width=1920, height=1080, bg=self.bg, font=(self.font, self.fs),
		highlightthickness=0, fg=self.fc, undo=True, insertbackground=self.ic)
		self.editor.pack()
		menu(self)
		self.func.newfile()
		self.root.title(self.filename + ' - disk')

	def start(self):
		self.root.mainloop()