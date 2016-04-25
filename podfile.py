import tempfile
import os
import urllib2
import podepisode
import re
from datetime import datetime
from mimetypes import MimeTypes

# download podcast and save with correct name
# returns full path and name of downloaded file, None if failure
def download( episode, podName, podPath ):

	tmpFile = _downloadTemp( episode )
	if tmpFile == None:
		return None
	
	fileName = _generateFileName( episode, podName )
	destFile = os.path.join( podPath, fileName )
	print( "Save: {}".format( destFile ) )
	_moveTemp( tmpFile, destFile )
	return destFile

# cleanup dir from too many files for a pod
def cleanupDir( podName, podPath, maxNbOfFiles ):
	# get pod all files in dir
	allFiles = os.listdir( podPath )
	# find files from searched pod
	podFiles = []
	for f in allFiles:
		if re.match( "^{}".format( podName ), f ):
			podFiles.append( f )
	# sort descending and delete all files after maxNbOfFiles
	podFiles.sort( reverse=True )
	cnt = 0
	for sf in podFiles:
		cnt = cnt + 1
		if cnt > maxNbOfFiles:
			fileToDelete = os.path.join( podPath, sf )
			print( "Delete: {}".format( fileToDelete ) )
			os.remove( fileToDelete )
	
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
	pubDate = None
	# use published time from RSS feed if exist, otherwise current date
	if episode.publishedTime != None and len( episode.publishedTime ) > 15:
		# only interested in date (example of format (RFC822) Sun, 24 Apr 2016 16:03:00 GMT)
		tmpStr = episode.publishedTime[:16]
		pubDate = datetime.strptime( tmpStr, "%a, %d %b %Y" )
	else:
		pubDate = datetime.now()

	dateStr = datetime.strftime( pubDate, "%Y%m%d" )
	
	ext = _getExtension( episode )

	result = None
	if episode.title != None and len( episode.title ) > 0:
		# remove forbidden file name chars. from title
		titleStr = re.sub( "[\/\*\<\>\:\\\\]", "_", episode.title )
		result = u"{} {} {}{}".format( podName, dateStr, titleStr, ext )
	else:
		result = u"{} {}{}".format( podName, dateStr, ext ) 
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
	os.rename( tmp, dest )