# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_interpret_make_py_01():

    segment_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_01',
        )
    make_path = os.path.join(segment_directory, '__make__.py')
    ly_path = os.path.join(segment_directory, 'output.ly')
    pdf_path = os.path.join(segment_directory, 'output.pdf')
    output_paths = (ly_path, pdf_path)

    keep = (make_path,) + output_paths
    with systemtools.FilesystemState(keep=keep):
        for path in output_paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in output_paths)
        input_ = 'red~example~score g A kyi y q'
        score_manager._run(pending_input=input_)
        assert all(os.path.isfile(_) for _ in output_paths)
        #assert systemtools.TestManager.compare_lys(
        #    ly_path,
        #    ly_path + '.backup',
        #    )
        #assert diff-pdf(pdf_path, pdf_path + '.backup')