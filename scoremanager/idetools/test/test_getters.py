# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session()



def test_getters_01():
    r'''Regression test.
    '''

    getter = scoremanager.idetools.getters.get_duration(
        'foo bar',
        session=session,
        )
    getter._session._pending_input = 'asdf (1, 16)'
    assert getter._run() == Duration(1, 16)


def test_getters_02():
    r'''Allow none.
    '''

    getter = scoremanager.idetools.getters.get_duration(
        'foo bar',
        session=session,
        )
    getter._session._pending_input = 'None'
    assert getter._run() is None