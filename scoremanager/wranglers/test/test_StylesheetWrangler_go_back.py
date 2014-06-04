# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_back_01():

    input_ = 'red~example~score y b q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_back_02():

    input_ = 'y b q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles