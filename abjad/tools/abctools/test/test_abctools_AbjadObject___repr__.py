# -*- coding: utf-8 -*-
from abjad import *


def test_abctools_AbjadObject___repr___01():

    class Foo(abctools.AbjadObject):
        def __init__(self, x, y, flavor=None):
            tmp_1 = 'foo'
            self.x = x
            self.y = y
            self.flavor = flavor
            tmp_2 = 'bar'

    assert repr(Foo(7, 8)) == 'Foo(7, 8)'
    assert repr(Foo(7, 8, 'cherry')) == "Foo(7, 8, flavor='cherry')"


def test_abctools_AbjadObject___repr___02():
    r'''Repr suppresses class methods to avoid recursive repr.
    '''

    class Foo(abctools.AbjadObject):
        def __init__(self, x, y, helper=None):
            tmp_1 = 'foo'
            self.x = x
            self.y = y
            self.helper = helper or self.do_stuff
            tmp_2 = 'bar'
        def do_stuff(self):
            pass

    assert repr(Foo(7, 8)) == 'Foo(7, 8)'
