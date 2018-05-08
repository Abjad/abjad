import abjad
import os
import platform
import pytest
import uqbar.io
from base import ScorePackageScriptTestCase
from io import StringIO
from unittest import mock
from uqbar.strings import normalize


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

    @mock.patch('abjad.IOManager.open_file')
    def test_success_one_material(self, open_file_mock):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        material_path = pytest.helpers.create_material(
            self.test_directory_path, 'test_material')
        self.illustrate_material('test_material')
        pdf_path = material_path.joinpath('illustration.pdf')
        assert pdf_path.exists()
        pdf_path.unlink()
        script = abjad.cli.ManageMaterialScript()
        command = ['--render', 'test_material']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(string_io.getvalue(), r'''
        Rendering candidates: 'test_material' ...
        Rendering test_score/materials/test_material/
            Writing test_score/materials/test_material/illustration.pdf ... OK!
                LilyPond runtime: ... second...
            Rendered test_score/materials/test_material/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(self.materials_path, self.expected_files)
