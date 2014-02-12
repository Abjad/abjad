# -*- encoding: utf-8 -*-
from experimental import *


def test_TempoEditor_run_01():

    editor = scoremanager.editors.TempoEditor()
    editor._run(pending_user_input='q')
    assert editor.target == Tempo()


def test_TempoEditor_run_02():

    editor = scoremanager.editors.TempoEditor()
    editor._run(pending_user_input='duration (1, 8) units 98 q')
    assert editor.target == indicatortools.Tempo(Duration(1, 8), 98)


def test_TempoEditor_run_03():

    editor = scoremanager.editors.TempoEditor()
    editor._run(pending_user_input='duration Duration(1, 8) units 98 q')
    assert editor.target == indicatortools.Tempo(Duration(1, 8), 98)
