# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_version_package_01():
    r'''Doesn't version anything because segment A should already be versioned.
    '''
    
    versions_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        'versions',
        )
    current_versioned_file_names = (
        'definition_0002.py',
        'illustration_0002.ly',
        'illustration_0002.pdf',
        )
    next_versioned_file_names = (
        'definition_0003.py',
        'illustration_0003.ly',
        'illustration_0003.pdf',
        )
    paths = []
    for next_versioned_file_name in next_versioned_file_names:
        path = os.path.join(versions_directory, next_versioned_file_name)
        paths.append(path)

    with systemtools.FilesystemState(remove=paths):
        input_ = 'red~example~score g A vr y q'
        ide._run(input_=input_)
        assert not any(os.path.isfile(_) for _ in paths)