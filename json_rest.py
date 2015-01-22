#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import json
import requests
from os.path import join


# Functions & classes =========================================================
def http_handler(method, url, data):
    resp = requests.request(method, url, params=data)

    return resp.text


def json_handler(method, url, data):
    if data:
        data = json.dumps(data)

    resp = requests.request(method, url, data=data)

    return json.loads(resp.text)


class JSONWrapper(object):
    def __init__(self, url, parent=None, suffix=None):
        self.url = url
        self.parent = parent
        self.suffix = suffix

        # get specials from parent if defined
        self.specials = self._get_root().specials if self.parent else {
            "__dot__": ".",
            "__slash__": "/",
            "__dash__": "-",
        }
        self.download_handler = json_handler

    def __call__(self, **kwargs):
        # if args and kwargs:
            # raise ValueError("You can use only *args OR **kwargs!")

        url = self._get_url(True)
        url = self._replace_specials(url)

        # add suffix to non-domain urls
        if self.parent.parent and self.suffix:
            url += self.suffix

        # params = args if args else kwargs
        return self.download_handler(
            method=self.url,  # this is the last part of the attribute access
            url=url,
            data=kwargs if kwargs else None,
        )

    def _replace_specials(self, url):
        """
        In `url` replace keys from :attr:`specials` with correspondings vals.

        Args:
            url (str): String where the values are replaced.

        Returns:
            str: Updated string.
        """
        for key, val in self.specials.iteritems():
            url = url.replace(key, val)

        return url

    def _get_root(self):
        """
        Get root object from the hierarchy.

        Returns:
            obj: :class:`Recurser` instance of the root object.
        """
        if self.parent:
            return self.parent._get_root()

        return self

    def _get_url(self, called=False):
        """
        Compose url from self and all previous items in linked list.

        Args:
            called (bool, default False): Switch to let the function knows,
                   that it should ignore the last part of the URL, which is
                   method type.

        Returns:
            str: Composed URL.
        """
        if not self.parent:
            return self.url

        # last call (called=True) is used for determining http method
        if called:
            return self.parent._get_url()
        else:
            return join(self.parent._get_url(), self.url)

    def __getattr__(self, attr):
        """
        Take care of URL composition.
        """
        return self.__dict__.get(
            attr,
            self.__class__(attr, self, self.suffix)
        )


class HTTPWrapper(JSONWrapper):
    def __init__(self, *args, **kwargs):
        super(HTTPWrapper, self).__init__(*args, **kwargs)
        self.download_handler = http_handler



r = HTTPWrapper("http://kitakitsune.org", suffix=".html")
r.get()
# print r.azgabash.asd.last__dot__fm.get("asd")