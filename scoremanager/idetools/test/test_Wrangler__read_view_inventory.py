# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
configuration = score_manager._configuration


def test_Wrangler__read_view_inventory_01():
    r'''Ignores corrupt __views.py__.
    '''

    views_py_path = os.path.join(
        configuration.example_score_packages_directory,
        'blue_example_score',
        'segments',
        '__views__.py',
        )
    exception_path = os.path.join(
        configuration.boilerplate_directory,
        'exception.py',
        )

    assert filecmp.cmp(views_py_path, exception_path)

    input_ = 'blue~example~score g va q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments',
        ]

    assert score_manager._transcript.titles == titles