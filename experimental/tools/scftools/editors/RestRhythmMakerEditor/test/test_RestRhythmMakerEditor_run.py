from abjad.tools import rhythmmakertools
from experimental import *


def test_RestRhythmMakerEditor_run_01():

    editor = scftools.editors.RestRhythmMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.RestRhythmMaker()

    assert editor.target == maker
