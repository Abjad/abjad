# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager


def test_BuildDirectoryManager_copy_segment_lilypond_files_01():

    # set up score manager and diretories
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    build_directory = os.path.join(
        score_manager._configuration.abjad_score_packages_directory_path,
        'red_example_score',
        'build',
        )
    temporary_directory = os.path.join(build_directory, 'tmp')

    # set up file paths
    file_names, file_paths, temporary_file_paths = [], [], []
    for number in ('01', '02', '03'):
        file_name = 'red-example-score-segment-{}.ly'
        file_name = file_name.format(number)
        file_names.append(file_name)
        file_path = os.path.join(build_directory, file_name)
        file_paths.append(file_path)
        temporary_file_path = os.path.join(temporary_directory, file_name)
        temporary_file_paths.append(temporary_file_path)

    # make sure segment files are currently in build directory
    for file_path in file_paths:
        assert os.path.isfile(file_path)

    if not os.path.isdir(temporary_directory):
        os.mkdir(temporary_directory)

    # move segment files from build directory to temporary directory
    pairs = zip(file_paths, temporary_file_paths)
    for file_path, temporary_file_path in pairs:
        print file_path, temporary_file_path
        shutil.move(file_path, temporary_file_path)

    # make sure segment files are no longer in build directory
    for file_path in file_paths:
        assert not os.path.isfile(file_path)

    # call (lycp)
    string = 'red~example~score u lycp default q'
    score_manager._run(pending_user_input=string, is_test=True)

    # make sure new segment files are currently in build directory
    for file_path in file_paths:
        assert os.path.isfile(file_path)

    # make sure new and old segment files compare equal
    for file_path, temporary_file_path in pairs:
        assert filecmp.cmp(file_path, temporary_file_path), repr(file_path)

    # remove temporary directory
    shutil.rmtree(temporary_directory)
