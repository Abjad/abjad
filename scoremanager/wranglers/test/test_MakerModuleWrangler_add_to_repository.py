# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MakerModuleWrangler_add_to_repository_01():
    pytest.skip()

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_add_to_repository_test = True
    input_ = 'red~example~score k rad default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_add_to_repository