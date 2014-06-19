# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_doctest_01():

    input_ = 'red~example~score m tempo~inventory pyd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        '7 testable assets found ...',
        '0 of 0 tests passed in 7 modules.',
        ]
    for string in strings:
       assert string in contents