# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_version_package_01():
    
    versions_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        'versions',
        )
    file_names = (
        'definition_0002.py',
        'output_0002.ly',
        'output_0002.pdf',
        )
    paths = []
    for file_name in file_names:
        path = os.path.join(versions_directory, file_name)
        paths.append(path)

    with systemtools.FilesystemState(remove=paths):
        input_ = 'red~example~score g A vr y q'
        ide._run(input_=input_)
        assert all(os.path.isfile(_) for _ in paths)