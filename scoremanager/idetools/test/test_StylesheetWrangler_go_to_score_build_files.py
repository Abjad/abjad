# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_score_build_files_01():
    r'''From stylesheets directory to build directory.
    '''

    input_ = 'red~example~score y u q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Red Example Score (2013) - build directory',
        ]
    assert ide._transcript.titles == titles