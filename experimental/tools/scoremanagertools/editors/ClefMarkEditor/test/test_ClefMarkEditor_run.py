from abjad.tools import contexttools
from experimental import *


def test_ClefMarkEditor_run_01():

    editor = scoremanagertools.editors.ClefMarkEditor()
    editor._run(user_input='clef treble done')

    clef_mark = contexttools.ClefMark('treble')
    assert editor.target == clef_mark
