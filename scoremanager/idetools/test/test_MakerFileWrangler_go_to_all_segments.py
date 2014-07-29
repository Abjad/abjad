# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_segments_01():
    r'''From makers directory to segments depot.
    '''

    input_ = 'red~example~score k gg q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_segments_02():
    r'''From makers depot to segments depot.
    '''

    input_ = 'kk gg q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - makers depot',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles