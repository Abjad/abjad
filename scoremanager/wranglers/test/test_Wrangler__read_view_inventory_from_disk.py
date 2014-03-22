# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)
configuration = score_manager._configuration


def test_Wrangler__read_view_inventory_from_disk_01():
    r'''Ignores corrupt views module.
    '''

    views_module_path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'blue_example_score',
        'segments',
        '__views__.py',
        )
    exception_path = os.path.join(
        configuration.boilerplate_directory_path,
        'exception.py',
        )

    assert filecmp.cmp(views_module_path, exception_path)

    input_ = 'blue~example~score g vl default q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments',
        'Views module is corrupt.',
        'No views found.',
        'Blue Example Score (2013) - segments',
        ]

    assert score_manager._transcript.titles == titles