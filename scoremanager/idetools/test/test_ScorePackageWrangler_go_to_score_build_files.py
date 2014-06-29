# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_score_build_files_01():
    r'''From materials directory to build directory.
    '''

    input_ = 'U q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build files',
        ]
    assert ide._transcript.titles == titles