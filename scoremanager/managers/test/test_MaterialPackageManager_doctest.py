# -*- encoding: utf-8 -*-
import pytest
pytest.skip('make me work')
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_doctest_01():

    input_ = 'red~example~score m tempo~inventory pyd default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.titles[-3] == 'Running doctest ...'