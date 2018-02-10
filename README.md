Hazardous Garbage
=================

Description
-----------

HG is a project to collect samples of malwares from many sources(feeds).

Features
--------

* New sources may be added in a simple way, just creating a module in sub directory modules.
* Is integrated with [VxCage](https://github.com/cuckoobox/vxcage), so it's focused only in get the samples.
* Is integrated with [Cuckoo Sandbox](https://github.com/cuckoobox/cuckoo).

Malware's Sources(Feeds):

* [Malc0de](http://malc0de.com/)
* [VXvault](http://vxvault.siri-urz.net/)

Changelog
---------

Version 0.1 (v0.1)

* A stable version with 6 malware's sources

Version 0.2 (v0.2)

* Fixed many issues with malware's feeds
* Changed log format
* Working with threads
* Now running until kill by system or interrupted through keyboard(Ctrl+C)

Requirements
------------

Python 2.7 is required to run HG. To install the project dependencies do this:

```bash
pip install -r requirements.txt
```

If you are using Debian/Ubuntu maybe you will need install some packages first:

```bash
apt-get install libxml2-dev libxslt1-dev python2.7-dev
```

Configuration
-------------

HG only analyzes the malwares sources and downloads the samples, so to store the samples, HG use
the VxCage, then first is needed to install it.

Configure HG using the hg.conf in conf directory, it is simple see below:

```ini
[vxcage]
enabled = yes
connection = http://localhost:8080/
```

Now HG can send samples to [Cuckoo Sandbox](https://github.com/cuckoobox/cuckoo), in hg.conf you
can configure this integration, just set the address for your cuckoo installation, remember, to do this you
need to run the Cuckoo API, not the web interface, see configuration example bellow:

```ini
[cuckoo]
enable = yes
connection = http://localhost:8090/
```

Contributions
-------------

And the thanks go to:

* [Silvio Giunge](https://github.com/SilvioGiunge)
