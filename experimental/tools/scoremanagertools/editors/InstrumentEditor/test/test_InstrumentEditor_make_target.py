from experimental import *
from abjad import *


def test_InstrumentEditor_make_target_01():

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input='cel q')
    assert editor.target == instrumenttools.Cello()
