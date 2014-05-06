# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_version_artifacts_01():
    
    versions_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
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

    assert not any(os.path.exists(_) for _ in paths)

    try:
        input_ = 'red~example~score m magic~numbers ver y q'
        score_manager._run(pending_user_input=input_)
        assert all(os.path.isfile(_) for _ in paths)
    finally:
        for path in paths:
            if os.path.exists(path):
                os.remove(path)

    assert not any(os.path.exists(_) for _ in paths)