# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
configuration = score_manager._configuration


def test_Wrangler__read_view_inventory_01():
    r'''Ignores corrupt __views.py__.
    '''

    views_file = os.path.join(
        configuration.example_score_packages_directory,
        'blue_example_score',
        'segments',
        '__views__.py',
        )
    metadata_file = os.path.join(
        configuration.example_score_packages_directory,
        'blue_example_score',
        'segments',
        '__metadata__.py',
        )
    exception_file = os.path.join(
        configuration.boilerplate_directory,
        'exception.py',
        )

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        shutil.copyfile(exception_file, views_file)
        assert filecmp.cmp(views_file, exception_file)
        input_ = 'blue~example~score g va q'
        score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments',
        'Blue Example Score (2013) - segments - views (EDIT)',
        ]

    assert score_manager._transcript.titles == titles