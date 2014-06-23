# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_score_segments_01():
    r'''From materials directory to build directory.
    '''

    input_ = 'G q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        ]
    assert score_manager._transcript.titles == titles