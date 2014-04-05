# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
from scoremanager import getters


def test_getters_01():
    r'''Regression test.
    '''

    getter = getters.get_duration('foo bar')
    input_ = 'asdf (1, 16)'
    assert getter._run(pending_user_input=input_) == Duration(1, 16)


def test_getters_02():
    r'''Allow none.
    '''

    getter = getters.get_duration('foo bar')
    input_ = 'None'
    assert getter._run(pending_user_input=input_) is None