from abjad.tools import rhythmmakertools
from experimental import *


def test_DivisionIncisedNoteRhythmMakerEditor_01():

    editor = scoremanagertools.editors.DivisionIncisedNoteRhythmMakerEditor()
    editor.run(user_input='1 [-8] [0, 1] [-1] [1] 32 q', is_autoadvancing=True)

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker([-8], [0, 1], [-1], [1], 32)

    assert editor.target == maker
