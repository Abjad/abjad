# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_pytest_01():
    r'''Works on all build files in library.
    '''

    input_ = 'u pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_BuildFileWrangler_pytest_02():
    r'''Works on all files in a single build directory.
    '''

    input_ = 'red~example~score u pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents