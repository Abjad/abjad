# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_go_home_01():

    input_ = 'red~example~score u h q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles


def test_BuildFileWrangler_go_home_02():

    input_ = 'u h q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles