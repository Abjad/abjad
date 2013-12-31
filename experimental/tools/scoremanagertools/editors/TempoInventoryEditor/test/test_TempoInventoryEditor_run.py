# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.indicatortools.Tempo import Tempo
from experimental import *


def test_TempoInventoryEditor_run_01():

    editor = scoremanagertools.editors.TempoInventoryEditor()
    editor._run(pending_user_input='q')
    assert editor.target == indicatortools.TempoInventory([])


def test_TempoInventoryEditor_run_02():

    editor = scoremanagertools.editors.TempoInventoryEditor()
    editor._run(pending_user_input='add ((1, 4), 60) add ((1, 4), 72) add ((1, 4), 84) q')
    assert editor.target == indicatortools.TempoInventory(
        [Tempo(Duration(1, 4), 60), Tempo(Duration(1, 4), 72), Tempo(Duration(1, 4), 84)])
