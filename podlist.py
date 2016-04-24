import os

# return list of podcasts
def getPodcasts( podListFile ):
	if not os.path.isfile( podListFile ):
		return None
	f = open( podListFile, "r" )
	lines = f.readlines()
	for line in lines:
		# split on ;
		print( line )
	f.close()
	return None
