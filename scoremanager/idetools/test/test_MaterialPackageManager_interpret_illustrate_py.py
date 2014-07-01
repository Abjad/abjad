# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_interpret_illustrate_py_01():
    r'''Works when illustration.ly already exists.
    '''

    package = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(package, 'illustration.ly')
    pdf_path = os.path.join(package, 'illustration.pdf')

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(ly_path)
        os.remove(pdf_path)
        assert not os.path.exists(ly_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score m magic~numbers li q'
        ide._run(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager.compare_lys(
            ly_path, 
            ly_path + '.backup',
            )
        assert systemtools.TestManager.compare_pdfs(
            pdf_path, 
            pdf_path + '.backup',
            )