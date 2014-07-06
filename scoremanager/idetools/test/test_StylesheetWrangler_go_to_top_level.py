# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_top_level_01():
    r'''From score stylesheets to library.
    '''

    input_ = 'red~example~score y H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Abjad IDE',
        ]
    assert ide._transcript.titles == titles


def test_StylesheetWrangler_go_to_top_level_02():
    r'''From all stylesheets to library.
    '''

    input_ = 'Y H q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Abjad IDE',
        ]
    assert ide._transcript.titles == titles