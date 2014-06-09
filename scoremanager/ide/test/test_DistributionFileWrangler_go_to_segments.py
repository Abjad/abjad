# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_segments_01():
    r'''Goes from score distribution files to score segments.
    '''

    input_ = 'red~example~score d g q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles

    
def test_DistributionFileWrangler_go_to_segments_02():
    r'''Goes from distribution file library to segment library.
    '''

    input_ = 'd g q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution files',
        'Abjad IDE - segments',
        ]
    assert score_manager._transcript.titles == titles