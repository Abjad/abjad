import abjad
import os
import platform
import pytest
import uqbar.io
from io import StringIO


def test_success_one_material(paths, open_file_mock):
    string_io = StringIO()
    pytest.helpers.create_score(paths.test_directory_path)
    material_path = pytest.helpers.create_material(
        paths.test_directory_path, 'test_material')
    pytest.helpers.illustrate_material(paths.test_directory_path, 'test_material')
    pdf_path = material_path.joinpath('illustration.pdf')
    assert pdf_path.exists()
    pdf_path.unlink()
    script = abjad.cli.ManageMaterialScript()
    command = ['--render', 'test_material']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(paths.score_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Rendering candidates: 'test_material' ...
        Rendering test_score/materials/test_material/
            Writing test_score/materials/test_material/illustration.pdf ... OK!
                LilyPond runtime: ... second...
            Rendered test_score/materials/test_material/
        '''.replace('/', os.path.sep),
    )
    expected_files = [
        'test_score/test_score/materials/.gitignore',
        'test_score/test_score/materials/__init__.py',
        'test_score/test_score/materials/test_material/__init__.py',
        'test_score/test_score/materials/test_material/definition.py',
        'test_score/test_score/materials/test_material/illustration.ly',
        'test_score/test_score/materials/test_material/illustration.pdf',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    pytest.helpers.compare_path_contents(
        paths.materials_path,
        expected_files,
        paths.test_directory_path,
    )
