# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_check_every_package_01():
    r'''Works in score.
    '''

    lines = [
        'Segments (3 packages)',
        'A: OK',
        'B: OK',
        'C: OK',
        ]

    input_ = 'red~example~score g ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents


def test_SegmentPackageWrangler_check_every_package_02():
    r'''Works in library.
    '''

    lines = [
        'A (Red Example Score): OK',
        'B (Red Example Score): OK',
        'C (Red Example Score): OK',
        ]

    input_ = 'g ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents