# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager__handle_input_01():
    r'''Command repetition works.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '>> . . . q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - scores',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        'Red Example Score (2013)',
        'Blue Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles