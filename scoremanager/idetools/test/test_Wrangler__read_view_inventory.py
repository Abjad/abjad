# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
configuration = ide._configuration


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
        os.remove(views_file)
        os.remove(metadata_file)
        shutil.copyfile(exception_file, views_file)
        assert filecmp.cmp(views_file, exception_file)
        input_ = 'blue~example~score g wa q'
        ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments directory',
        'Blue Example Score (2013) - segments directory - views (EDIT)',
        ]

    assert ide._transcript.titles == titles