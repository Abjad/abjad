# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_home_01():
    r'''From score stylesheets to library.
    '''

    input_ = 'red~example~score y hh q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles


def test_StylesheetWrangler_go_home_02():
    r'''From all stylesheets to library.
    '''

    input_ = 'yy hh q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets depot',
        'Abjad IDE - home',
        ]
    assert ide._transcript.titles == titles