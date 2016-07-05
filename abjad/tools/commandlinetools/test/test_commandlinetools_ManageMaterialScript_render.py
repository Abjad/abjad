# -*- coding: utf-8 -*-
import os
import platform
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase
try:
    from unittest import mock
except ImportError:
    import mock


class Test(ScorePackageScriptTestCase):

    expected_files = [
        'test_score/test_score/materials/.gitignore',
        'test_score/test_score/materials/__init__.py',
        'test_score/test_score/materials/test_material/__init__.py',
        'test_score/test_score/materials/test_material/definition.py',
        'test_score/test_score/materials/test_material/illustration.ly',
        'test_score/test_score/materials/test_material/illustration.pdf',
        ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_one_material(self, open_file_mock):
        self.create_score()
        material_path = self.create_material('test_material')
        self.illustrate_material('test_material')
        pdf_path = material_path.joinpath('illustration.pdf')
        assert pdf_path.exists()
        pdf_path.unlink()
        script = commandlinetools.ManageMaterialScript()
        command = ['--render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Rendering candidates: 'test_material' ...
        Rendering test_score/materials/test_material/
            Writing test_score/materials/test_material/illustration.pdf ... OK!
                LilyPond runtime: ... second...
            Rendered test_score/materials/test_material/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(self.materials_path, self.expected_files)
