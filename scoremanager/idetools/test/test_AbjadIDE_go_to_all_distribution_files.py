# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_distribution_files_01():
    r'''From top level to all distribution files.
    '''

    input_ = 'hh dd q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - home',
        'Abjad IDE - distribution depot',
        ]
    assert ide._transcript.titles == titles