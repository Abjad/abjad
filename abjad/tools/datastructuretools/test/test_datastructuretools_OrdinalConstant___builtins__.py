# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_datastructuretools_OrdinalConstant___builtins___01():

    assert Left < Right
    assert Down < Center < Up


def test_datastructuretools_OrdinalConstant___builtins___02():

    assert pytest.raises(Exception, 'Down < Right')
