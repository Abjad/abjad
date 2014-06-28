# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_remove_packages_01():

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'instrumentation',
        )
    backup_path = path + '.backup'

    assert os.path.exists(path)
    assert not os.path.exists(backup_path)
    shutil.copytree(path, backup_path)
    assert os.path.exists(backup_path)

    input_ = 'red~example~score m rm instrumentation remove q'
    ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(backup_path)
    shutil.move(backup_path, path)
    manager = scoremanager.idetools.PackageManager(
        path=path,
        session=ide._session,
        )
    manager.add()

    assert os.path.exists(path)
    assert not os.path.exists(backup_path)