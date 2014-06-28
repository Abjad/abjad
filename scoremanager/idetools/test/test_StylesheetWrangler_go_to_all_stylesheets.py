# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_all_stylesheets_01():
    r'''From score stylesheets files to all stylesheets.
    '''

    input_ = 'red~example~score y Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Abjad IDE - stylesheets',
        ]
    assert ide._transcript.titles == titles


def test_StylesheetWrangler_go_to_all_stylesheets_02():
    r'''From all stylesheets to all stylesheets.
    '''

    input_ = 'Y Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Abjad IDE - stylesheets',
        ]
    assert ide._transcript.titles == titles