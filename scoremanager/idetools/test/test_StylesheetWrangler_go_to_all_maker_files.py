# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_all_maker_files_01():
    r'''From stylesheets directory to makers depot.
    '''

    input_ = 'red~example~score y kk q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles


def test_StylesheetWrangler_go_to_all_maker_files_02():
    r'''From stylesheets depot to makers depot.
    '''

    input_ = 'yy kk q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets depot',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles