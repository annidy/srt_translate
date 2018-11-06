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


class MymemoryTranslator(BaseTranslator):

    def translate(self, source):
        if self.from_lang == self.to_lang:
            return source
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        return ' '.join(self._get_translation(s) for s in self.source_list)

    def _get_translation(self, source):
        json5 = self._get_json(source)
        data = json.loads(json5)
        translation = data['responseData']['translatedText']
        print(translation)
        if not isinstance(translation, bool):
            return translation
        else:
            matches = data['matches']
            for match in matches:
                if not isinstance(match['translation'], bool):
                    next_best_match = match['translation']
                    break
            return next_best_match

    def _get_json(self, source):
        escaped_source = quote_plus(source.encode('utf8'))
        headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                   (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        api_url = "http://mymemory.translated.net/api/get?q=%s&user=annidy&key=f831798351c5893f9055&langpair=%s|%s"
        req = request.Request(url=api_url % (escaped_source, self.from_lang, self.to_lang),
                              headers=headers)

        r = request.urlopen(req)
        return r.read().decode('utf-8')