# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_stylesheets_01():
    r'''From top level to all stylesheets.
    '''

    input_ = 'hh yy q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - home',
        'Abjad IDE - stylesheets depot',
        ]
    assert ide._transcript.titles == titles