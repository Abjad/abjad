# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_go_to_stylesheets_01():
    r'''Goes from score stylesheets to score stylesheets.
    '''

    input_ = 'red~example~score y y q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_stylesheets_02():
    r'''Goes from stylesheet library to stylesheet library.
    '''

    input_ = 'y y q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - scores',
        'Score manager - stylesheets',
        'Score manager - stylesheets',
        ]
    assert score_manager._transcript.titles == titles