# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_doctest_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g A dt q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    strings = [
        'Running doctest ...',
        '2 testable assets found ...',
        '0 of 0 tests passed in 2 modules.',
        ]