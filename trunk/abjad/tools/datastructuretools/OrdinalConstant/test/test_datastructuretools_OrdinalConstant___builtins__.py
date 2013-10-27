# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_datastructuretools_OrdinalConstant___builtins___01():

    assert Left < Right
    assert Down < Center < Up


def test_datastructuretools_OrdinalConstant___builtins___02():

    assert py.test.raises(Exception, 'Down < Right')
