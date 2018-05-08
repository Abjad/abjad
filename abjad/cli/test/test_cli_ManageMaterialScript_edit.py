import abjad
import pytest
import uqbar.io
from abjad import abjad_configuration
from base import ScorePackageScriptTestCase
from io import StringIO
from unittest import mock
from uqbar.strings import normalize


class Test(ScorePackageScriptTestCase):

    @mock.patch('abjad.cli.ScorePackageScript._call_subprocess')
    def test_success(self, call_subprocess_mock):
        string_io = StringIO()
        call_subprocess_mock.return_value = 0
        pytest.helpers.create_score(self.test_directory_path)
        material_path = pytest.helpers.create_material(
            self.test_directory_path, 'test_material')
        script = abjad.cli.ManageMaterialScript()
        command = ['--edit', 'test_material']
        with abjad.RedirectedStreams(stdout=string_io):
            with uqbar.io.DirectoryChange(self.score_path):
                try:
                    script(command)
                except SystemExit as e:
                    raise RuntimeError('SystemExit: {}'.format(e.code))
        pytest.helpers.compare_strings(
            actual=string_io.getvalue(),
            expected=r'''Edit candidates: 'test_material' ...''',
        )
        definition_path = material_path.joinpath('definition.py')
        command = '{} {!s}'.format(
            abjad_configuration.get_text_editor(),
            definition_path,
        )
        call_subprocess_mock.assert_called_with(command)
