# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageManager_check_package_01():

    input_ = 'red~example~score ck y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        'Build (18 files): OK',
        'Distribution (2 files): OK',
        'Makers (2 files): OK',
        'Materials (5 packages):',
        'Segments (3 packages):',
        'Stylesheets (2 files): OK',
        ]
    for line in lines:
        assert line in contents
    assert 'found' not in contents


def test_ScorePackageManager_check_package_02():

    input_ = 'red~example~score ck n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '6 of 6 required directories found:',
        '2 of 2 required files found:',
        '1 optional directory found:',
        ]
    for line in lines:
        assert line in contents


def test_ScorePackageManager_check_package_03():

    input_ = 'blue~example~score ck y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '1 unrecognized file found:',
        ]
    for line in lines:
        assert line in contents