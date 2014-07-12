# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_build_files_01():
    r'''From top level to all build files.
    '''

    input_ = 'H U q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - home',
        'Abjad IDE - build depot',
        ]
    assert ide._transcript.titles == titles