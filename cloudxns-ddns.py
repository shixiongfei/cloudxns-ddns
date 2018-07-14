#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  Copyright (c) 2018 Xiongfei Shi <jenson.shixf@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.

        http://shixf.com/
'''

import json
import time
import hashlib

try:
    # for py3
    from urllib.request import urlopen, Request, HTTPError, URLError
    from urllib.parse import urlencode
except:
    # for py2
    from urllib2 import urlopen, Request, HTTPError, URLError
    from urllib import urlencode


api_key = 'API_KEY'
api_secret = 'API_SECRET'
domains = [
    {
        'domain': 'example.com',
        'sub_domain': ['@', '*']
    }
]


api_url = 'https://www.cloudxns.net/api2/ddns'
now_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())

for domain in domains:
    for host in domain['sub_domain']:
        postdata = {
            'domain': '{0}.{1}'.format(host, domain['domain']) if host != '@' else domain['domain'],
        }

        raw = api_key + api_url + json.dumps(postdata) + now_time + api_secret
        sign = hashlib.md5(raw.encode()).hexdigest()

        try:
            req = Request(api_url, data=json.dumps(postdata).encode())
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'CloudXNS DDNS/1.0 (jenson.shixf@gmail.com)')
            req.add_header('API-KEY', api_key)
            req.add_header('API-REQUEST-DATE', now_time)
            req.add_header('API-HMAC', sign)
            req.add_header('API-FORMAT', 'json')
            req.get_method = lambda: 'POST'
            urlItem = urlopen(req, timeout=10)
            print(urlItem.read())
            urlItem.close()
        except URLError as e:
            print('URLError', e.reason)
        except HTTPError as e:
            print('HTTPError', e.reason)
        except Exception as e:
            print('FetchError', 'HTTP data fetch error: {0}'.format(e))
