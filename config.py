from ConfigParser import ConfigParser
from collections import namedtuple

# named tuple that holds config
Config = namedtuple( "Config", "podlist history downloadPath" )

def getConfig( configFile ):

	# defaults
	podlist = "~/.podagg/rssfeeds"
	history = "~/.podagg/.history"
	downloadPath = "~/podcasts/"
	
	cfgFile = ConfigParser()
	cfgFile.read( configFile )
	if cfgFile.has_option( "files", "podlist" ):
		podlist = cfgFile.get( "files", "podlist" )
	if cfgFile.has_option( "files", "history" ):
		history = cfgFile.get( "files", "history" )
	if cfgFile.has_option( "paths", "download_dir" ):
		downloadPath = cfgFile.get( "paths", "download_dir" )
	
	result = Config( podlist = podlist, history = history, downloadPath = downloadPath )
	
	return result