from abjad import *
from experimental.tools.scoremanagertools import getters


def test_getters_01():
    '''Regression test.
    '''

    getter = getters.get_duration('foo bar')
    assert getter.run(user_input='asdf (1, 16)') == Duration(1, 16)


def test_getters_02():
    '''Allow none.
    '''

    getter = getters.get_duration('foo bar')
    assert getter.run(user_input='None') is None
