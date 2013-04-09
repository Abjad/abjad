from abjad.tools import rhythmmakertools
import scftools


def test_OutputBurnishedTaleaRhythmMakerEditor_01():

    editor = scftools.editors.OutputBurnishedTaleaRhythmMakerEditor()
    editor.run(user_input='1 [1] 16 [2] [0] [-1] [0] [1] [1] q', is_autoadvancing=True)

    maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker([1], 16,
        prolation_addenda=[2],
        lefts=[0],
        middles=[-1],
        rights=[0],
        left_lengths=[1],
        right_lengths=[1],
        secondary_divisions=[],
        )

    assert editor.target == maker
