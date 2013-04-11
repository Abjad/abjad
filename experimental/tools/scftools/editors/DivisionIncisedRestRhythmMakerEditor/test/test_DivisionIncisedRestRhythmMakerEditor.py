from abjad.tools import rhythmmakertools
from experimental import *


def test_DivisionIncisedRestRhythmMakerEditor_01():

    editor = scftools.editors.DivisionIncisedRestRhythmMakerEditor()
    editor.run(user_input='1 [8] [0, 1] [1] [1] 32 q', is_autoadvancing=True)

    maker = rhythmmakertools.DivisionIncisedRestRhythmMaker([8], [0, 1], [1], [1], 32)

    assert editor.target == maker
