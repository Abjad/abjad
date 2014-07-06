# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_segments_01():
    r'''From top level to all segments.
    '''

    input_ = 'H G q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE',
        'Abjad IDE - segments',
        ]
    assert ide._transcript.titles == titles