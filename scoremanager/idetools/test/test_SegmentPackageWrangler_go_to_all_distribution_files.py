# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_distribution_files_01():
    r'''From score segments to all distribution files.
    '''

    input_ = 'red~example~score g D q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Abjad IDE - distribution files',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_distribution_files_02():
    r'''From all segments to all distribution files.
    '''

    input_ = 'G D q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - distribution files',
        ]
    assert score_manager._transcript.titles == titles