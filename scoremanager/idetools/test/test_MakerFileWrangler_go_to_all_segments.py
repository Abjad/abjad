# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_segments_01():
    r'''From score maker files to all segments.
    '''

    input_ = 'red~example~score k G q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Abjad IDE - segments',
        ]
    assert ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_segments_02():
    r'''From all maker files to all segments.
    '''

    input_ = 'K G q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Abjad IDE - segments',
        ]
    assert ide._transcript.titles == titles