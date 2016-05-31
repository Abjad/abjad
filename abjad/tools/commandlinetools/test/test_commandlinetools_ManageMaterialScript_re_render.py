# -*- coding: utf-8 -*-
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    expected_files = [
        'test_score/test_score/materials/.gitignore',
        'test_score/test_score/materials/__init__.py',
        'test_score/test_score/materials/test_material/__init__.py',
        'test_score/test_score/materials/test_material/definition.py',
        'test_score/test_score/materials/test_material/illustration.ly',
        'test_score/test_score/materials/test_material/illustration.pdf',
        ]

    def test_success_one_material(self):
        self.create_score()
        material_path = self.create_material('test_material')
        self.illustrate_material('test_material')
        pdf_path = material_path.joinpath('illustration.pdf')
        assert pdf_path.exists()
        pdf_path.unlink()
        script = commandlinetools.ManageMaterialScript()
        command = ['--re-render', 'test_material']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Re-rendering candidates: 'test_material' ...
        Re-rendering test_score/materials/test_material/
            Writing test_score/materials/test_material/illustration.pdf ... OK!
                LilyPond runtime: ... second...
            Re-rendered test_score/materials/test_material/
        ''')
        self.compare_path_contents(self.materials_path, self.expected_files)
