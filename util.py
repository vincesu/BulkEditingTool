import sys

def setSysCoding(value="utf-8"):
	default_encoding = value
	if sys.getdefaultencoding() != default_encoding:
		reload(sys)
		sys.setdefaultencoding(default_encoding)


