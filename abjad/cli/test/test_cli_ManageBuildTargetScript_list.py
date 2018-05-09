import abjad
import pytest
import uqbar.io
from io import StringIO


def test_list(paths):
    string_io = StringIO()
    pytest.helpers.create_score(paths.test_directory_path)
    script = abjad.cli.ManageBuildTargetScript()
    command = ['--new', 'big-version']
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    command = ['--new', 'medium-version']
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    command = ['--new', 'small-version']
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    command = ['--list']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(paths.score_path):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Available build targets:
            big-version
            medium-version
            small-version
        ''',
    )
