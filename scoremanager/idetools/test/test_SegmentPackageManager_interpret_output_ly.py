# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_interpret_output_ly_01():
    r'''Works when output.ly already exists.
    '''

    input_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        'output.ly',
        )
    output_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        'output.pdf',
        )

    with systemtools.FilesystemState(keep=[input_path, output_path]):
        os.remove(output_path)
        assert not os.path.exists(output_path)
        input_ = 'red~example~score g A oli y q'
        ide._run(input_=input_)
        assert os.path.isfile(output_path)
        # TODO: make this work
        #assert systemtools.TestManager.compare_pdfs(
        #    output_path, 
        #    output_path + '.backup',
        #    )