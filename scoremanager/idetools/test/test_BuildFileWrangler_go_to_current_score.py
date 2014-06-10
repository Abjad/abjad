# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_current_score_01():

    input_ = 'red~example~score u s q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_BuildFileWrangler_go_to_current_score_02():

    input_ = 'u s q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        'Abjad IDE - build files',
        ]
    assert score_manager._transcript.titles == titles