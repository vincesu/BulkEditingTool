#coding:utf-8
import codecs
import sys

import util

class Position():
	#位置类

	def __init__(self,row,column):
		self.row = row	#行
		self.column = column	#每行位置

class Note():

	def __init__(self,path):

		self.path = path #路径
		self.lines = []; #列表 存放每行数据
		self.currentPosition = Position(0,0)	#start find position

		i=0;
		f = None
		try:
			#读取文件存入列表
			f = file(path)
			while True:
				self.lines.append(unicode(f.readline()))
				if len(self.lines[i]) == 0: # Zero length indicates EOF
					break
				i+=1
			#删除最后一行空行
			del self.lines[i]
		except IOError:
			raise IOError("%s%s%s" % ("this file is not exists(",path,")"))
		finally:
			if f!=None:
				f.close()

	def searchNext(self,searchStr):
		"""在当前位置之后 继续搜索searchStr 如果当前位置为空 则从头搜索 
			搜索无结果返回空"""

		#编码
		searchStr = unicode(searchStr)

		result = None;
		if len(self.lines) == 0:
			return None;

		while self.currentPosition.row < len(self.lines):
			i = self.lines[self.currentPosition.row].find(searchStr,self.currentPosition.column)
			if i==-1:
				self.currentPosition.row +=1;
				self.currentPosition.column = 0;
				continue
			else:
				result = Position(self.currentPosition.row,i)
				self.currentPosition.column=(i+len(searchStr))
				break

		return result

	def replace(self,position,oldstr,newstr):
		"""在position位置 将oldstr替换为newstr"""

		#编码
		oldstr = unicode(oldstr)
		newstr = unicode(newstr)

		if position.row>=len(self.lines):
			return;
		string = "%s%s%s" % (self.lines[position.row][0:position.column],newstr,self.lines[position.row][position.column+len(oldstr):])
		self.lines[position.row] = string
		self.currentPosition.column = position.column+len(newstr);
	
	def reset(self):
		"""将搜索位置重置为起始位置"""
		self.currentPosition.row = 0;
		self.currentPosition.column = 0;
	
	def getCurrentLine(self):
		"""返回当前位置行 不存在返回空"""
		if len(self.lines)>0 and self.currentPosition.row<len(self.lines):
			return self.lines[self.currentPosition.row]
		else:
			return None

#path = "D:/MyDocument/code/python/BulkEditingTool/temp.txt"
#note = Note(path)
#p = None
#while True:
#	p = note.searchNext("这是")
#	if p==None:
#		break
#	note.replace(p,"这是","那是")
#
#ff = open("D:/MyDocument/code/python/BulkEditingTool/ok.txt","a")
#for s in note.lines:
#	ff.write(s)
#ff.close()
#
