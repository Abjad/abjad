# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_go_to_previous_package_01():
    r'''Previous material package.
    '''

    score_manager = scoremanager.iotools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m < < < < < < q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - time signatures',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Red Example Score (2013) - materials - pitch range inventory (AE)',
        'Red Example Score (2013) - materials - magic numbers',
        'Red Example Score (2013) - materials - instrumentation (AE)',
        'Red Example Score (2013) - materials - time signatures',
        ]
    assert score_manager._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_previous_package_02():
    r'''State is preserved cleanly navigating between different types of
    sibling asset.
    '''

    score_manager = scoremanager.iotools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m < < g < < q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - time signatures',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments - C',
        'Red Example Score (2013) - segments - B',
        ]
    assert score_manager._transcript.titles == titles