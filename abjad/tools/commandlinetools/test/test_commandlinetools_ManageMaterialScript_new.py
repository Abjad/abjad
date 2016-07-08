# -*- coding: utf-8 -*-
import os
import platform
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase


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
        self.create_score()
        self.create_material('test_material')
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_material('test_material', expect_error=True)
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Path exists: test_score/materials/test_material
        '''.replace('/', os.path.sep))

    def test_force_replace(self):
        self.create_score()
        self.create_material('test_material')
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_material('test_material', force=True)
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Reading test_score/metadata.json ... OK!
                Created test_score/materials/test_material/
        '''.replace('/', os.path.sep))

    def test_internal_path(self):
        self.create_score()
        script = commandlinetools.ManageMaterialScript()
        command = ['--new', 'test_material']
        internal_path = self.score_path.joinpath('test_score', 'build')
        assert internal_path.exists()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(internal_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Reading test_score/metadata.json ... OK!
                Created test_score/materials/test_material/
        '''.replace('/', os.path.sep))

    def test_success(self):
        self.create_score()
        script = commandlinetools.ManageMaterialScript()
        command = ['--new', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating material subpackage 'test_material' ...
                Reading test_score/metadata.json ... OK!
                Created test_score/materials/test_material/
        '''.replace('/', os.path.sep))
        assert self.materials_path.joinpath('test_material').exists()
        self.compare_path_contents(self.materials_path, self.expected_files)
