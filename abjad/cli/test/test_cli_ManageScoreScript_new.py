import json
import os
import platform
import pytest
import shutil
import uqbar.io
from io import StringIO


def test_exists(paths):
    string_io = StringIO()
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_score(paths.test_directory_path)
    assert paths.score_path.exists()
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_score(
            paths.test_directory_path, expect_error=True)
    assert paths.score_path.exists()
    shutil.rmtree(str(paths.score_path))
    for path in paths.test_directory_path.iterdir():
        assert path in paths.directory_items
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Creating score package 'Test Score'...
            Writing test_score/metadata.json
            Created test_score/
        Creating score package 'Test Score'...
            Directory test_score already exists.
        '''.replace('/', os.path.sep),
    )


def test_force_replace(paths):
    string_io = StringIO()
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_score(paths.test_directory_path)
    assert paths.score_path.exists()
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_score(paths.test_directory_path, force=True)
    assert paths.score_path.exists()
    shutil.rmtree(str(paths.score_path))
    for path in paths.test_directory_path.iterdir():
        assert path in paths.directory_items
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Creating score package 'Test Score'...
            Writing test_score/metadata.json
            Created test_score/
        Creating score package 'Test Score'...
            Writing test_score/metadata.json
            Created test_score/
        '''.replace('/', os.path.sep),
    )


def test_success(paths):
    string_io = StringIO()
    with uqbar.io.RedirectedStreams(stdout=string_io):
        pytest.helpers.create_score(paths.test_directory_path)
    assert paths.score_path.exists()
    expected_files = [
        'test_score/.gitignore',
        'test_score/.travis.yml',
        'test_score/README.md',
        'test_score/requirements.txt',
        'test_score/setup.cfg',
        'test_score/setup.py',
        'test_score/test_score/__init__.py',
        'test_score/test_score/__metadata__.py',
        'test_score/test_score/builds/.gitignore',
        'test_score/test_score/builds/assets/.gitignore',
        'test_score/test_score/builds/assets/instrumentation.tex',
        'test_score/test_score/builds/assets/performance-notes.tex',
        'test_score/test_score/builds/parts.ily',
        'test_score/test_score/builds/segments.ily',
        'test_score/test_score/builds/segments/.gitignore',
        'test_score/test_score/distribution/.gitignore',
        'test_score/test_score/etc/.gitignore',
        'test_score/test_score/materials/.gitignore',
        'test_score/test_score/materials/__init__.py',
        'test_score/test_score/metadata.json',
        'test_score/test_score/segments/.gitignore',
        'test_score/test_score/segments/__init__.py',
        'test_score/test_score/stylesheets/.gitignore',
        'test_score/test_score/stylesheets/nonfirst-segment.ily',
        'test_score/test_score/stylesheets/parts.ily',
        'test_score/test_score/stylesheets/stylesheet.ily',
        'test_score/test_score/test/.gitignore',
        'test_score/test_score/test/test_materials.py',
        'test_score/test_score/test/test_segments.py',
        'test_score/test_score/tools/.gitignore',
        'test_score/test_score/tools/ScoreTemplate.py',
        'test_score/test_score/tools/SegmentMaker.py',
        'test_score/test_score/tools/__init__.py',
    ]
    if platform.system().lower() == 'windows':
        expected_files = [
            _.replace('/', os.path.sep)
            for _ in expected_files
        ]
    pytest.helpers.compare_path_contents(
        paths.score_path,
        expected_files,
        paths.test_directory_path,
    )
    score_metadata_path = paths.score_path.joinpath(
        paths.score_path.name, 'metadata.json')
    assert score_metadata_path.exists()
    with open(str(score_metadata_path), 'r') as file_pointer:
        metadata = json.loads(file_pointer.read())
    assert metadata == {
        'composer_email': 'josiah.oberholtzer@gmail.com',
        'composer_github': 'josiah-wolf-oberholtzer',
        'composer_library': 'consort',
        'composer_name': 'Josiah Wolf Oberholtzer',
        'composer_website': 'www.josiahwolfoberholtzer.com',
        'title': 'Test Score',
        'year': 2016,
    }
    shutil.rmtree(str(paths.score_path))
    for path in paths.test_directory_path.iterdir():
        assert path in paths.directory_items
    pytest.helpers.compare_strings(
        actual=string_io.getvalue(),
        expected=r'''
        Creating score package 'Test Score'...
            Writing test_score/metadata.json
            Created test_score/
        '''.replace('/', os.path.sep),
    )
