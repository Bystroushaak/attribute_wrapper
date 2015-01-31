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


# Fixtures ====================================================================
@pytest.fixture
def p():
    return ReturnWrapper("http://kitakitsune.org")


@pytest.fixture
def r():
    return ReturnWrapper("return")


# Tests =======================================================================
def test_wrapper():
    p = ReturnWrapper("return")

    assert p.attribute.get() == ("get", "return/attribute", None)


def test_http_url(p):
    assert p.get() == ("get", "http://kitakitsune.org", None)
    assert p.attr.get() == ("get", "http://kitakitsune.org/attr", None)


def test_other_methods(p):
    assert p.post() == ("post", "http://kitakitsune.org", None)
    assert p.update() == ("update", "http://kitakitsune.org", None)

    assert p.attr.post() == ("post", "http://kitakitsune.org/attr", None)
    assert p.attr.update() == ("update", "http://kitakitsune.org/attr", None)


def test_no_method_given(p):
    with pytest.raises(ValueError):
        assert p()


def test_multiple_attributes(p):
    assert p.m() == ("m", "http://kitakitsune.org", None)
    assert p.b.m() == ("m", "http://kitakitsune.org/b", None)
    assert p.c.b.m() == ("m", "http://kitakitsune.org/c/b", None)
    assert p.d.c.b.m() == ("m", "http://kitakitsune.org/d/c/b", None)


def test_data(r):
    assert r.m(key="val") == ("m", "return", {"key": "val"})
    assert r.m(k="v", x=1) == ("m", "return", {"k": "v", "x": 1})
    assert r.b.m(k="v", x=1) == ("m", "return/b", {"k": "v", "x": 1})


def test_special_characters(r):
    assert r.azgabash__dot__txt.m() == ("m", "return/azgabash.txt", None)
    assert r.azgabash__slash__txt.m() == ("m", "return/azgabash/txt", None)
    assert r.azgabash__dash__txt.m() == ("m", "return/azgabash-txt", None)

    # test multiple special characters in one attribute
    assert r.aa__dash__aa__dot__txt.m() == ("m", "return/aa-aa.txt", None)

    # test with multiple attributes
    assert r.__dot__.__dash__.__slash__.m() == ("m", "return/./-//", None)


def test_automatic_suffix(p):
    p.suffix = ".txt"

    assert p.m() == ("m", "http://kitakitsune.org", None)  # no suffix
    assert p.file.m() == ("m", "http://kitakitsune.org/file.txt", None)

    # test also constructor
    p = ReturnWrapper("http://kitakitsune.org", suffix=".txt")

    assert p.m() == ("m", "http://kitakitsune.org", None)  # no suffix
    assert p.file.m() == ("m", "http://kitakitsune.org/file.txt", None)
    assert p.raw.file.m() == ("m", "http://kitakitsune.org/raw/file.txt", None)


def test_underscore_method(r):
    assert r._("a/~anyt$ů§hing").m() == ("m", "return/a/~anyt$ů§hing", None)
