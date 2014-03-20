# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_doctest_01():

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'red~example~score g segment~01 pyd default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.titles[-4] == 'Running doctest ...'