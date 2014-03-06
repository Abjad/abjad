# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip after where automatically toggles where-tracking.')


def test_UserInputGetter_where_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation mv where q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (11,)
