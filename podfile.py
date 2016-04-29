#!/usr/bin/python
# -*- coding: utf-8 -*-

import tempfile
import os
import shutil
import urllib2
import podepisode
import re
from mimetypes import MimeTypes


# download podcast and save with correct name
# returns full path and name of downloaded file, None if failure
def download( episode, podName, podPath ):

	tmpFile = _downloadTemp( episode )
	if tmpFile == None:
		return None
	
	fileName = _generateFileName( episode, podName )
	destFile = os.path.join( podPath, fileName )
	print( u"Save: {}".format( destFile ) )
	if _moveTemp( tmpFile, destFile ) != True:
		return None
	return destFile

# cleanup dir from too many files for a pod
def cleanupDir( podName, podPath, maxNbOfFiles ):
	# get pod files in dir
	podFiles = _allFilesFromPodInDir( podPath, podName )
	# sort descending and delete all files after maxNbOfFiles
	podFiles.sort( reverse=True )
	cnt = 0
	for sf in podFiles:
		cnt = cnt + 1
		if cnt > maxNbOfFiles:
			fileToDelete = os.path.join( podPath, sf )
			print( u"Delete: {}".format( fileToDelete ) )
			os.remove( fileToDelete )
	
# update last episode dir. with latest episode for a pod
def updateLastEpisodeDir( podName, podPath, lastEpisodeDir ):

	# create last episiode dir if missing
	if not os.path.isdir( lastEpisodeDir ):
		os.makedirs( lastEpisodeDir )

	# get pod files in dir
	podFiles = _allFilesFromPodInDir( podPath, podName )
	# sort descending
	podFiles.sort( reverse=True )

	if len( podFiles ) < 1:
		# no files
		return

	lastSourceFile = podFiles[ 0 ]
	
	# get files from pod in last episode dir
	lastFiles = _allFilesFromPodInDir( lastEpisodeDir, podName )
	
	# delete file(s) in last episode dir if not correct file
	alreadyLatest = False
	for f in lastFiles:
		uf = f.decode( "utf-8" )
		if uf == lastSourceFile:
			# latest file already in dir
			alreadyLatest = True
		else:
			fileToDelete = os.path.join( lastEpisodeDir, uf )
			os.remove( fileToDelete )
	
	# copy file to last episode dir
	if alreadyLatest != True:
		src = os.path.join( podPath, lastSourceFile )
		dest = os.path.join( lastEpisodeDir, lastSourceFile )
		shutil.copy( src, dest )
	
################################################################################

# private functions

# download pod file to a temp file, returns name of temp file or None if failed
def _downloadTemp( episode ):
	
	# create a temp file, returns a tuple ( file handle, file name )
	tmpFile = tempfile.mkstemp()

	# open url	
	rsp = None
	try:
		rsp = urllib2.urlopen( episode.url )
	except:
		return None
	
	# read in "chunks"
	done = False
	chunkSize = 1024 * 1024
	while done != True:
		data = rsp.read( chunkSize )
		if not data:
			done = True
		else:
			os.write( tmpFile[ 0 ], data )
	os.close( tmpFile[ 0 ] )
	return tmpFile[ 1 ]

def _getExtension( episode ):
	# get extension from url
	urlExt = os.path.splitext( episode.url )[ 1 ]
	# get extension from media type
	mime = MimeTypes()
	mimeExtList = mime.guess_all_extensions( episode.type )
	# check if url extension matches any item in list
	if urlExt in mimeExtList:
		# yep, then url extension is good
		return urlExt
	# otherwise, use recommendation from MimeTypes, as default we use .mp3  	
	mimeExt = mime.guess_extension( episode.type )
	if mimeExt == None:
		mimeExt = ".mp3"
	return mimeExt

def _generateFileName( episode, podName ):
	ext = _getExtension( episode )

	result = None
	if episode.title != None and len( episode.title ) > 0:
		# remove forbidden file name chars. from title
		titleStr = re.sub( "[\/\*\<\>\\\\]", "_", episode.title )
		result = u"{} {} {}{}".format( podName, episode.publishedTime, titleStr, ext )
	else:
		result = u"{} {}{}".format( podName, episode.publishedTime, ext ) 
	return result

def _moveTemp( tmp, to ):
	# append counter to filename if destination already exist
	dest = to
	cnt = 1
	while os.path.isfile( dest ):
		splitPath = os.path.splitext( to )
		dest = u"{}_{}{}".format( splitPath[ 0 ], cnt, splitPath[ 1 ] )
		cnt = cnt + 1
		
	# create destination path if missing
	destDir = os.path.split( dest )[ 0 ]
	if not os.path.isdir( destDir ):
		os.makedirs( destDir )
	try:
		shutil.copy( tmp, dest )
		os.remove( tmp )
		os.chmod( dest, 0644 )
		return True
	except:
		return False

def _allFilesFromPodInDir( dir, podName ):
	podFiles = []
	if not os.path.isdir( dir ):
		# dir missing
		return podFiles
	# get all files in dir
	allFiles = os.listdir( dir )
	# find files from searched pod
	for f in allFiles:
		if re.match( u"^{}".format( podName ), f ):
			podFiles.append( f )
	return podFiles
