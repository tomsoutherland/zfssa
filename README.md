zfssa.py

A python3 program to interact with the rest api in the Oracle ZFS Storage Appliance

Requires requests  
  macOS % sudo -H python3 -m pip install requests

<pre>
% zfssa -h
usage: zfssa [-h] [-u U] [-p P] [-l L] [-m {get,put,post,delete}] [-r] [-x]
             [-j k1:v1,k2:v2,.. | --json /path/to/json | --jsin | --wflo /../foo.akwf | --scrp /../foo.aksh | --upgr /../foo.pkg] [--api HOST[:PORT]]
             [-s svc[,svc]] [-v [v1 v2 v1,v2]]

Query a ZFSSA rest API

optional arguments:
  -h, --help            show this help message and exit
  -u U                  User name to use in authentication
  -p P                  User password to use in authentication
  -l L                  URL for REST method
  -m {get,put,post,delete}
                        Method to use for URL
  -r                    Recurse into JSON results URLs
  -x                    Use proxy environment (http[s]_proxy=)

json/payload input options:
  -j k1:v1,k2:v2,..     Comma separated list of key:data pairs
  --json /path/to/json  File containing json payload
  --jsin                Read json from STDIN (^D when done)
  --wflo /../foo.akwf   File containing workflow
  --scrp /../foo.aksh   File containing script
  --upgr /../foo.pkg    Path to upgrade package

api help (still need -u and -p):
  --api HOST[:PORT]     Host to use
  -s svc[,svc]          Optional comma separated service list
  -v [v1 v2 v1,v2]      Optional version(s)
</pre>
