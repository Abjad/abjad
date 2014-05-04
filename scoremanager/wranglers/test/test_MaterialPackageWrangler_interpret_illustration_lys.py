# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_interpret_illustration_lys_01():
    r'''Works when illustration.ly already exists.
    '''

    package_names = ('pitch_range_inventory', 'tempo_inventory')
    input_paths = []
    for name in package_names:
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory_path,
            'red_example_score',
            'materials',
            name,
            'illustration.ly',
            )
        input_paths.append(path)
    output_paths = []
    for path in input_paths:
        path = path.replace('.ly', '.pdf')
        output_paths.append(path)
    backup_output_paths = [_ + '.backup' for _ in output_paths]
    pairs = zip(output_paths, backup_output_paths)

    assert all(os.path.isfile(_) for _ in input_paths)
    assert all(os.path.isfile(_) for _ in output_paths)
    assert not any(os.path.exists(_) for _ in backup_output_paths)

    try:
        for path in output_paths:
            shutil.copyfile(path, path + '.backup')
        assert all(os.path.isfile(_) for _ in backup_output_paths)
        for path in output_paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in output_paths)
        input_ = 'red~example~score m lyi y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert all(os.path.isfile(_) for _ in output_paths)
        assert 'Will interpret ...' in contents
        assert 'INPUT:' in contents
        assert 'OUTPUT:' in contents
        assert 'Interpreted' in contents
        #for output_path, backup_output_path in pairs:
        #    assert diff-pdf(output_path, backup_output_path)
    finally:
        assert all(os.path.exists(_) for _ in backup_output_paths)
        for path in output_paths:
            if os.path.exists(path):
                os.remove(path)
        for output_path, backup_output_path in pairs:
            shutil.copyfile(backup_output_path, output_path)
        for path in backup_output_paths:
            os.remove(path)

    assert all(os.path.isfile(_) for _ in input_paths)
    assert all(os.path.isfile(_) for _ in output_paths)
    assert not any(os.path.exists(_) for _ in backup_output_paths)