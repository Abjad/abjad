# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_maker_files_01():
    r'''From top level to all maker files.
    '''

    input_ = 'hh kk q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - home',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles