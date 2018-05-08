import abjad
import pytest
from abjad import abjad_configuration
from base import ScorePackageScriptTestCase
from unittest import mock


class Test(ScorePackageScriptTestCase):

    @mock.patch('abjad.cli.ScorePackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        call_subprocess_mock.return_value = 0
        pytest.helpers.create_score(self.test_directory_path)
        material_path = self.create_material('test_material')
        script = abjad.cli.ManageMaterialScript()
        command = ['--edit', 'test_material']
        with abjad.RedirectedStreams(stdout=self.string_io):
            with abjad.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        self.compare_captured_output(r'''
        Edit candidates: 'test_material' ...
        ''')
        definition_path = material_path.joinpath('definition.py')
        command = '{} {!s}'.format(
            abjad_configuration.get_text_editor(),
            definition_path,
            )
        call_subprocess_mock.assert_called_with(command)
