# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_home_01():

    input_ = 'red~example~score k h q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerFileWrangler_go_home_02():

    input_ = 'k h q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles