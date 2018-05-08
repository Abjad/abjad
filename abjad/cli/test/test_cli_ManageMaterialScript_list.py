import abjad
import pytest
import uqbar.io
from io import StringIO


def test_list_materials(paths):
    string_io = StringIO()
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.create_material(paths.test_directory_path, 'foo')
    pytest.helpers.create_material(paths.test_directory_path, 'bar')
    pytest.helpers.create_material(paths.test_directory_path, 'baz')
    pytest.helpers.create_material(paths.test_directory_path, 'quux')
    script = abjad.cli.ManageMaterialScript()
    command = ['--list']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(paths.score_path):
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 2
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Available materials:
            Markup:
                bar [Markup]
                baz [Markup]
                foo [Markup]
                quux [Markup]
        ''',
    )


def test_list_materials_no_materials(paths):
    string_io = StringIO()
    pytest.helpers.create_score(paths.test_directory_path)
    script = abjad.cli.ManageMaterialScript()
    command = ['--list']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(paths.score_path):
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 2
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Available materials:
            No materials available.
        ''',
    )
