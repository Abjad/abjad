# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_maker_files_01():
    r'''From distribution directory to makers depot.
    '''

    input_ = 'red~example~score d K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_maker_files_02():
    r'''From distribution depot to makers depot.
    '''

    input_ = 'D K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - distribution depot',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles