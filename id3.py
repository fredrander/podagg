import eyeD3
import os


# update ID3 tag with filename as title and podName as artist
def updateTags( fullFileName, podName ):

	id3Tag = eyeD3.Tag()
	id3Tag.link( fullFileName )

	# extract file name without extension from full file name
	fileName = os.path.split( fullFileName )[ 1 ]
	title = os.path.splitext( fileName )[ 0 ]

	id3Tag.setTitle( u"{}".format( title ) )
	id3Tag.setArtist( u"{}".format( podName ) )

	id3Tag.update()