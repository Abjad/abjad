# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_doctest_01():

    input_ = 'red~example~score m tempo~inventory pyd default q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        '3 testable assets found ...',
        '0 of 0 tests passed in 3 modules.',
        ]
    for string in strings:
       assert string in contents