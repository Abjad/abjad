# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_edit_and_interpret_illustrate_py_01():
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
    paths = (ly_path, pdf_path)

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        for path in paths:
            os.remove(path)
            assert not os.path.exists(path)
        input_ = 'red~example~score m magic~numbers iei q'
        ide._run(input_=input_)
        for path in paths:
            assert os.path.isfile(path)
        # TODO: make this work
        #assert systemtools.TestManager.compare_pdfs(
        #    pdf_path, 
        #    pdf_path + '.backup',
        #    )
        assert systemtools.TestManager.compare_lys(
            ly_path, 
            ly_path + '.backup',
            )

    assert ide._session._attempted_to_open_file