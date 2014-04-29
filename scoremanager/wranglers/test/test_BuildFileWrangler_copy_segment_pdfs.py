# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_copy_segment_pdfs_01():

    # find build directory
    build_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        )
    temporary_directory = os.path.join(build_directory, 'tmp')

    # find source pdfs
    source_pdfs = []
    for number in ('01', '02', '03'):
        directory_name = 'segment_{}'.format(number)
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory_path,
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
            score_manager._configuration.example_score_packages_directory_path,
            'red_example_score',
            'build',
            file_name,
            )
        destination_pdfs.append(path)

    # make sure destination paths don't exist
    for path in destination_pdfs:
        assert not os.path.exists(path)

    # run input
    input_ = 'red~example~score u pdfcp y q'
    score_manager._run(pending_user_input=input_)

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

    # make sure destination paths do not exist
    for path in destination_pdfs:
        assert not os.path.exists(path)

    # make sure source paths do exist
    for path in source_pdfs:
        assert os.path.isfile(path)