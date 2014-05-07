# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_pytest_01():
    r'''Works on all visible score packages.
    '''

    input_ = 'pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        '70 testable assets found ...',
        ]

    for string in strings:
        assert string in transcript_contents


def test_ScorePackageWrangler_pytest_02():
    r'''Works on a single score package.
    '''

    input_ = 'red~example~score pyt q'
    score_manager._run(pending_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        '1 testable asset found ...',
        ]

    for string in strings:
        assert string in transcript_contents