# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_stylesheets_01():
    r'''Goes from score distribution files to score stylesheets.
    '''

    input_ = 'red~example~score d y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_DistributionFileWrangler_go_to_stylesheets_02():
    r'''Goes from distribution file library to stylesheet library.
    '''

    input_ = 'd y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution files',
        'Abjad IDE - stylesheets',
        ]
    assert score_manager._transcript.titles == titles