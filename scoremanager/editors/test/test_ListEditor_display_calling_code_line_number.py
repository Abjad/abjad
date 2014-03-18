# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListEditor_display_calling_code_line_number_01():

    score_manager = scoremanager.core.ScoreManager(is_test=False)
    input_ = 'red~example~score setup instrumentation scl q'
    score_manager._run(pending_user_input=input_)
    string = '       file: ListEditor.py'

    assert score_manager._transcript.last_title == string
