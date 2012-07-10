from abjad.cfg.cfg import ABJADPATH
from abjad.demos.desordre import helpers
import os


def test_demos_desordre_01():

    pitches_filepath = os.path.join(ABJADPATH, 'demos', 'desordre', 'desordre_pitches.txt')

    pitches = helpers.load_desordre_pitches(pitches_filepath)

    score = helpers.desordre_build(pitches)

    assert 0 < score.prolated_duration
