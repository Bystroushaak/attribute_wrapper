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


# Tests =======================================================================
class PrintWrapper(GenericWrapper):
    def download_handler(self, method, url, data):
        return "%s:%s:%s" % (method, url, str(data))


def test_wrapper():
    p = PrintWrapper("print")

    assert p.attribute.get() == "get:print/attribute:None"
