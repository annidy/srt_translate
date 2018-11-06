#!/usr/bin/env python
# coding: UTF-8
#
# this program is designed to translate to chinese only.
from __future__ import unicode_literals
import sys
import re
import threading
import logging
from translator import BaseTranslator
from translator import cache
logging.basicConfig(level=logging.DEBUG)

import json
from textwrap import wrap
try:
    import urllib2 as request
    from urllib import quote_plus
    from urllib2 import HTTPError
except:
    from urllib import request
    from urllib.parse import quote_plus
    from urllib import HTTPError


class YandexTranslator(BaseTranslator):
    def translate(self, source):
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        return ' '.join(self._get_translation(s) for s in self.source_list)

    def _get_translation(self, source):
        json5 = self._get_json(source)
        data = json.loads(json5)
        # {u'lang': u'ko-zh', u'text': [u'\u963f\u62c9\u4f2f\u5de5\u4e1a\u5316\u7ec4\u7ec7\u53f8'], u'code': 200}
        translation = data['text'][0]
        return translation

    def _get_json(self, source):
        escaped_source = quote_plus(source.encode('utf8'))
        headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                   (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        api_url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&text=%s&lang=%s-%s"
        req = request.Request(url=api_url % (self.key, escaped_source, self.from_lang, self.to_lang),
                              headers=headers)

        r = request.urlopen(req)
        return r.read().decode('utf-8')