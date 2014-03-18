# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager___init___01():
    r'''Shared session.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    wrangler = score_manager._score_package_wrangler

    assert score_manager._session is wrangler._session
