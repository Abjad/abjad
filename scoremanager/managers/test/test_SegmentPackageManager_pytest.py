# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_pytest_01():

    input_ = 'red~example~score g segment~01 pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents