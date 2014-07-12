# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_segments_01():
    r'''From segments directory to segments depot.
    '''

    input_ = 'red~example~score g G q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_segments_02():
    r'''From segments depot to segments depot.
    '''

    input_ = 'G G q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - segments depot',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles