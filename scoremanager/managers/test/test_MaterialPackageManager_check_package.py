# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_check_package_01():

    input_ = 'red~example~score m tempo~inventory ck y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Top level (6 assets): OK' in contents
    assert 'found' not in contents
    assert 'missing' not in contents


def test_MaterialPackageManager_check_package_02():

    input_ = 'red~example~score m tempo~inventory ck n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '1 of 1 required directory found:',
        '2 of 2 required files found:',
        '3 optional files found:',
        ]
    for line in lines:
        assert line in contents
    assert 'No problem assets found.' not in contents