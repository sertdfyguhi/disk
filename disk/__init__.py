import tkinter as tk
from configparser import ConfigParser
from .func import functions
from .menu import menu
from appdirs import user_config_dir, user_data_dir
from os import path, mkdir


class window:
	def __init__(self):
		self.configPath = user_config_dir('disk', 'hdwyx')
		self.themesPath = user_data_dir('disk_themes', 'hdwyx')

		#make config file and directory if no directory/file 
		if not path.isdir(self.configPath):
			mkdir(self.configPath)
		if not path.isfile(self.configPath + '/config.ini'):
			open(self.configPath + '/config.ini', mode='w').close()
		if not path.isdir(self.themesPath):
			mkdir(self.themesPath)

		self.ic = '#fff'
		self.fs = 12
		self.fc = '#ffffff'
		self.bg = '#333333'
		self.font = 'Menlo'
		self.zoomed = False
		self.filename = None
		self.config = ConfigParser()
		self.root = tk.Tk()
		self.root.geometry('550x320')
		self.func = functions(self)
		#load configuration
		self.func.loadconfig()
		self.editor = tk.Text(master=self.root, width=1920, height=1080, bg=self.bg, font=(self.font, self.fs),
		highlightthickness=0, fg=self.fc, undo=True, insertbackground=self.ic)
		self.editor.pack()
		m = menu(self)
		m.make()
		self.winmenu.add_command(label='New window', command=lambda: window().start())
		m.add()
		self.func.newfile()
		self.root.title(self.filename + ' - disk')

	def start(self):
		self.root.mainloop()