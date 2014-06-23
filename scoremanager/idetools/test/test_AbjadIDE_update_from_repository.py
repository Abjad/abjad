# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_update_from_repository_01():

    score_manager._session._is_repository_test = True
    input_ = '** rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository