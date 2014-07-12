# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_all_maker_files_01():
    r'''From materials directory to makers depot.
    '''

    input_ = 'red~example~score m K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_all_maker_files_02():
    r'''From materials depot to makers depot.
    '''

    input_ = 'M K q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - materials depot',
        'Abjad IDE - makers depot',
        ]
    assert ide._transcript.titles == titles