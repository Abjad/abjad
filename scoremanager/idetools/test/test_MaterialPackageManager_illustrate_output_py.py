# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_illustrate_output_py_01():

    illustration_ly = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.ly',
        )
    illustration_pdf = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.pdf',
        )

    with systemtools.FilesystemState(keep=[illustration_ly, illustration_pdf]):
        os.remove(illustration_ly)
        os.remove(illustration_pdf)
        assert not os.path.exists(illustration_ly)
        assert not os.path.exists(illustration_pdf)
        input_ = 'red~example~score m tempo~inventory oi q'
        ide._run(input_=input_)
        assert os.path.isfile(illustration_ly)
        assert os.path.isfile(illustration_pdf)
        #assert diff-pdf(illustration_pdf, backup_illustration_pdf)
        #assert systemtools.TestManager.compare_lys(
        #    illustration_ly,
        #    illustration_ly + '.backup',
        #    )