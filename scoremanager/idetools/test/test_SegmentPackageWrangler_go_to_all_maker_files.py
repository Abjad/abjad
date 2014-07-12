# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_maker_files_01():
    r'''From segments directory to makers depot.
    '''

    input_ = 'red~example~score g K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_maker_files_02():
    r'''From segments depot to makers depot.
    '''

    input_ = 'G K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - segments depot',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles