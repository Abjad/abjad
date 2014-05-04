# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_doctest_01():
    r'''Works in library.
    '''

    input_ = 'm pyd q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        'testable assets found ...',
        'tests passed in',
        ]
    for string in strings:
        assert string in contents

    
def test_MaterialPackageWrangler_doctest_02():
    r'''Works in score.
    '''

    input_ = 'red~example~score m pyd q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        '21 testable assets found ...',
        '0 of 0 tests passed in 21 modules.',
        ]
    for string in strings:
        assert string in contents