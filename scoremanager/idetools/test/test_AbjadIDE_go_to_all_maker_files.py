# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_all_maker_files_01():
    r'''From library to all maker files.
    '''

    input_ = '** K q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE',
        'Abjad IDE - maker files',
        ]
    assert score_manager._transcript.titles == titles