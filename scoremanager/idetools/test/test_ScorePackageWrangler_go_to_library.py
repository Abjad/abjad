# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_library_01():
    r'''From all scores to library.
    '''

    input_ = '** q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE',
        ]
    assert score_manager._transcript.titles == titles