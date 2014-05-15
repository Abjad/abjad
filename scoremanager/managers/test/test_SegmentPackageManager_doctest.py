# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_doctest_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score g A pyd q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        '2 testable assets found ...',
        '0 of 0 tests passed in 2 modules.',
        ]