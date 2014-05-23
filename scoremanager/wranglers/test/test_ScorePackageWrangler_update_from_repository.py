# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageWrangler_update_from_repository_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'rup <return> q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository