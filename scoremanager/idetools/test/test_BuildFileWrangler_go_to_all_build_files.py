# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_all_build_files_01():
    r'''From score build files to all build files.
    '''

    input_ = 'red~example~score u U q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Abjad IDE - build depot',
        ]
    assert ide._transcript.titles == titles


def test_BuildFileWrangler_go_to_all_build_files_02():
    r'''From all build files to all build files.
    '''

    input_ = 'U U q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - build depot',
        'Abjad IDE - build depot',
        ]
    assert ide._transcript.titles == titles