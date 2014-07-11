# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_home_01():
    r'''From score maker files to library.
    '''

    input_ = 'red~example~score k H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles


def test_MakerFileWrangler_go_home_02():
    r'''From all maker files to library.
    '''

    input_ = 'K H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles