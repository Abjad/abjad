# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_score_stylesheets_01():
    r'''Goes from build directory to stylesheets directory.
    '''

    input_ = 'red~example~score u y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - stylesheets directory',
        ]
    assert ide._transcript.titles == titles