# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_stylesheets_01():
    r'''From score distribution files to all stylesheets.
    '''

    input_ = 'red~example~score d Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Abjad IDE - stylesheets',
        ]
    assert ide._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_stylesheets_02():
    r'''From all distribution files to all stylesheets.
    '''

    input_ = 'D Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution files',
        'Abjad IDE - stylesheets',
        ]
    assert ide._transcript.titles == titles