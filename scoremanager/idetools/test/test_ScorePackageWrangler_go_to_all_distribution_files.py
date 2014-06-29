# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_all_distribution_files_01():
    r'''From all scores to all distribution files.
    '''

    input_ = 'D q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution files',
        ]
    assert ide._transcript.titles == titles