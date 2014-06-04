# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_materials_01():
    r'''Goes from score build files to score materials.
    '''

    input_ = 'red~example~score u m q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_BuildFileWrangler_go_to_materials_02():
    r'''From build file library to material library.
    '''

    input_ = 'u m q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles