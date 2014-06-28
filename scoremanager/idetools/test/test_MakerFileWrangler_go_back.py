# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_back_01():

    input_ = 'red~example~score k b q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Red Example Score (2013)',
        ]
    assert ide._transcript.titles == titles


def test_MakerFileWrangler_go_back_02():

    input_ = 'K b q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - maker files',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles