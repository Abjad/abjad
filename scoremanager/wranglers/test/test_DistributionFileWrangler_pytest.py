# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_pytest_01():
    r'''Works on all distribution files in library.
    '''

    input_ = 'd pyt q'
    score_manager._run(input_=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_DistributionFileWrangler_pytest_02():
    r'''Works on all files in a single distribution directory.
    '''

    input_ = 'red~example~score d pyt q'
    score_manager._run(input_=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents