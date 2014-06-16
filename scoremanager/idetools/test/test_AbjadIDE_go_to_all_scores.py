# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_scores_01():
    r'''From library to all scores.
    '''

    input_ = '** S q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles