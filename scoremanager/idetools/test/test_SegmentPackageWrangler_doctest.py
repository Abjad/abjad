# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_doctest_01():
    r'''In library.
    '''

    input_ = 'gg dt q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    strings = [
        'Running doctest ...',
        'testable assets found ...',
        'tests passed in',
        ]
    for string in strings:
        assert string in contents

    
def test_SegmentPackageWrangler_doctest_02():
    r'''In score package.
    '''

    input_ = 'red~example~score g dt q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    strings = [
        'Running doctest ...',
        '15 testable assets found ...',
        '0 of 0 tests passed in 15 modules.',
        ]
    for string in strings:
        assert string in contents