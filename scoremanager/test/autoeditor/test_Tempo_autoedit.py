# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Tempo_autoedit_01():
    r'''Creates default tempo.
    '''

    target = Tempo()
    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target is target


def test_Tempo_autoedit_02():
    r'''Edits tempo duration with pair.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Tempo(),
        )
    input_ = 'Duration (1, 8) units 98 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Tempo(Duration(1, 8), 98)


def test_Tempo_autoedit_03():
    r'''Edits tempo duration with duration object.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Tempo(),
        )
    input_ = 'Duration Duration(1, 8) units 98 done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Tempo(Duration(1, 8), 98)

