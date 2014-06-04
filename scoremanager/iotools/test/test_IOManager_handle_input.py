# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager_handle_input_01():
    r'''Command repetition works.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    input_ = '>> . . . q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        'Red Example Score (2013)',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles