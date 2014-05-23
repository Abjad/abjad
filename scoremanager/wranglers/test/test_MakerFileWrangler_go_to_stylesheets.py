# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerFileWrangler_go_to_stylesheets_01():
    r'''Goes from score maker files to score stylesheets.
    '''

    input_ = 'red~example~score k y q'
    score_manager._run(input_=input_)
    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerFileWrangler_go_to_stylesheets_02():
    r'''Goes from maker file library to stylesheet library.
    '''

    input_ = 'k y q'
    score_manager._run(input_=input_)
    titles = [
        'Score Manager - scores',
        'Score Manager - maker files',
        'Score Manager - stylesheets',
        ]
    assert score_manager._transcript.titles == titles