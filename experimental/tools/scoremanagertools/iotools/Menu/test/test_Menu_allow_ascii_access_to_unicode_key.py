# -*- encoding: utf-8 -*-
from experimental import *
import pytest


def test_Menu_allow_ascii_access_to_unicode_key_01():
    pytest.skip('fix eventually with new score name or something.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='Étude q')
    assert score_manager.session.io_transcript.signature == (4,)

    score_manager._run(pending_user_input='étude q')
    assert score_manager.session.io_transcript.signature == (4,)

    score_manager._run(pending_user_input='Etude q')
    assert score_manager.session.io_transcript.signature == (4,)

    score_manager._run(pending_user_input='etude q')
    assert score_manager.session.io_transcript.signature == (4,)
