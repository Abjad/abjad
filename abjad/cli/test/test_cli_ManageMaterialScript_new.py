import abjad
import os
import platform
import pytest
import uqbar.io
from base import ScorePackageScriptTestCase
from io import StringIO
from uqbar.strings import normalize


class Test(ScorePackageScriptTestCase):

    expected_files = [
        'test_score/test_score/materials/.gitignore',
        'test_score/test_score/materials/__init__.py',
        'test_score/test_score/materials/test_material/__init__.py',
        'test_score/test_score/materials/test_material/definition.py',
    ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    def test_exists(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        pytest.helpers.create_material(
            self.test_directory_path, 'test_material')
        with abjad.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_material(
                self.test_directory_path, 'test_material', expect_error=True)
        pytest.helpers.compare_strings(
            expected=r'''
            Creating material subpackage 'test_material' ...
                Path exists: test_score/materials/test_material
            '''.replace('/', os.path.sep),
            actual=string_io.getvalue(),
        )

    def test_force_replace(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        pytest.helpers.create_material(
            self.test_directory_path, 'test_material')
        with abjad.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_material(
                self.test_directory_path, 'test_material', force=True)
        pytest.helpers.compare_strings(
            r'''
            Creating material subpackage 'test_material' ...
                Reading test_score/metadata.json ... OK!
                Created test_score/materials/test_material/
            '''.replace('/', os.path.sep),
            actual=string_io.getvalue(),
        )

    def test_internal_path(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        script = abjad.cli.ManageMaterialScript()
        command = ['--new', 'test_material']
        internal_path = self.score_path.joinpath('test_score', 'builds')
        assert internal_path.exists()
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(internal_path):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        pytest.helpers.compare_strings(
            expected=r'''
            Creating material subpackage 'test_material' ...
                Reading test_score/metadata.json ... OK!
                Created test_score/materials/test_material/
            '''.replace('/', os.path.sep),
            actual=string_io.getvalue(),
        )

    def test_success(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        script = abjad.cli.ManageMaterialScript()
        command = ['--new', 'test_material']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        pytest.helpers.compare_strings(
            actual=string_io.getvalue(),
            expected=r'''
            Creating material subpackage 'test_material' ...
                Reading test_score/metadata.json ... OK!
                Created test_score/materials/test_material/
            '''.replace('/', os.path.sep),
        )
        assert self.materials_path.joinpath('test_material').exists()
        self.compare_path_contents(self.materials_path, self.expected_files)
