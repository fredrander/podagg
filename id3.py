#!/usr/bin/python
# -*- coding: utf-8 -*-

from mutagen.easyid3 import EasyID3
import mutagen
import os


# update ID3 tag with filename as title and podName as artist
def updateTags( fullFileName, podName ):

	id3Tag = None
	
	# try open tags, if fails, create new
	try:
		id3Tag = EasyID3( fullFileName )
	except:
		id3Tag = mutagen.File( fullFileName, easy = True )
		if id3Tag == None:
			print( "Failed to create id3 tags" )
			return
		id3Tag.add_tags()

	# extract file name without extension from full file name
	fileName = os.path.split( fullFileName )[ 1 ]
	title = os.path.splitext( fileName )[ 0 ]

	id3Tag[ "title" ] = u"{}".format( title )
	id3Tag[ "artist" ] = u"{}".format( podName )

	id3Tag.save()