# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_next_score_01():

    input_ = 'red~example~score k >> q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerFileWrangler_go_to_next_score_02():

    input_ = 'k >> q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles