# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_all_segments_01():
    r'''From stylesheets director to segments depot.
    '''

    input_ = 'red~example~score y gg q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles


def test_StylesheetWrangler_go_to_all_segments_02():
    r'''From stylesheets depot to segments depot.
    '''

    input_ = 'yy gg q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets depot',
        'Abjad IDE - segments depot',
        ]
    assert ide._transcript.titles == titles