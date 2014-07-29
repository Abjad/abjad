# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_home_01():
    r'''From score build files to library.
    '''

    input_ = 'red~example~score u hh q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles


def test_BuildFileWrangler_go_home_02():
    r'''From all build files to library.
    '''

    input_ = 'uu hh q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles