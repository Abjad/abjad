# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_home_01():
    r'''From makers directory.
    '''

    input_ = 'red~example~score k H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles


def test_MakerFileWrangler_go_home_02():
    r'''From makers depot.
    '''

    input_ = 'K H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - makers depot',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles