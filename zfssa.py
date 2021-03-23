#!/usr/bin/env python3

import json, argparse, ssl, re, sys, urllib3
from os.path import join, basename
from collections import defaultdict

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
                #print(json.dumps(json_data, sort_keys=True, indent=4))
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

def do_url(url, meth, user, passw, body, ct):
    urllib3.disable_warnings()
    http = urllib3.PoolManager(cert_reqs=ssl.CERT_NONE)
    headers = urllib3.make_headers(basic_auth=user + ':' + passw)
    if body:
        if ct == 'application/json':
            headers.update({'Content-Type':ct})
            encoded_data = json.dumps(body).encode('utf-8')
            r = http.request(meth, url, headers=headers, body=encoded_data)
        elif ct == 'application/javascript':
            headers.update({'Content-Type': ct})
            r = http.request(meth, url, headers=headers, body=body)
        elif ct == 'application/x-www-form-urlencoded':
            headers.update({'Content-Type': ct})
            r = http.request(meth, url, headers=headers, body=body)
            if r.status == 201:
                print('Response Code', r.status, '\n')
                print(r.data.decode('utf-8'))
                sys.exit(0)
        elif ct == 'application/octet-stream':
            headers.update({'Content-Type': ct})
            r = http.request(meth, url, headers=headers, body=body)
            if r.status == 201:
                print('Response Code', r.status, '\n')
                print(r.data.decode('utf-8'))
                sys.exit(0)
    else:
        r = http.request(meth, url, headers=headers)
    try:
        json_data = json.loads(r.data.decode('utf-8'))
    except:
        json_data = None
    return r.status, json_data

def json_recurse(url, user, passw, json_data, rcode, done):
    print('Response Code', rcode, '\n')
    print(json.dumps(json_data, sort_keys=True, indent=4))
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
                rcode, json_data = do_url(host + url, "GET", user, passw, None, 'application/json')
                json_recurse(host + url, user, passw, json_data, rcode, done)

def main():
    parser = argparse.ArgumentParser(description='Query a ZFSSA rest API')
    parser.add_argument('-u', type=str, help='User name to use in authentication')
    parser.add_argument('-p', type=str, help='User password to use in authentication')
    parser.add_argument('-l', type=str, help="URL for REST method")
    parser.add_argument('-m', type=str.lower, choices=['get', 'put', 'post', 'delete'], help="Method to use for URL")
    parser.add_argument('-r', action='store_true', help="Recurse into JSON results URLs")

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
        body = ct = None
        if results.j or results.json or results.jsin:
            ct = 'application/json'
        if results.j:
            body = {}
            for kv in re.split(',', results.j):
                [k, v] = kv.split(':')
                if v.lower() == 'true':
                    body[k] = True
                elif v.lower() == 'false':
                    body[k] = False
                else:
                    body[k] = v
        elif results.json:
            with open(results.json) as json_file:
                body = json.load(json_file)
        elif results.jsin:
            print('Enter json now. Hit ^D when done.\n')
            body = json.loads(sys.stdin.read())
        elif results.wflo:
            with open(results.wflo) as fp:
                body = fp.read()
                ct = 'application/javascript'
        elif results.scrp:
            with open(results.scrp) as fp:
                body = fp.read()
                ct = 'application/x-www-form-urlencoded'
        elif results.upgr:
            with open(results.upgr, 'rb') as fp:
                body = fp.read()
                ct = 'application/octet-stream'
        meth = results.m.upper()
        rcode, json_data = do_url(results.l, meth, results.u, results.p, body, ct)
        if results.r and meth == 'GET':
            json_recurse(results.l, results.u, results.p, json_data, rcode, [])
        else:
            print('Response Code', rcode, '\n')
            print(json.dumps(json_data, sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
