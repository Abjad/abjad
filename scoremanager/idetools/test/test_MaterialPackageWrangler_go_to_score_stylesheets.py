# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_score_stylesheets_01():
    r'''From materials directory to stylesheets directory.
    '''

    input_ = 'red~example~score m y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - stylesheets directory',
        ]
    assert ide._transcript.titles == titles