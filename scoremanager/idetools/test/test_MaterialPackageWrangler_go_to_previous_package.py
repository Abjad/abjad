# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_go_to_previous_package_01():
    r'''Previous material package.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m < < < < < < q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - time signatures',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - materials directory - pitch range inventory',
        'Red Example Score (2013) - materials directory - performer inventory',
        'Red Example Score (2013) - materials directory - magic numbers',
        'Red Example Score (2013) - materials directory - time signatures',
        ]
    assert ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_previous_package_02():
    r'''State is preserved cleanly navigating between different types of
    sibling asset.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m < < g < < q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - time signatures',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - C',
        'Red Example Score (2013) - segments directory - B',
        ]
    assert ide._transcript.titles == titles