# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_top_level_01():
    r'''From top level to library.
    '''

    input_ = 'H H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE',
        'Abjad IDE',
        ]
    assert ide._transcript.titles == titles