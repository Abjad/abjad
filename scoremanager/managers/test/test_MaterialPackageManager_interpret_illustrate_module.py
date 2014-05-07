# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_interpret_illustrate_module_01():
    r'''Works when illustration.ly already exists.
    '''

    package = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'magic_numbers',
        )

    ly_path = os.path.join(package, 'illustration.ly')
    pdf_path = os.path.join(package, 'illustration.pdf')
    paths = (ly_path, pdf_path)
    backup_paths = [_ + '.backup' for _ in paths]

    assert all(os.path.isfile(_) for _ in paths)
    assert not any(os.path.exists(_) for _ in backup_paths)

    try:
        for path in paths:
            shutil.copyfile(path, path + '.backup')
            assert filecmp.cmp(path, path + '.backup')
            os.remove(path)
            assert not os.path.exists(path)
        input_ = 'red~example~score m magic~numbers imi q'
        score_manager._run(pending_input=input_)
        for path in paths:
            assert os.path.isfile(path)
        #assert diff-pdf(pdf_path, pdf_path + '.backup')
        #assert systemtools.TestManager.compare_lys(
        #    ly_path, 
        #    ly_path + '.backup',
        #    )
    finally:
        assert all(os.path.isfile(_) for _ in backup_paths)
        for path in paths:
            os.remove(path)
            shutil.copyfile(path + '.backup', path)
            os.remove(path + '.backup')

    assert all(os.path.isfile(_) for _ in paths)
    assert not any(os.path.exists(_) for _ in backup_paths)