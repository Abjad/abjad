# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_all_materials_01():
    r'''From score build files to all materials.
    '''

    input_ = 'red~example~score u mm q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Abjad IDE - materials depot',
        ]
    assert ide._transcript.titles == titles


def test_BuildFileWrangler_go_to_all_materials_02():
    r'''From all build files to all materials.
    '''

    input_ = 'uu mm q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        'Abjad IDE - materials depot',
        ]
    assert ide._transcript.titles == titles