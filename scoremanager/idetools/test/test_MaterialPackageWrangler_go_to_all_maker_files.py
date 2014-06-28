# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_all_maker_files_01():
    r'''From score materials to all maker files.
    '''

    input_ = 'red~example~score m K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Abjad IDE - maker files',
        ]
    assert ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_all_maker_files_02():
    r'''From all materials to all maker files.
    '''

    input_ = 'M K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials',
        'Abjad IDE - maker files',
        ]
    assert ide._transcript.titles == titles