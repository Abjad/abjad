# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_pytest_01():

    input_ = 'red~example~score g A pyt q'
    score_manager._run(input_=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents