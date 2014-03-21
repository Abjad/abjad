# -*- encoding: utf-8 -*-
import pytest
pytest.skip()
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_add_to_repository_01():
    r'''Works in score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_add_to_repository_test = True
    input_ = 'red~example~score m rad default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_add_to_repository


def test_MaterialPackageWrangler_add_to_repository_02():
    r'''Works in library.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_add_to_repository_test = True
    input_ = 'lmm rad default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._session._attempted_to_add_to_repository