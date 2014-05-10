# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_interpret_lilypond_files_01():

    path = score_manager._configuration.example_score_packages_directory_path
    path = os.path.join(path, 'red_example_score', 'segments')
    paths = [
        os.path.join(path, 'segment_01', 'output.ly'),
        os.path.join(path, 'segment_01', 'output.pdf'),
        os.path.join(path, 'segment_02', 'output.ly'),
        os.path.join(path, 'segment_02', 'output.pdf'),
        os.path.join(path, 'segment_03', 'output.ly'),
        os.path.join(path, 'segment_03', 'output.pdf'),
        ]


    pdf_paths = [_ for _ in paths if _.endswith('.pdf')]

    with systemtools.FilesystemState(keep=pdf_paths):
        input_ = 'red~example~score g lyi y q'
        score_manager._run(pending_input=input_)
        contents = score_manager._transcript.contents
        strings = []
        strings.extend(paths)
        strings.extend([
            'Will interpret ...',
            'INPUT:',
            'OUTPUT:',
            'Interpreted',
            'Wrote',
            ])
        for string in strings:
            assert string in contents