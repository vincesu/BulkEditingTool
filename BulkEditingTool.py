#coding:utf-8
from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
import time

from NoteBook import NoteBook
from NoteBook import NoteBookException
import util

util.setSysCoding()

class BulkEditingTool:

	def __init__(self,root):

		self.isComingSoonDialog = lambda : tkMessageBox.showwarning("message","this function is coming soon")

		self.root = root

		self.root.title("bulk editing tool")#窗口标题

		self.notebook = NoteBook()#笔记本

		self.searchEntireFile = IntVar()#是否查找替换整个文件 1 是 0 否
		self.searchAllFiles = IntVar()#是否查找替换所有文件 1 是 0 否
		self.searchString = StringVar()#查找字符串
		self.replaceString = StringVar()#替换字符串
		self.codeType = StringVar()#文件编码类型
		self.codeType.set("utf-8")#设置文件编码类默认为utf-8

		self.topFrame = Frame(self.root)
		self.topFrame.pack(fill="x")
		self.leftFrame = Frame(self.root)
		self.leftFrame.pack(side="left",fill="y")
		self.rightFrame = Frame(self.root,)
		self.rightFrame.pack(expand="yes",fill="both")

		self.__createMenu()
		self.__createListBox()
		self.__createConsole()
		self.__createShowArea()
	
	def __createMenu(self):
		""" 创建菜单 """

		self.menu = Menu(self.root)
		self.root.config(menu=self.menu);

		filemenu = Menu(self.menu)
		self.menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="Open", command=self.__chooseFiles)
		#filemenu.add_separator()
		filemenu.add_command(label="Clear",command=self.clearFilesList)
		filemenu.add_command(label="Exit",command=self.root.quit)

		helpmenu = Menu(self.menu)
		self.menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About",command=self.__about)

	def __about(self):
		tkMessageBox.showwarning("About","author:vince su\ncontact me:vince.lr.s@gmail.com")

	def __createListBox(self):
		""" 创建文件显示列表"""
		self.fileListBox = Listbox(self.topFrame,height=5)
		self.fileListBox.pack(fill="x",padx=10,pady=10)

	def __createConsole(self):
		""" 创建控制面板控件 """
		f1 = Frame(self.leftFrame)
		f2 = Frame(self.leftFrame)
		f3 = Frame(self.leftFrame)
		f4 = Frame(self.leftFrame)
		f5 = Frame(self.leftFrame)

		Label(f1, text="find:").grid(row=0)
		Label(f1, text="replace:").grid(row=1)

		self.entrySearch = Entry(f1,textvariable=self.searchString).grid(row=0,column=1)
		self.entryReplace = Entry(f1,textvariable=self.replaceString).grid(row=1,column=1)

		f1.pack(fill="x")

		self.buttonFind = Button(f2,text="Find",command=self.find)\
				.pack(side="left",padx=5,pady=5)
		self.buttonReplace = Button(f2,text="Replace",command=self.replace)\
				.pack(side="left",padx=5,pady=5)
		self.buttonReplace_Find = Button(f2,text="Replace/Find",command=self.r_f).\
		pack(side="left",padx=5,pady=5)
		f2.pack(fill="x")

		self.CK_replaceEntireFile = Checkbutton(f3,text="replace entire file",variable=self.searchEntireFile).\
			pack(side="left")
		f3.pack(fill="x")

		self.CK_replaceAllFile = Checkbutton(f4,text="replace all file",variable=self.searchAllFiles).\
			pack(side="left")
		f4.pack(fill="x")

		Label(f5, text="code:").grid(row=0)
		combobox = ttk.Combobox(f5,textvariable=self.codeType,values=["utf-8","gbk","gb2312"])
		combobox.grid(row=0,column=1)
		f5.pack(fill="x")
		combobox.bind("<<ComboboxSelected>>",lambda e:util.setSysCoding(self.codeType.get()) ) 

	def __createShowArea(self):
		""" 创建显示区域 """
		self.showArea = Text(self.rightFrame)
		self.showArea.pack(fill="both",expand="yes")
	
	def __chooseFiles(self):
		""" 选择文件并写入notebook """
		filenames = tkFileDialog.askopenfilenames().split()
		try:
			for s in filenames:
				if self.notebook.add(s):
					self.fileListBox.insert(END,s)
		except:
			tkMessageBox.showerror("error","can't read file.please change code.");

	def showMsg(self,string,flag=1):
		if flag:
			self.showArea.insert(END,"error:%s\n" % string)
		else:
			self.showArea.insert(END,"msg:%s\n" % string)

	def find(self):
		""" 查找下一处 """
		self.isComingSoonDialog()

	def clearFilesList(self):
		self.notebook = NoteBook()
		self.fileListBox.delete(0,self.fileListBox.size()-1)

	def replace(self):
		""" 替换，根据选项可实现单处替换，单一文件替换，所有文件替换 """
		self.showMsg(
				"begin at: %s" % (
				time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
			),
			0)
		if self.searchString.get() == "":
			self.showMsg("search string is empty")
			tkMessageBox.showwarning("message", "search string is empty")
			return None
		if self.replaceString.get() == "":
			self.showMsg("replace string is empty")
			tkMessageBox.showwarning("message", "replace string is empty")
			return None
		if self.searchAllFiles.get():
			try:
				self.notebook.reset()
				self.notebook.setSerachStr(self.searchString.get())
				self.notebook.replaceAll(self.replaceString.get())
			except:
				self.showMsg("can non't replace files")
				tkMessageBox.showerror( "message", "can non't replace files")
				return None
			try:
				self.notebook.update()
				tkMessageBox.showwarning( "message", "replace completed")
				self.showMsg("replace completed",0)
			except NoteBookException, e:
				string = None
				for s in e.errorfiles:
					self.showMsg(
						"file:%s --- can not update,the backup files maybe exist." % (s,))
				if len(e.errorfiles) != len(self.notebook.files):
					self.showMsg("other files update completed.",0)
				if len(e.errorfiles) == 1:
					string = "1 file can't update"
				else:
					string = "%d files can't update" % (len(e.errorfiles),)
				tkMessageBox.showerror( "message", string)
				return None
			except Exception:
				self.showMsg("can not update files!")
				tkMessageBox.showerror( "message", "can not update files!")
		else:
			if self.searchEntireFile.get() == 1:
				self.isComingSoonDialog()
			else:
				self.isComingSoonDialog()

	def r_f(self):
		""" 替换并且查找下一处，前提已处于替换位置 """
		self.isComingSoonDialog()


# create a menu
#menu = Menu(root)
#root.config(menu=menu)
#
#filemenu = Menu(menu)
#menu.add_cascade(label="File", menu=filemenu)
#filemenu.add_command(label="New", command=callback)
#filemenu.add_command(label="Open...", command=callback)
#filemenu.add_separator()
#filemenu.add_command(label="Exit", command=callback)
#
#helpmenu = Menu(menu)
#menu.add_cascade(label="Help", menu=helpmenu)
#helpmenu.add_command(label="About...", command=callback)
#
#leftFrame = Frame(root,bg="red",height=300,width=200)
#frame.pack(side="left",fill="y")
#

