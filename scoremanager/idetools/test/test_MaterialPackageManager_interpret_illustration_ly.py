# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_interpret_illustration_ly_01():
    r'''Works when illustration.ly already exists.
    '''

    ly_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.ly',
        )
    pdf_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.pdf',
        )

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score m tempo~inventory ii y q'
        ide._run(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(pdf_path)