# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_interpret_illustration_ly_01():
    r'''Works when illustration.ly already exists.
    '''

    input_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.ly',
        )
    output_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.pdf',
        )
    backup_output_path = output_path + '.backup'
    assert os.path.isfile(input_path)
    assert os.path.isfile(output_path)
    assert not os.path.exists(backup_output_path)

    try:
        shutil.copyfile(output_path, backup_output_path)
        assert filecmp.cmp(output_path, backup_output_path)
        os.remove(output_path)
        assert not os.path.exists(output_path)
        input_ = 'red~example~score m tempo~inventory lyi q'
        score_manager._run(pending_user_input=input_)
        assert os.path.isfile(output_path)
        #assert diff-pdf(output_path, backup_output_path)
    finally:
        assert os.path.exists(backup_output_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        shutil.copyfile(backup_output_path, output_path)
        os.remove(backup_output_path)

    assert os.path.isfile(input_path)
    assert os.path.isfile(output_path)
    assert not os.path.exists(backup_output_path)