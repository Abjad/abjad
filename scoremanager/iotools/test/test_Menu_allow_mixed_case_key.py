# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_Menu_allow_mixed_case_key_01():
    r'''Allow mixed case commands.
    '''
    pytest.skip('FIXME')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input="Red~Example~Score h q")
    assert score_manager._session.transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input="red~example~score HOME q")
    assert score_manager._session.transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input="red~example~score hOmE q")
    assert score_manager._session.transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input="red~example~score hOME q")
    assert score_manager._session.transcript.signature == (6, (0, 4))
