# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_UserInputGetter_display_calling_code_line_number_01():
    pytest.skip('make UserInputGetter keep track of source code.')

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation mv scl q'
    score_manager._run(pending_user_input=string, is_test=False)
    string = '       file: UserInputGetter.py'

    assert score_manager._transcript.last_title == string
