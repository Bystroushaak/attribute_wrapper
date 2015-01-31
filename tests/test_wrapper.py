#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys

import pytest

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


def test_other_methods():
    p = ReturnWrapper("http://kitakitsune.org")

    assert p.post() == ("post", "http://kitakitsune.org", None)
    assert p.update() == ("update", "http://kitakitsune.org", None)

    assert p.attr.post() == ("post", "http://kitakitsune.org/attr", None)
    assert p.attr.update() == ("update", "http://kitakitsune.org/attr", None)


def test_no_method_given():
    p = ReturnWrapper("http://kitakitsune.org")

    with pytest.raises(ValueError):
        assert p() == ("a", "http://kitakitsune.org", None)


def test_multiple_attributes():
    p = ReturnWrapper("http://kitakitsune.org")

    assert p.a() == ("a", "http://kitakitsune.org", None)
    assert p.b.a() == ("a", "http://kitakitsune.org/b", None)
    assert p.c.b.a() == ("a", "http://kitakitsune.org/c/b", None)
    assert p.d.c.b.a() == ("a", "http://kitakitsune.org/d/c/b", None)
