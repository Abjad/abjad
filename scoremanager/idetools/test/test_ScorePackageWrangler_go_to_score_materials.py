# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_go_to_score_materials_01():
    r'''From scores to materials depot.
    '''

    input_ = 'M q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - materials depot',
        ]
    assert ide._transcript.titles == titles