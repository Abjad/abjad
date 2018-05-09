import abjad
import os
import platform
import pytest
import uqbar.io
from io import StringIO


def test_success(paths, open_file_mock):
    expected_files = [
        'test_score/test_score/distribution/.gitignore',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-cello.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-viola.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-violin-i.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-parts-violin-ii.pdf',
        'test_score/test_score/distribution/letter-portrait/letter-portrait-score.pdf',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    string_io = StringIO()
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.install_fancy_segment_maker(paths.test_directory_path)
    pytest.helpers.create_segment(paths.test_directory_path, 'test_segment')
    pytest.helpers.illustrate_segments(paths.test_directory_path)
    pytest.helpers.collect_segments(paths.test_directory_path)
    pytest.helpers.create_build_target(paths.test_directory_path)
    script = abjad.cli.ManageBuildTargetScript()
    command = ['--render', 'letter-portrait']
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    command = ['--distribute', 'letter-portrait']
    with uqbar.io.RedirectedStreams(stdout=string_io):
        with uqbar.io.DirectoryChange(paths.score_path):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Distributing 'letter-portrait'
            score.pdf --> letter-portrait-score.pdf
            parts-cello.pdf --> letter-portrait-parts-cello.pdf
            parts-viola.pdf --> letter-portrait-parts-viola.pdf
            parts-violin-i.pdf --> letter-portrait-parts-violin-i.pdf
            parts-violin-ii.pdf --> letter-portrait-parts-violin-ii.pdf
        ''',
    )
    pytest.helpers.compare_path_contents(
        paths.distribution_path,
        expected_files,
        paths.test_directory_path,
    )
