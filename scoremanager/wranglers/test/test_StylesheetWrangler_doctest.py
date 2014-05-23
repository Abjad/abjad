# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_doctest_01():
    r'''In library.
    '''

    input_ = 'y pyd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        'No testable assets found.',
        ]
    for string in strings:
        assert string in contents

    
def test_StylesheetWrangler_doctest_02():
    r'''In score package.
    '''

    input_ = 'red~example~score y pyd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        'No testable assets found.',
        ]
    for string in strings:
        assert string in contents