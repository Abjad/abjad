# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_doctest_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score pyd q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        '30 testable assets found ...',
        '0 of 0 tests passed in 30 modules.',
        ]

    for string in strings:
        assert string in contents