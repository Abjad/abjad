# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_home_01():
    r'''From segments directory.
    '''

    input_ = 'red~example~score g hh q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_home_02():
    r'''From segments depot.
    '''

    input_ = 'gg hh q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments depot',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles