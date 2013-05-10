from abjad.tools import rhythmmakertools
from experimental.tools import handlertools
from experimental import *


def test_NoteRhythmMakerEditor_01():

    editor = scoremanagertools.editors.NoteRhythmMakerEditor()
    editor._run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker
