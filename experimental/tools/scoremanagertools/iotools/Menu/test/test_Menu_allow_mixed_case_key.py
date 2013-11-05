# -*- encoding: utf-8 -*-
from experimental import *
import pytest


def test_Menu_allow_mixed_case_key_01():
    r'''Allow mixed case 'home' key.
    '''
    pytest.skip('remove custom score name.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input="L'arch home q")
    assert score_manager.session.io_transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input="L'arch HOME q")
    assert score_manager.session.io_transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input="L'arch hOmE q")
    assert score_manager.session.io_transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input="L'arch hOME q")
    assert score_manager.session.io_transcript.signature == (6, (0, 4))
