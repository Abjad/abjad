# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_interpret_every_make_py_01():

    path = score_manager._configuration.example_score_packages_directory
    path = os.path.join(path, 'red_example_score', 'segments')
    paths = [
        os.path.join(path, 'segment_01', '__make__.py'),
        os.path.join(path, 'segment_01', 'output.ly'),
        os.path.join(path, 'segment_01', 'output.pdf'),
        os.path.join(path, 'segment_02', '__make__.py'),
        os.path.join(path, 'segment_02', 'output.ly'),
        os.path.join(path, 'segment_02', 'output.pdf'),
        os.path.join(path, 'segment_03', '__make__.py'),
        os.path.join(path, 'segment_03', 'output.ly'),
        os.path.join(path, 'segment_03', 'output.pdf'),
        ]


    ly_paths = [_ for _ in paths if _.endswith('.ly')]
    pdf_paths = [_ for _ in paths if _.endswith('.pdf')]
    original_paths = ly_paths + pdf_paths

    with systemtools.FilesystemState(keep=original_paths):
        input_ = 'red~example~score g ki* y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        strings = []
        strings.extend(paths)
        strings.extend([
            'Will interpret ...',
            'INPUT:',
            'OUTPUT:',
            ])
        for string in strings:
            assert string in contents