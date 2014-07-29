# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_build_files_01():
    r'''From distribution directory to build depot.
    '''

    input_ = 'red~example~score d uu q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution directory',
        'Abjad IDE - build depot',
        ]
    assert ide._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_build_files_02():
    r'''From distribution depot to build depot.
    '''

    input_ = 'dd uu q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution depot',
        'Abjad IDE - build depot',
        ]
    assert ide._transcript.titles == titles