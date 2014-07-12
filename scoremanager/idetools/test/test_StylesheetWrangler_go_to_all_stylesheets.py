# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_all_stylesheets_01():
    r'''From stylesheets directory to stylesheets depot.
    '''

    input_ = 'red~example~score y Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Abjad IDE - stylesheets depot',
        ]
    assert ide._transcript.titles == titles


def test_StylesheetWrangler_go_to_all_stylesheets_02():
    r'''From stylesheets depot to styleshseets depot.
    '''

    input_ = 'Y Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - stylesheets depot',
        'Abjad IDE - stylesheets depot',
        ]
    assert ide._transcript.titles == titles