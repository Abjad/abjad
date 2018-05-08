import abjad
import pytest
import uqbar.io
from base import ScorePackageScriptTestCase
from io import StringIO
from uqbar.strings import normalize


class Test(ScorePackageScriptTestCase):

    def test_list_materials(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        pytest.helpers.create_material(self.test_directory_path, 'foo')
        pytest.helpers.create_material(self.test_directory_path, 'bar')
        pytest.helpers.create_material(self.test_directory_path, 'baz')
        pytest.helpers.create_material(self.test_directory_path, 'quux')
        script = abjad.cli.ManageMaterialScript()
        command = ['--list']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 2
        pytest.helpers.compare_strings(string_io.getvalue(), r'''
        Available materials:
            Markup:
                bar [Markup]
                baz [Markup]
                foo [Markup]
                quux [Markup]
        ''')

    def test_list_materials_no_materials(self):
        string_io = StringIO()
        pytest.helpers.create_score(self.test_directory_path)
        script = abjad.cli.ManageMaterialScript()
        command = ['--list']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 2
        pytest.helpers.compare_strings(string_io.getvalue(), r'''
        Available materials:
            No materials available.
        ''')
