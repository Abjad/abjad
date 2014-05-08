# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerModuleWrangler_go_to_stylesheets_01():
    r'''Goes from score maker modules to score stylesheets.
    '''

    input_ = 'red~example~score k y q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker modules',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerModuleWrangler_go_to_stylesheets_02():
    r'''Goes from maker module library to stylesheet library.
    '''

    input_ = 'k y q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - maker modules',
        'Score manager - stylesheets',
        ]
    assert score_manager._transcript.titles == titles