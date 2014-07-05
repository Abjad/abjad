# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_collect_segment_pdfs_01():

    build_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        )
    source_pdfs = []
    for number in ('01', '02', '03'):
        directory_name = 'segment_{}'.format(number)
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            directory_name,
            'illustration.pdf',
            )
        source_pdfs.append(path)
    destination_pdfs = []
    for number in ('01', '02', '03'):
        file_name = 'segment-{}.pdf'
        file_name = file_name.format(number)
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'build',
            file_name,
            )
        destination_pdfs.append(path)
    all_pdfs = source_pdfs + destination_pdfs
    pairs = zip(source_pdfs, destination_pdfs)
    for source_path, destination_path in pairs:
        assert filecmp.cmp(source_path, destination_path)

    with systemtools.FilesystemState(keep=all_pdfs):
        for path in destination_pdfs:
            os.remove(path)
        input_ = 'red~example~score u dc y q'
        ide._run(input_=input_)
        for path in destination_pdfs:
            assert os.path.isfile(path)
        for source_path, destination_path in pairs:
            assert filecmp.cmp(source_path, destination_path)