# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_Menu_allow_ascii_access_to_unicode_key_01():
    pytest.skip('fix eventually with new score name or something.')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='Étude q')
    assert score_manager._session.io_transcript.signature == (4,)

    score_manager._run(pending_user_input='étude q')
    assert score_manager._session.io_transcript.signature == (4,)

    score_manager._run(pending_user_input='Etude q')
    assert score_manager._session.io_transcript.signature == (4,)

    score_manager._run(pending_user_input='etude q')
    assert score_manager._session.io_transcript.signature == (4,)
