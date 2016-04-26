#!/usr/bin/python
# -*- coding: utf-8 -*-

from mutagen.easyid3 import EasyID3
import os


# update ID3 tag with filename as title and podName as artist
def updateTags( fullFileName, podName ):

	id3Tag = EasyID3( fullFileName )

	# extract file name without extension from full file name
	fileName = os.path.split( fullFileName )[ 1 ]
	title = os.path.splitext( fileName )[ 0 ]

	id3Tag[ "title" ] = u"{}".format( title )
	id3Tag[ "artist" ] = u"{}".format( podName )

	id3Tag.save()