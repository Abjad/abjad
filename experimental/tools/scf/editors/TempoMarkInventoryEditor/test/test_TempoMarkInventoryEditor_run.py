from abjad import *
from abjad.tools.contexttools.TempoMark import TempoMark
import scf


def test_TempoMarkInventoryEditor_run_01():

    editor = scf.editors.TempoMarkInventoryEditor()
    editor.run(user_input='q')
    assert editor.target == contexttools.TempoMarkInventory([])


def test_TempoMarkInventoryEditor_run_02():

    editor = scf.editors.TempoMarkInventoryEditor()
    editor.run(user_input='add ((1, 4), 60) add ((1, 4), 72) add ((1, 4), 84) q')
    assert editor.target == contexttools.TempoMarkInventory(
        [TempoMark(Duration(1, 4), 60), TempoMark(Duration(1, 4), 72), TempoMark(Duration(1, 4), 84)])
