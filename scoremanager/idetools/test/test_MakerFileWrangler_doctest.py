# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_doctest_01():
    r'''In library.
    '''

    input_ = 'k pyd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        'testable assets found ...',
        'tests passed in',
        ]
    for string in strings:
        assert string in contents

    
def test_MakerFileWrangler_doctest_02():
    r'''In score package.
    '''

    input_ = 'red~example~score k pyd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        'Running doctest ...',
        '3 testable assets found ...',
        'RedExampleScoreRhythmMaker.py OK',
        'RedExampleScoreTemplate.py OK',
        '0 of 0 tests passed in 3 modules.',
        ]
    for string in strings:
        assert string in contents