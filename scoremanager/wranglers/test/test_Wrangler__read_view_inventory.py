# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)
configuration = score_manager._configuration


def test_Wrangler__read_view_inventory_01():
    r'''Ignores corrupt __views.py__.
    '''

    views_py_path = os.path.join(
        configuration.example_score_packages_directory_path,
        'blue_example_score',
        'segments',
        '__views__.py',
        )
    exception_path = os.path.join(
        configuration.boilerplate_directory_path,
        'exception.py',
        )

    assert filecmp.cmp(views_py_path, exception_path)

    input_ = 'blue~example~score g vls default q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments',
        '',
        'SegmentPackageWrangler __views.py__ is corrupt:',
        'No views found.',
        'Blue Example Score (2013) - segments',
        ]

    assert score_manager._transcript.titles == titles