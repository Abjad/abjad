# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_score_materials_01():
    r'''Goes from score distribution files to score materials.
    '''

    input_ = 'red~example~score d m q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_DistributionFileWrangler_go_to_score_materials_02():
    r'''Goes from distribution file library to material library.
    '''

    input_ = 'D M q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution files',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles