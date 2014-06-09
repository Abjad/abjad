# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.ide.Session()



def test_getters_01():
    r'''Regression test.
    '''

    getter = scoremanager.ide.getters.get_duration(
        'foo bar',
        session=session,
        )
    input_ = 'asdf (1, 16)'
    assert getter._run(input_=input_) == Duration(1, 16)


def test_getters_02():
    r'''Allow none.
    '''

    getter = scoremanager.ide.getters.get_duration(
        'foo bar',
        session=session,
        )
    input_ = 'None'
    assert getter._run(input_=input_) is None