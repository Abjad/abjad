# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_all_build_files_01():
    r'''From materials directory to build depot.
    '''

    input_ = 'red~example~score m U q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Abjad IDE - build depot',
        ]
    assert ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_all_build_files_02():
    r'''From materials depot to build depot.
    '''

    input_ = 'M U q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - materials depot',
        'Abjad IDE - build depot',
        ]
    assert ide._transcript.titles == titles