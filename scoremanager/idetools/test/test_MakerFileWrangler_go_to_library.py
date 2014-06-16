# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_library_01():
    r'''From score maker files to library.
    '''

    input_ = 'red~example~score k ** q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Abjad IDE',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerFileWrangler_go_to_library_02():
    r'''From all maker files to library.
    '''

    input_ = 'K ** q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Abjad IDE',
        ]
    assert score_manager._transcript.titles == titles