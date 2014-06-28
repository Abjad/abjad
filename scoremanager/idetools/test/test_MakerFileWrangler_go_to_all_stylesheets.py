# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_stylesheets_01():
    r'''From score maker files to all stylesheets.
    '''

    input_ = 'red~example~score k Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Abjad IDE - stylesheets',
        ]
    assert ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_stylesheets_02():
    r'''From all maker files to all stylesheets.
    '''

    input_ = 'K Y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Abjad IDE - stylesheets',
        ]
    assert ide._transcript.titles == titles