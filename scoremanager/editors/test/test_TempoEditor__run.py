# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_TempoEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.TempoEditor(session=session)
    input_ = 'q'
    editor._run(pending_user_input=input_)
    assert editor.target == Tempo()


def test_TempoEditor__run_02():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.TempoEditor(session=session)
    input_ = 'duration (1, 8) units 98 q'
    editor._run(pending_user_input=input_)
    assert editor.target == indicatortools.Tempo(Duration(1, 8), 98)


def test_TempoEditor__run_03():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.TempoEditor(session=session)
    input_ = 'duration Duration(1, 8) units 98 q'
    editor._run(pending_user_input=input_)
    assert editor.target == indicatortools.Tempo(Duration(1, 8), 98)
