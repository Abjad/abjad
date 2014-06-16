# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_all_distribution_files_01():
    r'''From score stylesheets to all distribution files.
    '''

    input_ = 'red~example~score y D q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Abjad IDE - distribution files',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_all_distribution_files_02():
    r'''From all stylesheets to all distribution files.
    '''

    input_ = 'Y D q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Abjad IDE - distribution files',
        ]
    assert score_manager._transcript.titles == titles