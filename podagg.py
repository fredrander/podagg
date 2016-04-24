import rssfeed
import podepisode
import history
import podfile
import podlist
import config


configFile = ".config"

# read config
cfg = config.getConfig( configFile )

# get all podcast configs
pods = podlist.getPodcasts( cfg.podlist )

# get list os all episodes in pod
episodes = rssfeed.getPodEpisodes( "http://feeds.serialpodcast.org/serialpodcast" )
podName = "Serial"
podPath = "/home/fredrander/Serial/"
#episodes = rssfeed.getPodEpisodes( "http://api.sr.se/api/rss/pod/3966" )
if episodes != None:
	for episode in episodes:

		# check if already handled
		if history.exist( episode.url, cfg.history ) != True:
			# no, download
			if podfile.download( episode, podName, cfg.downloadPath ) == True:
				# add to history
				history.add( episode.url, cfg.history )
