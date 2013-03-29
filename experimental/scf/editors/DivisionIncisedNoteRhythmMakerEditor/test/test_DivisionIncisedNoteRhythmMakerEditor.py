from abjad.tools import rhythmmakertools
import scf


def test_DivisionIncisedNoteRhythmMakerEditor_01():

    editor = scf.editors.DivisionIncisedNoteRhythmMakerEditor()
    editor.run(user_input='1 [-8] [0, 1] [-1] [1] 32 q', is_autoadvancing=True)

    maker = rhythmmakertools.DivisionIncisedNoteRhythmMaker([-8], [0, 1], [-1], [1], 32)

    assert editor.target == maker
