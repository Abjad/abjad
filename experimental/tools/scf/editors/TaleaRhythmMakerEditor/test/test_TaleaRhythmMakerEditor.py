from abjad.tools import rhythmmakertools
import scf


def test_TaleaRhythmMakerEditor_01():

    editor = scf.editors.TaleaRhythmMakerEditor()
    editor.run(user_input='2 16 [2, 3] [6] [-1, 2, -3, 4] q', is_autoadvancing=True)

    maker = rhythmmakertools.TaleaRhythmMaker([-1, 2, -3, 4], 16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    assert editor.target == maker
