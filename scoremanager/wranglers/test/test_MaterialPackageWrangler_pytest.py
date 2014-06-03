# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_pytest_01():
    r'''Works on a single material package.
    '''

    input_ = 'red~example~score m tempo~inventory pyt q'
    score_manager._run(input_=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_MaterialPackageWrangler_pytest_02():
    r'''Works on all material packages in a score.
    '''

    input_ = 'red~example~score m pyt q'
    score_manager._run(input_=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents


def test_MaterialPackageWrangler_pytest_03():
    r'''Works on all material packages in library.
    '''

    input_ = 'm pyt q'
    score_manager._run(input_=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        'No testable assets found.',
        ]

    for string in strings:
        assert string in transcript_contents