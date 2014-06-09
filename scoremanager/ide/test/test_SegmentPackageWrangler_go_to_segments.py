# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_segments_01():
    r'''Goes from score segments to score segments.
    '''

    input_ = 'red~example~score g g q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_segments_02():
    r'''Goes from segment library to segment library.
    '''

    input_ = 'g g q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - segments',
        ]
    assert score_manager._transcript.titles == titles