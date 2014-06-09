# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_MaterialPackageManager_interpret_illustration_ly_01():
    r'''Works when illustration.ly already exists.
    '''

    input_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.ly',
        )
    output_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'illustration.pdf',
        )

    with systemtools.FilesystemState(keep=[input_path, output_path]):
        os.remove(output_path)
        assert not os.path.exists(output_path)
        input_ = 'red~example~score m tempo~inventory ili q'
        score_manager._run(input_=input_)
        assert os.path.isfile(output_path)
        #assert diff-pdf(output_path, backup_output_path)