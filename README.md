Hazardous Garbage
=================

Description
-----------

HG is a project to collect samples of malwares from many sources.

Features
--------

* New sources may be added in a simple way, just creating a module in sub directory modules.
* Is integrated with [VxCage] (https://github.com/cuckoobox/vxcage), so it's focused only in get the samples. 
* Is integrated with [Cuckoo Sandbox] (https://github.com/cuckoobox/cuckoo).

Malwares Sources:

* [Malc0de](http://malc0de.com/)
* [Malware Blacklist](http://www.malwareblacklist.com)
* [Malware Domain List](http://www.malwaredomainlist.com/)
* [Spyeye Tracker](https://spyeyetracker.abuse.ch/)
* [VXvault](http://vxvault.siri-urz.net/)
* [Zeus Tracker](https://zeustracker.abuse.ch/)

Requirements
------------

Python 2.7 is required to run HG. To install the project dependencies do this:

	pip install -r requirements.txt

If you are using Debian/Ubuntu maybe you will need install some packages first:

    apt-get install libxml2-dev libxslt1-dev python2.7-dev

Configuration
-------------

HG only analyzes the malwares sources and downloads the samples, so to store the samples, HG use
the VxCage, then first is needed to install it.

Configure HG using the hg.conf in conf directory, it is simple see below:

	[vxcage]
	enabled = yes
	connection = http://localhost:8080/

Now HG can send samples to [Cuckoo Sandbox] (https://github.com/cuckoobox/cuckoo), in hg.conf you
can configure this integration, just set the address for your cuckoo installation, remember, to do this you
need to run the Cuckoo API, not the web interface, see configuration example bellow:

	[cuckoo]
	enable = yes
	connection = http://localhost:8090/

Contributions
-------------

And the thanks go to:

* [Silvio Giunge](https://github.com/SilvioGiunge)

[![endorse](https://api.coderwall.com/neriberto/endorsecount.png)](https://coderwall.com/neriberto)
