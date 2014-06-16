# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_distribution_files_01():
    r'''From score maker files to all distribution files.
    '''

    input_ = 'red~example~score k D q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Abjad IDE - distribution files',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_distribution_files_02():
    r'''From all maker files to all distribution files.
    '''

    input_ = 'K D q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Abjad IDE - distribution files',
        ]
    assert score_manager._transcript.titles == titles