# -*- coding: utf-8 -*-
from abjad.tools import systemtools
import pytest
try:
    from unittest import mock
except ImportError:
    import mock

midi_player, text_editor, pdf_viewer = (
    'midi_player_application',
    'text_editor_application',
    'pdf_viewer_application',
)
test_files_to_viewer_mapping = {
    'test.midi': midi_player,
    'test.py': text_editor,
    'test.txt': text_editor,
    'test.pdf': pdf_viewer,
}
test_files = test_files_to_viewer_mapping.keys()
empty_abjad_configuration, nonempty_abjad_configuration = (
    (
        'abjad.abjad_configuration', {
            'midi_player': None,
            'text_editor': None,
            'pdf_viewer': None,
        }
    ),
    (
        'abjad.abjad_configuration', {
            'midi_player': midi_player,
            'text_editor': text_editor,
            'pdf_viewer': pdf_viewer,
        },
    )
)
abjad_configurations = (
    empty_abjad_configuration,
    nonempty_abjad_configuration,
)
applications = (None, 'custom-viewer')


@mock.patch('sys.platform', 'linux2')
@mock.patch('abjad.systemtools.IOManager.spawn_subprocess')
@pytest.mark.parametrize('configuration', abjad_configurations)
@pytest.mark.parametrize('file_path', test_files)
@pytest.mark.parametrize('application', applications)
def test_systemtools_IOManager__open_file_01(spawn_subprocess_mock,
                                             configuration,
                                             file_path,
                                             application):
    with mock.patch(*configuration):
        systemtools.IOManager.open_file(
            file_path=file_path,
            application=application,
        )
        command = None
        if application is None:
            command = 'xdg-open {}'.format(file_path)
        else:
            command = '{} {}'.format(application, file_path)
        spawn_subprocess_mock.assert_called_with(command)


@mock.patch('sys.platform', 'darwin')
@mock.patch('abjad.systemtools.IOManager.spawn_subprocess')
@pytest.mark.parametrize('configuration', abjad_configurations)
@pytest.mark.parametrize('file_path', test_files)
@pytest.mark.parametrize('application', applications)
def test_systemtools_IOManager__open_file_02(spawn_subprocess_mock,
                                             configuration,
                                             file_path,
                                             application):
    with mock.patch(*configuration):
        systemtools.IOManager.open_file(
            file_path=file_path,
            application=application,
        )
        is_empty_config = configuration == empty_abjad_configuration
        command = None
        if application is None and is_empty_config:
            command = 'open {}'.format(file_path)
        elif application is None and not is_empty_config:
            application_ = test_files_to_viewer_mapping[file_path]
            command = '{} {}'.format(application_, file_path)
        else:
            command = '{} {}'.format(application, file_path)
        spawn_subprocess_mock.assert_called_with(command)


@mock.patch('sys.platform', 'win32')
@mock.patch('os.startfile', create=True)
@pytest.mark.parametrize('configuration', abjad_configurations)
@pytest.mark.parametrize('file_path', test_files)
@pytest.mark.parametrize('application', applications)
def test_systemtools_IOManager__open_file_03(startfile_mock,
                                             configuration,
                                             file_path,
                                             application):
    with mock.patch(*configuration):
        systemtools.IOManager.open_file(
            file_path=file_path,
            application=application,
        )
        startfile_mock.assert_called_with(file_path)
