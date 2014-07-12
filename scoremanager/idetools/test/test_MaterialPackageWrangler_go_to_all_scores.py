# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_all_scores_01():

    input_ = 'red~example~score m S q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Abjad IDE - scores depot',
        ]
    assert ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_all_scores_02():

    input_ = 'M S q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - materials depot',
        'Abjad IDE - scores depot',
        ]
    assert ide._transcript.titles == titles