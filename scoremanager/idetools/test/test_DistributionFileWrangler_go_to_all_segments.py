# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_segments_01():
    r'''From distribution directory to segments depot.
    '''

    input_ = 'red~example~score d G q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_segments_02():
    r'''From distribution depot to segments depot.
    '''

    input_ = 'D G q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - distribution depot',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles