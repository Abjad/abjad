# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager___init___01():
    r'''Shared session.
    '''

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager.score_package_wrangler

    assert score_manager.session is wrangler.session
