#!/usr/bin/python

import urllib2
import urlparse
import podepisode
from xml.dom import minidom
from datetime import datetime


# returns an array with all episodes in pod
def getPodEpisodes( url ):
	
	result = []

	# read url
	rsp = None
	rssData = None
	try:
		rsp = urllib2.urlopen( url )
		rssData = rsp.read()
	except:
		return result
	
	# parse xml
	xmlDoc = minidom.parseString( rssData )
	for node in xmlDoc.getElementsByTagName( "item" ):
		episode = _getPodEpisode( node )
		if episode != None:
			result.append( episode )
	return result

########################################################################

# private functions

def _getPodEpisodeContentUrl( enclosureElement ):
	if enclosureElement.hasAttribute( "url" ) == False:
		return None
	url = enclosureElement.getAttribute( "url" )
	splitUrl = urlparse.urlsplit( url )
	protStr = splitUrl[ 0 ] + "://"
	result = protStr + urllib2.quote( url[ len(protStr): ].encode( 'utf-8' ) )
	return result

def _getPodEpisodeContentType( enclosureElement ):
	if enclosureElement.hasAttribute( "type" ) == False:
		return None
	result = enclosureElement.getAttribute( "type" )
	return result

def _getPodEpisodeTitle( titleElement ):
	result = None
	for child in titleElement.childNodes:
		if child.nodeType == minidom.Node.TEXT_NODE:
			result = child.data
		elif child.nodeType == minidom.Node.CDATA_SECTION_NODE:
			result = child.data
	result = result.strip()
	return result.encode( 'utf-8' )

def _getPodEpisodePublishedTime( publishedElement ):
	elemStr = None
	for child in publishedElement.childNodes:
		if child.nodeType == minidom.Node.TEXT_NODE:
			elemStr = child.data

	# parse publish time
	pubDate = None
	if elemStr != None and len( elemStr ) > 15:
		# only interested in date (example of format (RFC822) Sun, 24 Apr 2016 16:03:00 GMT)
		try:
			tmpStr = elemStr[:16]
			pubDate = datetime.strptime( tmpStr, "%a, %d %b %Y" )
		except:
			# incorrect date format
			pubDate = None

	if pubDate == None:
		pubDate = datetime.now()

	dateStr = datetime.strftime( pubDate, "%Y%m%d" )
	return dateStr

def _getPodEpisode( rssItem ):

	url = None
	mimeType = None
	title = None
	publishedTime = None

	result = None

	for element in rssItem.childNodes:

		if element.nodeType == minidom.Node.ELEMENT_NODE: 
			if element.tagName == "enclosure":
				url = _getPodEpisodeContentUrl( element )
				mimeType = _getPodEpisodeContentType( element )
			if element.tagName == "title":
				title = _getPodEpisodeTitle( element )
			if element.tagName == "pubDate":
				publishedTime = _getPodEpisodePublishedTime( element )

	if url != None:
		result = podepisode.Episode( title = title, url = url, type = mimeType, publishedTime = publishedTime )
	return result
