# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_segments_01():
    r'''From segments directory to segments depot.
    '''

    input_ = 'red~example~score g gg q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_segments_02():
    r'''From segments depot to segments depot.
    '''

    input_ = 'gg gg q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments depot',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles