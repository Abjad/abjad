import abjad
import os
import platform
import pytest
import uqbar.io


def test_success_all(paths, open_file_mock):
    expected_files = [
        'test_score/test_score/builds/.gitignore',
        'test_score/test_score/builds/assets/.gitignore',
        'test_score/test_score/builds/assets/instrumentation.tex',
        'test_score/test_score/builds/assets/performance-notes.tex',
        'test_score/test_score/builds/letter-portrait/back-cover.pdf',
        'test_score/test_score/builds/letter-portrait/back-cover.tex',
        'test_score/test_score/builds/letter-portrait/front-cover.pdf',
        'test_score/test_score/builds/letter-portrait/front-cover.tex',
        'test_score/test_score/builds/letter-portrait/music.ly',
        'test_score/test_score/builds/letter-portrait/music.pdf',
        'test_score/test_score/builds/letter-portrait/parts.ly',
        'test_score/test_score/builds/letter-portrait/preface.pdf',
        'test_score/test_score/builds/letter-portrait/preface.tex',
        'test_score/test_score/builds/letter-portrait/score.pdf',
        'test_score/test_score/builds/letter-portrait/score.tex',
        'test_score/test_score/builds/parts.ily',
        'test_score/test_score/builds/segments.ily',
        'test_score/test_score/builds/segments/.gitignore',
        'test_score/test_score/builds/segments/test-segment.ily',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    pytest.helpers.create_score(paths.test_directory_path)
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
    pytest.helpers.compare_path_contents(
        paths.build_path,
        expected_files,
        paths.test_directory_path,
    )
    assert open_file_mock.called


def test_success_back_cover(paths, open_file_mock):
    expected_files = [
        'test_score/test_score/builds/letter-portrait/back-cover.pdf',
        'test_score/test_score/builds/letter-portrait/back-cover.tex',
        'test_score/test_score/builds/letter-portrait/front-cover.tex',
        'test_score/test_score/builds/letter-portrait/music.ly',
        'test_score/test_score/builds/letter-portrait/parts.ly',
        'test_score/test_score/builds/letter-portrait/preface.tex',
        'test_score/test_score/builds/letter-portrait/score.tex',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.create_segment(paths.test_directory_path, 'test_segment')
    pytest.helpers.illustrate_segments(paths.test_directory_path)
    pytest.helpers.collect_segments(paths.test_directory_path)
    target_path = pytest.helpers.create_build_target(paths.test_directory_path)
    script = abjad.cli.ManageBuildTargetScript()
    command = [
        '--render', 'letter-portrait',
        '--back-cover',
    ]
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    pytest.helpers.compare_path_contents(
        target_path,
        expected_files,
        paths.test_directory_path,
    )
    assert open_file_mock.called


def test_success_front_cover(paths, open_file_mock):
    expected_files = [
        'test_score/test_score/builds/letter-portrait/back-cover.tex',
        'test_score/test_score/builds/letter-portrait/front-cover.pdf',
        'test_score/test_score/builds/letter-portrait/front-cover.tex',
        'test_score/test_score/builds/letter-portrait/music.ly',
        'test_score/test_score/builds/letter-portrait/parts.ly',
        'test_score/test_score/builds/letter-portrait/preface.tex',
        'test_score/test_score/builds/letter-portrait/score.tex',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.create_segment(paths.test_directory_path, 'test_segment')
    pytest.helpers.illustrate_segments(paths.test_directory_path)
    pytest.helpers.collect_segments(paths.test_directory_path)
    target_path = pytest.helpers.create_build_target(paths.test_directory_path)
    script = abjad.cli.ManageBuildTargetScript()
    command = [
        '--render', 'letter-portrait',
        '--front-cover',
    ]
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    pytest.helpers.compare_path_contents(
        target_path,
        expected_files,
        paths.test_directory_path,
    )
    assert open_file_mock.called


def test_success_music(paths, open_file_mock):
    expected_files = [
        'test_score/test_score/builds/letter-portrait/back-cover.tex',
        'test_score/test_score/builds/letter-portrait/front-cover.tex',
        'test_score/test_score/builds/letter-portrait/music.ly',
        'test_score/test_score/builds/letter-portrait/music.pdf',
        'test_score/test_score/builds/letter-portrait/parts.ly',
        'test_score/test_score/builds/letter-portrait/preface.tex',
        'test_score/test_score/builds/letter-portrait/score.tex',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.create_segment(paths.test_directory_path, 'test_segment')
    pytest.helpers.illustrate_segments(paths.test_directory_path)
    pytest.helpers.collect_segments(paths.test_directory_path)
    target_path = pytest.helpers.create_build_target(paths.test_directory_path)
    script = abjad.cli.ManageBuildTargetScript()
    command = [
        '--render', 'letter-portrait',
        '--music',
    ]
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    pytest.helpers.compare_path_contents(
        target_path,
        expected_files,
        paths.test_directory_path,
    )
    assert open_file_mock.called


def test_success_parts(paths, open_file_mock):
    expected_files = [
        'test_score/test_score/builds/letter-portrait/back-cover.tex',
        'test_score/test_score/builds/letter-portrait/front-cover.tex',
        'test_score/test_score/builds/letter-portrait/music.ly',
        'test_score/test_score/builds/letter-portrait/parts-cello.pdf',
        'test_score/test_score/builds/letter-portrait/parts-viola.pdf',
        'test_score/test_score/builds/letter-portrait/parts-violin-i.pdf',
        'test_score/test_score/builds/letter-portrait/parts-violin-ii.pdf',
        'test_score/test_score/builds/letter-portrait/parts.ly',
        'test_score/test_score/builds/letter-portrait/preface.tex',
        'test_score/test_score/builds/letter-portrait/score.tex',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep) for _ in expected_files
        ]
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.install_fancy_segment_maker(paths.test_directory_path)
    pytest.helpers.create_segment(paths.test_directory_path, 'test_segment')
    pytest.helpers.illustrate_segments(paths.test_directory_path)
    pytest.helpers.collect_segments(paths.test_directory_path)
    target_path = pytest.helpers.create_build_target(paths.test_directory_path)
    script = abjad.cli.ManageBuildTargetScript()
    command = [
        '--render', 'letter-portrait',
        '--parts',
    ]
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    pytest.helpers.compare_path_contents(
        target_path,
        expected_files,
        paths.test_directory_path,
    )
    assert open_file_mock.called


def test_success_preface(paths, open_file_mock):
    expected_files = [
        'test_score/test_score/builds/letter-portrait/back-cover.tex',
        'test_score/test_score/builds/letter-portrait/front-cover.tex',
        'test_score/test_score/builds/letter-portrait/music.ly',
        'test_score/test_score/builds/letter-portrait/parts.ly',
        'test_score/test_score/builds/letter-portrait/preface.pdf',
        'test_score/test_score/builds/letter-portrait/preface.tex',
        'test_score/test_score/builds/letter-portrait/score.tex',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.create_segment(paths.test_directory_path, 'test_segment')
    pytest.helpers.illustrate_segments(paths.test_directory_path)
    pytest.helpers.collect_segments(paths.test_directory_path)
    target_path = pytest.helpers.create_build_target(paths.test_directory_path)
    script = abjad.cli.ManageBuildTargetScript()
    command = [
        '--render', 'letter-portrait',
        '--preface',
    ]
    with uqbar.io.DirectoryChange(paths.score_path):
        try:
            script(command)
        except SystemExit:
            raise RuntimeError('SystemExit')
    pytest.helpers.compare_path_contents(
        target_path,
        expected_files,
        paths.test_directory_path,
    )
    assert open_file_mock.called
