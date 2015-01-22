#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import json
import requests
from os.path import join


# Variables ===================================================================



# Functions & classes =========================================================
class Recurser(object):
    def __init__(self, url, parent=None, suffix=None):
        self.url = url
        self.parent = parent
        self.suffix = suffix

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError("You can use only *args OR **kwargs!")

        url = self._get_url(True)

        # add suffix to non-domain urls
        if self.parent.parent and self.suffix:
            url += self.suffix

        # params = args if args else kwargs
        return self.url, url, args

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
        if not self.parent:
            return self.url

        # last call (called=True) is used for determining http method
        if called:
            return self.parent._get_url()
        else:
            return join(self.parent._get_url(), self.url)

    def __getattr__(self, attr):
        return self.__dict__.get(
            attr,
            Recurser(attr, self, self.suffix)
        )

r = Recurser("http://kitakitsune.org", suffix=".html")
print r.get()
print r.azgabash.asd.last__dot__fm.get("asd")