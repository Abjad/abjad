# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_pytest_01():
    r'''Works on a single material package.
    '''

    input_ = 'red~example~score m tempo~inventory pyt q'
    score_manager._run(pending_user_input=input_)
    transcript_contents = score_manager._transcript.contents

    strings = [
        'Running py.test ...',
        '3 testable assets found ...',
        'Collected 0 items',
        ]

    for string in strings:
        assert string in transcript_contents