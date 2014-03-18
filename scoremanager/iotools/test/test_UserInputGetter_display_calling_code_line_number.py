# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_display_calling_code_line_number_01():
    '''Nontest session turns on source code tracking.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=False)
    input_ = 'red~example~score setup instrumentation mv scl q'
    score_manager._run(pending_user_input=input_)

    string = '       file: ListEditor.py'
    assert score_manager._transcript.entries[-2].lines[0] == string

    string = '     method: move_item'
    assert score_manager._transcript.entries[-2].lines[1] == string
