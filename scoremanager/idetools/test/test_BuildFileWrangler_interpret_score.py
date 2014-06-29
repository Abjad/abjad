# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_interpret_score_01():
    r'''Works when score already exists.
    '''

    tex_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'score.tex',
        )
    pdf_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'score.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score u si q'
        ide._run(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager.compare_pdfs(
            pdf_path, 
            pdf_path + '.backup',
            )