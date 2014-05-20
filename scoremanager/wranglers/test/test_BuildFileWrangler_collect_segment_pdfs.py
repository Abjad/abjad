# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_collect_segment_pdfs_01():

    # find build directory
    build_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        )
    temporary_directory = os.path.join(build_directory, 'tmp')

    # find source pdfs
    source_pdfs = []
    for number in ('01', '02', '03'):
        directory_name = 'segment_{}'.format(number)
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            directory_name,
            'output.pdf',
            )
        source_pdfs.append(path)

    # make sure source paths exist
    for path in source_pdfs:
        assert os.path.isfile(path)

    # find destination paths
    destination_pdfs = []
    for number in ('01', '02', '03'):
        file_name = 'segment-{}.pdf'
        file_name = file_name.format(number)
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'build',
            file_name,
            )
        destination_pdfs.append(path)

    # make sure destination paths exist
    for path in destination_pdfs:
        assert os.path.exists(path)

    # make sure source and destination files compare equal
    pairs = zip(source_pdfs, destination_pdfs)
    for source_path, destination_path in pairs:
        assert filecmp.cmp(source_path, destination_path)

    # back up existing pdfs
    backup_paths = []
    for path in destination_pdfs:
        backup_path = path + '.backup'
        backup_paths.append(backup_path)
        shutil.copyfile(path, backup_path)

    # remove existing pdfs
    for path in destination_pdfs:
        os.remove(path)
        
    # run input
    input_ = 'red~example~score u dc y q'
    score_manager._run(pending_input=input_)

    # make sure destination paths exist
    for path in destination_pdfs:
        assert os.path.isfile(path)

    # make sure source and destination files compare equal
    pairs = zip(source_pdfs, destination_pdfs)
    for source_path, destination_path in pairs:
        assert filecmp.cmp(source_path, destination_path)

    # remove destination pdfs
    for path in destination_pdfs:
        if os.path.exists(path):
            os.remove(path)

    # restore backup pdfs
    for backup_path, destination_path in zip(backup_paths, destination_pdfs):
        shutil.copyfile(backup_path, destination_path)
        
    # remove backup pdfs
    for path in backup_paths:
        os.remove(path)

    # make sure source paths do exist
    for path in source_pdfs:
        assert os.path.isfile(path)