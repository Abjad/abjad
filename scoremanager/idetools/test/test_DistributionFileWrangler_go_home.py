# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_home_01():
    r'''From distribution directory.
    '''

    input_ = 'red~example~score d H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles


def test_DistributionFileWrangler_go_home_02():
    r'''From distribution depot.
    '''

    input_ = 'D H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - distribution depot',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles