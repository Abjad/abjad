# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_version_every_package_01():
    
    target_paths = []
    segments = ('segment_01', 'segment_02', 'segment_03')
    file_names = ('definition.py', 'output.ly', 'output.pdf')
    for segment in segments:
        versions_directory = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            segment,
            'versions',
            )
        for file_name in file_names:
            root, extension = os.path.splitext(file_name)
            target_name = '{}_{}{}'.format(root, '0002', extension)
            target_path = os.path.join(versions_directory, target_name)
            target_paths.append(target_path)

    for path in target_paths:
        assert not os.path.exists(path)

    with systemtools.FilesystemState(remove=target_paths):
        input_ = 'red~example~score g vr* y q'
        score_manager._run(pending_input=input_)
        for path in target_paths:
            assert os.path.isfile(path)