#coding:utf-8
import os
import codecs
import sys

from Note import Position
from Note import Note

class NoteBookException(Exception):

	def __init__(self,errorfiles):
		Exception.__init__(self)
		self.errorfiles = errorfiles
	
#class ShortInputException(Exception):
#	def __init__(self, length, atleast):
#		Exception.__init__(self)
#		self.length = length
#		self.atleast = atleast
	

class NoteBook():

	def __init__(self):
		self.files = [] #文件名列表
		self.searchStr = None #查找字符串
		#self.replaceEntireFile = False #不间断搜索替换整个文档
		#self.replaceAllFiles = False #不间断搜索替换所有文件
		self.notes = [] #note列表
		self.__index = 0 #当前搜索走在文档位置

	def setSerachStr(self,value):
		self.searchStr = value
	
	def reset(self):
		self.currentNote = None
		self.__index = 0
	
	def searchNext(self):
		#判断数据不全情况，直接返回空
		if len(self.files) == 0 or self.searchStr == None or self.__index>=len(self.files):
			return None

		#搜索当前文档
		p = self.notes[self.__index].searchNext(self.searchStr);

		if p==None:
			#当前文档已经是最后一个文档，返回空
			if (self.__index+1)==len(self.files):
				self.reset()
				return None
			else:
			#继续搜索下一个文档
				self.__index+=1
				return self.searchNext()
		else:
			return p

	def replace(self,p,newStr):
		self.notes[self.__index].replace(p,self.searchStr,newStr)
	
	def replace_find(self,p,newStr):
		self.replace(p,newStr)
		return self.searchNext()

	def replaceAll(self,newStr):
		while True:
			p = self.searchNext()
			if p!=None:
				self.replace(p,newStr)
			else:
				break

	def add(self,path):
	#添加路径，并且创建note加入列表
		for i in self.files:
			if i==path:
				return False
		self.files.append(path);
		self.notes.append(Note(path));
		return True
	
	def update(self):
	#在文件所在位置新建backup文件夹进行备份，更新文件
		if len(self.files) == 0:
			return

		f = None
		errorfiles = []

		i=0
		while i<len(self.files):
			try:
				p = self.files[i]
				abspath = os.path.abspath(p) #文件所在绝对路径
				filename = os.path.basename(p) #文件名
				parent = os.path.dirname(p) #文件所在父目录绝对路径
				backupfolder = os.path.join(parent,"backup") #备份文件夹绝对路径

				#创建备份文件夹
				if not os.path.exists(backupfolder):
					os.mkdir(backupfolder);
				
				#备份
				os.rename(abspath,os.path.join(backupfolder,filename));

				#写入文件
				f = open(p,'w')
				for string in self.notes[i].lines:
					f.write(string)

			except:
				errorfiles.append(self.files[i])
			finally:
				if f!=None:
					f.close()
				i+=1

		if len(errorfiles)!=0:
			print "raise"
			raise NoteBookException(errorfiles)


#notebook = NoteBook()
#notebook.add("temp.txt")
#notebook.add("temp2.txt")
#notebook.setSerachStr("那是")
#notebook.replaceAll("这是")
#notebook.update()
#while True:
#	posi = notebook.searchNext();
#	if posi==None:
#		break
#	notebook.replace(posi,"那是");
#notebook.update()
