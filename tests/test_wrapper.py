#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys

sys.path.insert(0, "src")
sys.path.insert(0, "../src")

from attribute_wrapper import GenericWrapper


# Classes =====================================================================
class ReturnWrapper(GenericWrapper):
    def download_handler(self, method, url, data):
        return (method, url, data)


# Tests =======================================================================
def test_wrapper():
    p = ReturnWrapper("return")

    assert p.attribute.get() == ("get", "return/attribute", None)


def test_http_url():
    p = ReturnWrapper("http://kitakitsune.org")

    assert p.get() == ("get", "http://kitakitsune.org", None)
    assert p.attr.get() == ("get", "http://kitakitsune.org/attr", None)
