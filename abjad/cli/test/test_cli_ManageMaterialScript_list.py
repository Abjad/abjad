import abjad
import pytest
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    def test_list_materials(self):
        self.create_score()
        self.create_material('foo')
        self.create_material('bar')
        self.create_material('baz')
        self.create_material('quux')
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
        self.create_score()
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
