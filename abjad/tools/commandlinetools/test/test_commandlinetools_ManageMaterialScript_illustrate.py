# -*- coding: utf-8 -*-
import os
import platform
from abjad.tools import commandlinetools
from abjad.tools import stringtools
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

    expected_illustration_contents = stringtools.normalize(
        r'''
        \language "english"

        \header {
            tagline = ##f
        }

        \layout {}

        \paper {}

        \markup { "An example illustrable material." }
        '''
        )

    def test_lilypond_error(self):
        """
        Handle failing LilyPond rendering.
        """
        self.create_score()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(stringtools.normalize(r'''
            # -*- coding: utf-8 -*-
            from abjad.tools import lilypondfiletools


            test_material = lilypondfiletools.make_basic_lilypond_file()
            test_material.items.append(r'\this-does-not-exist')
            '''))
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_material' ...
            Illustrating test_score/materials/test_material/
                Importing test_score.materials.test_material.definition
                    Abjad runtime: ... second...
                Writing test_score/materials/test_material/illustration.ly ... OK!
                Writing test_score/materials/test_material/illustration.pdf ... Failed!
        '''.replace('/', os.path.sep))
        illustration_ly_path = material_path.joinpath('illustration.ly')
        assert illustration_ly_path.exists()
        self.compare_lilypond_contents(
            illustration_ly_path, stringtools.normalize(r'''
            \language "english"

            \header {}

            \layout {}

            \paper {}

            \this-does-not-exist
            '''))

    def test_missing_definition(self):
        """
        Handle missing definition.
        """
        self.create_score()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        definition_path.unlink()
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_material' ...
            Illustrating test_score/materials/test_material/
                Importing test_score.materials.test_material.definition
        '''.replace('/', os.path.sep))

    def test_python_cannot_illustrate(self):
        """
        Handle un-illustrables.
        """
        self.create_score()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(stringtools.normalize(r'''
            # -*- coding: utf-8 -*-

            test_material = None
            '''))
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_material' ...
            Illustrating test_score/materials/test_material/
                Importing test_score.materials.test_material.definition
                Cannot illustrate material of type NoneType.
        '''.replace('/', os.path.sep))

    def test_python_error_on_illustrate(self):
        """
        Handle exceptions inside the Python module on __call__().
        """
        self.create_score()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'w') as file_pointer:
            file_pointer.write(stringtools.normalize(r'''
            # -*- coding: utf-8 -*-
            from abjad.tools import abctools


            class Foo(object):
                def __illustrate__(self):
                    raise TypeError('This is fake.')

            test_material = Foo()
            '''))
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_material' ...
            Illustrating test_score/materials/test_material/
                Importing test_score.materials.test_material.definition
        '''.replace('/', os.path.sep))

    def test_python_error_on_import(self):
        """
        Handle exceptions inside the Python module on import.
        """
        self.create_score()
        material_path = self.create_material('test_material')
        definition_path = material_path.joinpath('definition.py')
        with open(str(definition_path), 'a') as file_pointer:
            file_pointer.write('\n\nfailure = 1 / 0\n')
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
            Illustration candidates: 'test_material' ...
            Illustrating test_score/materials/test_material/
                Importing test_score.materials.test_material.definition
        '''.replace('/', os.path.sep))

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_all_materials(self, open_file_mock):
        self.create_score()
        self.create_material('material_one')
        self.create_material('material_two')
        self.create_material('material_three')
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', '*']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
            Illustration candidates: '*' ...
            Illustrating test_score/materials/material_one/
                Importing test_score.materials.material_one.definition
                    Abjad runtime: ... second...
                Writing test_score/materials/material_one/illustration.ly ... OK!
                Writing test_score/materials/material_one/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/materials/material_one/
            Illustrating test_score/materials/material_three/
                Importing test_score.materials.material_three.definition
                    Abjad runtime: ... second...
                Writing test_score/materials/material_three/illustration.ly ... OK!
                Writing test_score/materials/material_three/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/materials/material_three/
            Illustrating test_score/materials/material_two/
                Importing test_score.materials.material_two.definition
                    Abjad runtime: ... second...
                Writing test_score/materials/material_two/illustration.ly ... OK!
                Writing test_score/materials/material_two/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/materials/material_two/
        '''.replace('/', os.path.sep))
        assert self.materials_path.joinpath(
            'material_one',
            'illustration.pdf',
            ).exists()
        assert self.materials_path.joinpath(
            'material_two',
            'illustration.pdf',
            ).exists()
        assert self.materials_path.joinpath(
            'material_three',
            'illustration.pdf',
            ).exists()

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_filtered_materials(self, open_file_mock):
        self.create_score()
        self.create_material('material_one')
        self.create_material('material_two')
        self.create_material('material_three')
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', 'material_t*']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
            Illustration candidates: 'material_t*' ...
            Illustrating test_score/materials/material_three/
                Importing test_score.materials.material_three.definition
                    Abjad runtime: ... second...
                Writing test_score/materials/material_three/illustration.ly ... OK!
                Writing test_score/materials/material_three/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/materials/material_three/
            Illustrating test_score/materials/material_two/
                Importing test_score.materials.material_two.definition
                    Abjad runtime: ... second...
                Writing test_score/materials/material_two/illustration.ly ... OK!
                Writing test_score/materials/material_two/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/materials/material_two/
        '''.replace('/', os.path.sep))
        assert not self.materials_path.joinpath(
            'material_one',
            'illustration.pdf',
            ).exists()
        assert self.materials_path.joinpath(
            'material_two',
            'illustration.pdf',
            ).exists()
        assert self.materials_path.joinpath(
            'material_three',
            'illustration.pdf',
            ).exists()

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_success_one_material(self, open_file_mock):
        self.create_score()
        self.create_material('test_material')
        script = commandlinetools.ManageMaterialScript()
        command = ['--illustrate', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
            Illustration candidates: 'test_material' ...
            Illustrating test_score/materials/test_material/
                Importing test_score.materials.test_material.definition
                    Abjad runtime: ... second...
                Writing test_score/materials/test_material/illustration.ly ... OK!
                Writing test_score/materials/test_material/illustration.pdf ... OK!
                    LilyPond runtime: ... second...
                Illustrated test_score/materials/test_material/
        '''.replace('/', os.path.sep))
        self.compare_path_contents(self.materials_path, self.expected_files)
        illustration_path = self.materials_path.joinpath(
            'test_material', 'illustration.ly')
        self.compare_lilypond_contents(
            illustration_path,
            self.expected_illustration_contents,
            )
