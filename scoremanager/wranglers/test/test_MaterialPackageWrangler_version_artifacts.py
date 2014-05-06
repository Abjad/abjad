# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_version_artifacts_01():
    
    input_ = ''
    target_paths = []
    segments = ('segment_01', 'segment_02', 'segment_03')
    file_names = ('definition.py', 'output.ly', 'output.pdf')
    for segment in segments:
        versions_directory = os.path.join(
            score_manager._configuration.example_score_packages_directory_path,
            'red_example_score',
            'segments',
            segment,
            'versions',
            )
        for file_name in file_names:
            _, extension = os.path.splitext(file_name)
            target_name = '0001' + extension
            target_path = os.path.join(versions_directory, target_name)
            target_paths.append(target_path)

    for path in target_paths:
        assert not os.path.exists(path)

    try:
        input_ = 'red~example~score g ver y q'
        score_manager._run(pending_user_input=input_)
        for path in target_paths:
            assert os.path.isfile(path)
    finally:
        for path in target_paths:
            if os.path.exists(path):
                os.remove(path)

    for path in target_paths:
        assert not os.path.exists(path)