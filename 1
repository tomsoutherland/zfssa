#!/usr/bin/env python3

import json, argparse, re, sys, requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from os.path import join, basename
from os import environ
from collections import defaultdict

json_indent = 2

def api_help(user, passw, host, versions, services):
    api_services = defaultdict(list)
    api_descript = {}
    match = re.search(r'(\S+):(\d+)', host)
    if not match:
        host = host + ':215'
    if not versions:
        versions = ['v1', 'v2']
    if services:
        for s in services:
            for v in versions:
                url = 'https://' + host + '/api/' + join(s, v)
                rcode, json_data = do_url(url, "GET", user, passw, None, None)
                if rcode != 200: continue
                for i in json_data["service"]["methods"]:
                    if i['path']:
                        k = i['path'] + " " + i['request']
                        api_services[k].append(v)
                        if not k in api_descript:
                            api_descript.update({k: i['description']})
    else:
        for v in versions:
            url = 'https://' + host + '/api/access/' + v
            rcode, json_data = do_url(url, "GET", user, passw, None, None)
            if rcode != 200: continue
            for i in json_data["services"]:
                api_services[i['name']].append(v)
                if not i['name'] in api_descript:
                    api_descript.update({i['name']: i['uri']})
                else:
                    api_descript.update({i['name']: api_descript[i['name']] + ', ' + i['uri']})
    for k in sorted(api_descript):
        if k == "access": continue
        print(k, api_services[k], api_descript[k])
    pfoo = basename(__file__)
    if services:
        print("\nEXAMPLE:")
        for s in services:
            for v in versions:
                print(pfoo, "-u", user, "-p", passw, "-m METHOD -l",
                      "https://" + host + "/api/" + join(s, v) + "/<path>")
    print("\nAPI Docs -> https://docs.oracle.com/cd/F13758_01/html/F13772/index.html")

def do_url(url, meth, user, passw, body, headers):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    try:
        if meth == 'GET':
            r = requests.get(url, auth=(user, passw), verify=False, data=body, headers=headers)
        elif meth == 'PUT':
            r = requests.put(url, auth=(user, passw), verify=False, data=body, headers=headers)
        elif meth == 'POST':
            r = requests.post(url, auth=(user, passw), verify=False, data=body, headers=headers)
        elif meth == 'DELETE':
            r = requests.delete(url, auth=(user, passw), verify=False, data=body, headers=headers)
        else:
            print("Invalid method,", meth)
            return 404, None
    except Exception as e:
        print(str(e))
        return None, None
    try:
        json_data = json.loads(r.text)
    except:
        json_data = None
    return r.status_code, json_data

def json_recurse(url, user, passw, json_data, rcode, done):
    print('\nURL', url)
    print('Response Code', rcode, '\n')
    print(json.dumps(json_data, sort_keys=True, indent=json_indent))
    match = re.search(r'(\S+)(/api\S+)', url)
    if match:
        host = match.group(1)
        nurl = match.group(2)
        done.append(nurl)
    for url in re.findall(r'(/api/\S+)\"', json.dumps(json_data)):
        for d in done:
            if d == url:
                break
        else:
            if url != nurl:
                rcode, json_data = do_url(host + url, "GET", user, passw, None, None)
                json_recurse(host + url, user, passw, json_data, rcode, done)
def no_proxy():
    environ.pop('http_proxy', None)
    environ.pop('https_proxy', None)
    environ.pop('HTTP_PROXY', None)
    environ.pop('HTTPS_PROXY', None)
def main():
    parser = argparse.ArgumentParser(description='Query a ZFSSA rest API')
    parser.add_argument('-u', type=str, help='User name to use in authentication')
    parser.add_argument('-p', type=str, help='User password to use in authentication')
    parser.add_argument('-l', type=str, help="URL for REST method")
    parser.add_argument('-m', type=str.lower, choices=['get', 'put', 'post', 'delete'], help="Method to use for URL")
    parser.add_argument('-r', action='store_true', help="Recurse into JSON results URLs")
    parser.add_argument('-x', action='store_true', help="Use proxy environment (http[s]_proxy=)")

    json_group = parser.add_argument_group('json/payload input options').add_mutually_exclusive_group()
    json_group.add_argument('-j', type=str,
                            help="Comma separated list of key:data pairs",
                            metavar = "k1:v1,k2:v2,..")
    json_group.add_argument('--json', type=str, help="File containing json payload", metavar = '/path/to/json')
    json_group.add_argument('--jsin', action='store_true', help="Read json from STDIN (^D when done)")
    json_group.add_argument('--wflo', type=str, help="File containing workflow", metavar='/../foo.akwf')
    json_group.add_argument('--scrp', type=str, help="File containing script", metavar='/../foo.aksh')
    json_group.add_argument('--upgr', type=str, help="Path to upgrade package", metavar='/../foo.pkg')

    api_help_group = parser.add_argument_group('api help (still need -u and -p)')
    api_help_group.add_argument('--api', help="Host to use", metavar = 'HOST[:PORT]')
    api_help_group.add_argument('-s', help="Optional comma separated service list", metavar = 'svc[,svc]')
    api_help_group.add_argument('-v', help="Optional version(s)", metavar = '[v1 v2 v1,v2]')
    results = parser.parse_args()

    if not results.x:
        no_proxy()
    if results.api:
        if not (results.u and results.p):
            parser.print_help()
            return 1
        if results.s:
            services = results.s.split(',')
        else:
            services = None
        if results.v:
            versions = results.v.split(',')
        else:
            versions = None
        api_help(results.u, results.p, results.api, versions, services)
    elif results.u and results.p and results.l and results.m:
        body = headers = None
        if results.j or results.json or results.jsin:
            headers = {'Content-type': 'application/json'}
        if results.j:
            b = {}
            for kv in re.split(',', results.j):
                [k, v] = kv.split(':')
                if v.lower() == 'true':
                    b.update({k: True})
                elif v.lower() == 'false':
                    b.update({k: False})
                else:
                    b.update({k: v})
            body = json.dumps(b)
        elif results.json:
            with open(results.json) as json_file:
                body = json.load(json_file)
        elif results.jsin:
            print('Enter json now. Hit ^D when done.\n')
            body = json.loads(sys.stdin.read())
        elif results.wflo:
            with open(results.wflo) as fp:
                body = fp.read()
                headers = {'Content-type': 'application/javascript'}
        elif results.scrp:
            with open(results.scrp) as fp:
                body = fp.read()
                headers = {'Content-type': 'application/x-www-form-urlencoded'}
        elif results.upgr:
            with open(results.upgr, 'rb') as fp:
                body = fp.read()
                headers = {'Content-type': 'application/octet-stream'}
        meth = results.m.upper()
        rcode, json_data = do_url(results.l, meth, results.u, results.p, body, headers)
        if results.r and meth == 'GET':
            json_recurse(results.l, results.u, results.p, json_data, rcode, [])
        else:
            print('Response Code', rcode, '\n')
            print(json.dumps(json_data, sort_keys=True, indent=json_indent))

if __name__ == '__main__':
    main()
