# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_stylesheets_01():
    r'''From segments directory to stylesheets directory.
    '''

    input_ = 'red~example~score g y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_stylesheets_02():
    r'''Goes from segment library to stylesheet library.
    '''

    input_ = 'g y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - stylesheets',
        ]
    assert score_manager._transcript.titles == titles