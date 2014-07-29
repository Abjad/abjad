# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_all_maker_files_01():
    r'''From score build files to all maker files.
    '''

    input_ = 'red~example~score u kk q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles


def test_BuildFileWrangler_go_to_all_maker_files_02():
    r'''From all build files to all maker files.
    '''

    input_ = 'uu kk q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles