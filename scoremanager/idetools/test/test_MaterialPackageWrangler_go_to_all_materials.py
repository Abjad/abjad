# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_all_materials_01():
    r'''From materials directory to materials depot.
    '''

    input_ = 'red~example~score m mm q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Abjad IDE - materials depot',
        ]
    assert ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_all_materials_02():
    r'''From materials depot to materials depot.
    '''

    input_ = 'mm mm q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        'Abjad IDE - materials depot',
        ]
    assert ide._transcript.titles == titles