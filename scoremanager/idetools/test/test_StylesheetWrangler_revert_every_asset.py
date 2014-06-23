# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_revert_every_asset_01():

    score_manager._session._is_repository_test = True
    input_ = 'red~example~score y rrv* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_revert


def test_StylesheetWrangler_revert_every_asset_02():

    score_manager._session._is_repository_test = True
    input_ = 'Y rrv* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_revert