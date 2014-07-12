# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_score_materials_01():
    r'''From makers directory to materials directory.
    '''

    input_ = 'red~example~score k m q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Red Example Score (2013) - materials directory',
        ]
    assert ide._transcript.titles == titles