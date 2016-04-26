#!/usr/bin/python
# -*- coding: utf-8 -*-

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

		# we want to handle strings in unicode	
		line = line.decode( "utf-8" )
		
		# split on ;
		if line[ 0 ] != '#':
			# remove \n from end of line
			podLine = line.strip()
			podCfg = podLine.split( ";" )
			if len( podCfg ) >= 3:
				pod = PodConfig( name = podCfg[ 0 ], nbOfSaveFiles = int( podCfg[ 1 ] ), url = podCfg[ 2 ] )
				result.append( pod )

	return result
