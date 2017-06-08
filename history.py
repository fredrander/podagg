#!/usr/bin/python

import mmap


def exist( url, historyFile ):
	# memory map history file
	fp = None
	try:
		fp = open( historyFile, "r" )
	except:
		return False

	fileContent = mmap.mmap( fp.fileno(), 0, access=mmap.ACCESS_READ )
	found = False
	if fileContent.find( url ) != -1:
		found = True
	else:
		found = False
	fp.close()
	return found

def add( url, historyFile ):
	fp = open( historyFile, "a" )
	if fp == None:
		return False
	fp.write( url )
	fp.write( "\n" )
	fp.close()
	return True
