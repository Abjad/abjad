# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Editor__run_01():
    r'''Works to change clef name.
    '''

    target = Clef('alto')
    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'nm tenor done'
    editor._run(pending_user_input=input_)

    assert editor.target == Clef('tenor')


def test_Editor__run_02():
    r'''Works with unmodified tempo.
    '''

    target = Tempo()
    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'done'
    editor._run(pending_user_input=input_)

    assert editor.target is target


def test_Editor__run_03():
    r'''Works to change tempo duration with pair.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=Tempo(),
        )
    input_ = 'duration (1, 8) units 98 done'
    editor._run(pending_user_input=input_)

    assert editor.target == Tempo(Duration(1, 8), 98)


def test_Editor__run_04():
    r'''Works to change tempo duration with duration object.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=Tempo(),
        )
    input_ = 'duration Duration(1, 8) units 98 done'
    editor._run(pending_user_input=input_)

    assert editor.target == Tempo(Duration(1, 8), 98)