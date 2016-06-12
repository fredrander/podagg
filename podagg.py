#!/usr/bin/python
# -*- coding: utf-8 -*-

import rssfeed
import podepisode
import history
import podfile
import podlist
import config
import id3
import os
import sys
import operator
import syslog


syslog.syslog( syslog.LOG_INFO, "Start" )

# default config file path
configFile = os.path.expanduser( "~/.podagg/config" )
# check if alternate config file in arg
if len( sys.argv ) > 1:
	configFile = sys.argv[ 1 ]

# read config
cfg = config.getConfig( configFile )

# get all configured podcasts
pods = podlist.getPodcasts( cfg.podlist )

podCnt = 0
for pod in pods:

	podCnt = podCnt + 1

	# append podcast name to download dir. if config separateDirs = True
	destDir = cfg.downloadPath
	if cfg.separateDirs:
		destDir = os.path.join( cfg.downloadPath, pod.name )

	# get list os all episodes in pod
	episodes = rssfeed.getPodEpisodes( pod.url )

	# get list of episodes to download
	episodesToDownload = []
	for episode in episodes:
		if history.exist( episode.url, cfg.history ) != True:
			episodesToDownload.append( episode )

	# sort descending by publish date and title
	episodesToDownload = sorted( episodesToDownload, key = operator.attrgetter( "publishedTime", "title" ), reverse = True )

	# only download at max pod.nbOfSaveFiles episodes 
	episodesToDownload = episodesToDownload[ : pod.nbOfSaveFiles ]
	episodeCnt = 0

	for episode in episodesToDownload:
		episodeCnt = episodeCnt + 1
		syslog.syslog( syslog.LOG_INFO, u"Download, pod: {}/{}, episode: {}/{}".format( podCnt, len( pods ), episodeCnt, len( episodesToDownload ) ) )
		downloadedFile = None				
		downloadedFile = podfile.download( episode, pod.name, destDir )
		if downloadedFile != None:
			# add to history
			history.add( episode.url, cfg.history )
			# update ID3 tags of downloaded file
			if cfg.updateId3:
				id3.updateTags( downloadedFile, pod.name )
		else:
			syslog.syslog( syslog.LOG_ERR, "Download failed" )

	# remove pod files if too many in dir					
	podfile.cleanupDir( pod.name, destDir, pod.nbOfSaveFiles )
	# copy latest episode to special dir
	if cfg.latestEpisodeDir != None:
		podfile.updateLastEpisodeDir( pod.name, destDir, cfg.latestEpisodeDir )

syslog.syslog( syslog.LOG_INFO, "Done" )

