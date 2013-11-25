Hazardous Garbage
=================

Description
-----------

HG is a project to collect samples of malwares from many sources.

Features
--------

* New sources may be added in a simple way, just creating a module in sub directory modules.
* Is integrated with [VxCage] (https://github.com/cuckoobox/vxcage), so it's focused only in get the samples. 

Malwares Sources:

* [Malc0de](http://malc0de.com/)
* [Malware Domain List](http://www.malwaredomainlist.com/)
* [Spyeye Tracker](https://spyeyetracker.abuse.ch/)
* [Zeus Tracker](https://zeustracker.abuse.ch/)

Requirements
------------

HG only analyzes the malwares sources and downloads the samples, so to store the samples, HG use the VxCage, then first is needed to install it.

Configure HG using the hg.conf in conf directory, it is simple see below:

	[vxcage]
	https = no
	ip = localhost
	port = 8080
	username =
	password =

TODO
----

* Discard empty files
* Send samples to [Aleph](https://github.com/merces/aleph)
* Work with VxCage authenticated
* Analyze Zip Files, if  is a Zip, JAR or APK, so sends a tag to VxCage
* Save URLs.
