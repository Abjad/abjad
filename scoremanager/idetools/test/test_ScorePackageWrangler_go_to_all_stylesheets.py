# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_all_stylesheets_01():
    r'''From all scores to all stylesheets.
    '''

    input_ = 'Y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        ]
    assert score_manager._transcript.titles == titles