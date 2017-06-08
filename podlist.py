#!/usr/bin/python

import os
from collections import namedtuple

# named tuple that holds a podcast config
PodConfig = namedtuple( "PodConfig", "name nbOfSaveFiles url" )

# return list of podcasts
def getPodcasts( podListFile ):

	# read list of podcasts
	if not os.path.isfile( podListFile ):
		return None
	f = open( podListFile, "r" )
	lines = f.readlines()
	f.close()

	result = []	
	for line in lines:

		# split on ;
		if line[ 0 ] != '#':
			# remove \n from end of line
			podLine = line.strip()
			podCfg = podLine.split( ";" )
			if len( podCfg ) >= 3:
				podName = podCfg[ 0 ]
				podNbOfSaveFiles = int( podCfg[ 1 ] )
				podUrl = podCfg[ 2 ]
				pod = PodConfig( name = podName, nbOfSaveFiles = podNbOfSaveFiles, url = podUrl )
				result.append( pod )

	return result
