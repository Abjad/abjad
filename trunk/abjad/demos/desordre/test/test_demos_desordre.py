from abjad import ABJCFG
from abjad.demos.desordre import helpers
import os


def test_demos_desordre_01():

    pitches_filepath = os.path.join(ABJCFG.ABJAD_PATH, 'demos', 'desordre', 'desordre_pitches.txt')

    pitches = helpers.load_desordre_pitches(pitches_filepath)

    score = helpers.desordre_build(pitches)

    assert 0 < score.prolated_duration
