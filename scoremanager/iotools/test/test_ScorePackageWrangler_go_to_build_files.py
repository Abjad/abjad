# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_build_files_01():
    r'''From materials directory to build directory.
    '''

    input_ = 'u q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        ]
    assert score_manager._transcript.titles == titles