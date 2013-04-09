from abjad.tools import rhythmmakertools
from experimental.tools import handlertools
import scftools


def test_NoteRhythmMakerEditor_01():

    editor = scftools.editors.NoteRhythmMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker
