# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_score_stylesheets_01():
    r'''Goes from score stylesheets to score stylesheets.
    '''

    input_ = 'red~example~score y y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles