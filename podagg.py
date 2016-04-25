import rssfeed
import podepisode
import history
import podfile
import podlist
import config
import id3
import os
import sys


# default config file path
configFile = os.path.expanduser( "~/.podagg/config" )
# check if alternate config file in arg
if len( sys.argv ) > 1:
	configFile = sys.argv[ 1 ]

print( "Config file: {}".format( configFile ) )

# read config
cfg = config.getConfig( configFile )

# get all configured podcasts
pods = podlist.getPodcasts( cfg.podlist )

for pod in pods:

	# append podcast name to download dir. if config separateDirs = True
	destDir = cfg.downloadPath
	if cfg.separateDirs:
		destDir = os.path.join( cfg.downloadPath, pod.name )

	# get list os all episodes in pod
	episodes = rssfeed.getPodEpisodes( pod.url )

	if episodes != None:
		for episode in episodes:

			# check if already handled
			if history.exist( episode.url, cfg.history ) != True:
				# no, download
				print( "Download: {}".format( episode.url ) )
				downloadedFile = None				
				downloadedFile = podfile.download( episode, pod.name, destDir )
				if downloadedFile != None:
					# add to history
					history.add( episode.url, cfg.history )
					# update ID3 tags of downloaded file
					if cfg.updateId3:
						id3.updateTags( downloadedFile, pod.name )
	# remove pod files if too many in dir					
	podfile.cleanupDir( pod.name, destDir, pod.nbOfSaveFiles )
