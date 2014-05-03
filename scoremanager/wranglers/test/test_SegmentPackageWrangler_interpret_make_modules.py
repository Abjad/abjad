# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_interpret_make_modules_01():

    path = score_manager._configuration.example_score_packages_directory_path
    path = os.path.join(path, 'red_example_score', 'segments')
    paths = [
        os.path.join(path, 'segment_01', '__make__.py'),
        os.path.join(path, 'segment_01', 'output.ly'),
        os.path.join(path, 'segment_01', 'output.pdf'),
        os.path.join(path, 'segment_02', '__make__.py'),
        os.path.join(path, 'segment_02', 'output.ly'),
        os.path.join(path, 'segment_02', 'output.pdf'),
        os.path.join(path, 'segment_03', '__make__.py'),
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

    ly_paths = [_ for _ in paths if _.endswith('.ly')]
    pdf_paths = [_ for _ in paths if _.endswith('.pdf')]
    original_paths = ly_paths + pdf_paths

    backup_paths = [_ + '.backup' for _ in original_paths]

    for path in original_paths:
        assert os.path.isfile(path)
    for backup_path in backup_paths:
        assert not os.path.exists(backup_path)

    try:
        for original_path, backup_path in zip(original_paths, backup_paths):
            shutil.copyfile(original_path, backup_path)
        for backup_path in backup_paths:
            assert os.path.isfile(backup_path)
        input_ = 'red~example~score g mmi y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        for string in strings:
            assert string in contents
    finally:
        for backup_path, original_path in zip(backup_paths, original_paths):
            shutil.copy(backup_path, original_path)
        for backup_path in backup_paths:
            os.remove(backup_path)

    for original_path in original_paths:
        assert os.path.isfile(original_path)
    for backup_path in backup_paths:
        assert not os.path.exists(backup_path)