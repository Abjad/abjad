# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_score_segments_01():
    r'''Goes from score stylesheets to score segments.
    '''

    input_ = 'red~example~score y g q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_score_segments_02():
    r'''Goes from stylesheets library to segments library.
    '''

    input_ = 'Y G q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Abjad IDE - segments',
        ]
    assert score_manager._transcript.titles == titles