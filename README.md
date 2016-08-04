# external_web_sources
A python script to pull script src, iframe src, window data values from BurpSuite proxy logs. 

Enable logging in your Burp Miscellaneous options and make sure that (any category) Request and Response are both being logged. If one is not being logged then the script will fail.

Call the script with `python external_web_sources.py <log_file>` and it will display a sorted GUI of 3rd party imports for each website. 

