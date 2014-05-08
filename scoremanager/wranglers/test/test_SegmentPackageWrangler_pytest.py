# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_pytest_01():
    r'''Works on all visible segment packages in library.
    '''

    input_ = 'g pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_SegmentPackageWrangler_pytest_02():
    r'''Works on all segment packages in a score.
    '''

    input_ = 'red~example~score g pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_SegmentPackageWrangler_pytest_03():
    r'''Works on a single segment package.
    '''

    input_ = 'red~example~score g segment~01 pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        '3 testable assets found ...',
        ]

    for string in strings:
        assert string in transcript_contents