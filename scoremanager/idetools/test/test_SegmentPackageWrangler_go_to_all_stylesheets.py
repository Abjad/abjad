# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_stylesheets_01():
    r'''From segments directory to stylesheets depot.
    '''

    input_ = 'red~example~score g Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Abjad IDE - stylesheets depot',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_stylesheets_02():
    r'''From segments depot to stylesheets depot.
    '''

    input_ = 'G Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments depot',
        'Abjad IDE - stylesheets depot',
        ]
    assert ide._transcript.titles == titles