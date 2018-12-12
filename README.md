Hazardous Garbage
=================

Description
-----------

HG is a project to collect samples of malwares from many sources(feeds).

HG uses the [malwarefeeds](https://github.com/neriberto/malwarefeeds), visit the project to check which feeds are in use.

Changelog
---------

Version 0.1 (v0.1)

* A stable version with 6 malware's sources

Version 0.2 (v0.2)

* Fixed many issues with malware's feeds
* Changed log format
* Working with threads
* Now running until kill by system or interrupted through keyboard(Ctrl+C)

Version 0.3 (v0.3)

* Redesigned to be simple to install and usage
* Doesn't have anymore integrations with other projects like [Cuckoo Sandbox](https://github.com/cuckoobox/cuckoo), Viper or VxCage
* The downloaded samples are store in a directory

Requirements
------------

The project was developed and tested with python 3.6

Install and Usage
-----------------

To install use the pip tool

```bash
pip3 install git+https://github.com/neriberto/hg.git#egg=hg
```

To usage just run the command in terminal

```
hg
```

And all the samples with be store in the ~/.samples directory. To change the default directory, try something like:

```
hg --repo /opt/samples/
```

Contributions
-------------

And the thanks go to:

* [Silvio Giunge](https://github.com/SilvioGiunge)
