# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_check_package_01():

    input_ = 'red~example~score g A ck y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '1 of 2 required files missing:',
        ]
    for line in lines:
        assert line in contents
    assert 'No problem assets found.' not in contents
    assert 'required directory found' not in contents
    assert 'required files found' not in contents
    assert 'optional files found' not in contents


def test_SegmentPackageManager_check_package_02():

    input_ = 'red~example~score g A ck n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '1 of 1 required directory found:',
        '1 of 2 required files found:',
        '1 of 2 required files missing:',
        '4 optional files found:',
        ]
    for line in lines:
        assert line in contents