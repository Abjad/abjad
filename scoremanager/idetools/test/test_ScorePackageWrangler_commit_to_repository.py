# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageWrangler_commit_to_repository_01():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'rci* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_commit_to_repository