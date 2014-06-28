# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_version_package_01():
    
    versions_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'magic_numbers',
        'versions',
        )
    file_names = (
        'definition_0002.py', 
        'illustration_0002.ly',
        'illustration_0002.pdf',
        'output_0002.py',
        )
    paths = []
    for file_name in file_names:
        path = os.path.join(versions_directory, file_name)
        paths.append(path)

    with systemtools.FilesystemState(remove=paths):
        input_ = 'red~example~score m magic~numbers vr y q'
        ide._run(input_=input_)
        assert all(os.path.isfile(_) for _ in paths)