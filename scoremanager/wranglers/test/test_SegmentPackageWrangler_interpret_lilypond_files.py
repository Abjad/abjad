# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_interpret_lilypond_files_01():

    path = score_manager._configuration.example_score_packages_directory_path
    path = os.path.join(path, 'red_example_score', 'segments')
    paths = [
        os.path.join(path, 'segment_01', 'output.ly'),
        os.path.join(path, 'segment_01', 'output.pdf'),
        os.path.join(path, 'segment_02', 'output.ly'),
        os.path.join(path, 'segment_02', 'output.pdf'),
        os.path.join(path, 'segment_03', 'output.ly'),
        os.path.join(path, 'segment_03', 'output.pdf'),
        ]

    strings = []
    strings.extend(paths)
    strings.extend([
        'Will interpret ...',
        'INPUT:',
        'OUTPUT:',
        'Interpreted',
        'Wrote',
        ])

    pdf_paths = [_ for _ in paths if _.endswith('.pdf')]
    backup_paths = [_ + '.backup' for _ in pdf_paths]

    for pdf_path in pdf_paths:
        assert os.path.isfile(pdf_path)
    for backup_path in backup_paths:
        assert not os.path.exists(backup_path)

    try:
        for pdf_path, backup_path in zip(pdf_paths, backup_paths):
            shutil.copyfile(pdf_path, backup_path)
        for backup_path in backup_paths:
            assert os.path.isfile(backup_path)
        input_ = 'red~example~score g lyi y q'
        score_manager._run(pending_input=input_)
        contents = score_manager._transcript.contents
        for string in strings:
            assert string in contents
    finally:
        for backup_path, pdf_path in zip(backup_paths, pdf_paths):
            shutil.copy(backup_path, pdf_path)
        for backup_path in backup_paths:
            os.remove(backup_path)

    for pdf_path in pdf_paths:
        assert os.path.isfile(pdf_path)
    for backup_path in backup_paths:
        assert not os.path.exists(backup_path)