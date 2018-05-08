import abjad
import pytest
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    def test_list_materials(self):
        pytest.helpers.create_score(self.test_directory_path)
        pytest.helpers.create_material(self.test_directory_path, 'foo')
        pytest.helpers.create_material(self.test_directory_path, 'bar')
        pytest.helpers.create_material(self.test_directory_path, 'baz')
        pytest.helpers.create_material(self.test_directory_path, 'quux')
        script = abjad.cli.ManageMaterialScript()
        command = ['--list']
        with abjad.RedirectedStreams(stdout=self.string_io):
            with abjad.TemporaryDirectoryChange(str(self.score_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 2
        self.compare_captured_output(r'''
        Available materials:
            Markup:
                bar [Markup]
                baz [Markup]
                foo [Markup]
                quux [Markup]
        ''')

    def test_list_materials_no_materials(self):
        pytest.helpers.create_score(self.test_directory_path)
        script = abjad.cli.ManageMaterialScript()
        command = ['--list']
        with abjad.RedirectedStreams(stdout=self.string_io):
            with abjad.TemporaryDirectoryChange(str(self.score_path)):
                with pytest.raises(SystemExit) as exception_info:
                    script(command)
                assert exception_info.value.code == 2
        self.compare_captured_output(r'''
        Available materials:
            No materials available.
        ''')
