# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListEditor_display_calling_code_line_number_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    string = 'red~example~score setup instrumentation scl q'
    score_manager._run(pending_user_input=string, is_test=False)
    string = '       file: ListEditor.py'

    assert score_manager._transcript.last_title == string
