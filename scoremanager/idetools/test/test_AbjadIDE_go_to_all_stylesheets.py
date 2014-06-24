# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_stylesheets_01():
    r'''From top level to all stylesheets.
    '''

    input_ = '** Y q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE',
        'Abjad IDE - stylesheets',
        ]
    assert score_manager._transcript.titles == titles