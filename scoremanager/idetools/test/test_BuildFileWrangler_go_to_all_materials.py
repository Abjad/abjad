# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_all_materials_01():
    r'''From score build files to all materials.
    '''

    input_ = 'red~example~score u M q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_BuildFileWrangler_go_to_all_materials_02():
    r'''From all build files to all materials.
    '''

    input_ = 'U M q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles