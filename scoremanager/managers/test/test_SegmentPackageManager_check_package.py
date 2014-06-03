# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_SegmentPackageManager_check_package_01():

    input_ = 'blue~example~score g segment~01 ck y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '1 of 1 required directory missing:',
        '1 of 2 required files missing:',
        ]
    for line in lines:
        assert line in contents
    assert 'optional directories' not in contents
    assert 'optional files' not in contents


def test_SegmentPackageManager_check_package_02():

    input_ = 'blue~example~score g segment~01 ck n n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '1 of 1 required directory missing:',
        '1 of 2 required files found:',
        '1 of 2 required files missing:',
        '1 optional file found:',
        ]
    for line in lines:
        assert line in contents