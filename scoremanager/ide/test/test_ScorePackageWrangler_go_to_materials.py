# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_materials_01():
    r'''From materials directory to build directory.
    '''

    input_ = 'm q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles