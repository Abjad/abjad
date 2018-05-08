import abjad
import json
import os
import platform
import pytest
import shutil
from base import ScorePackageScriptTestCase
from io import StringIO


class Test(ScorePackageScriptTestCase):

    def test_exists(self):
        string_io = StringIO()
        with abjad.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_score(self.test_directory_path)
        assert self.score_path.exists()
        with abjad.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_score(
                self.test_directory_path, expect_error=True)
        assert self.score_path.exists()
        shutil.rmtree(str(self.score_path))
        for path in self.test_directory_path.iterdir():
            assert path in self.directory_items
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

    def test_force_replace(self):
        string_io = StringIO()
        with abjad.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_score(self.test_directory_path)
        assert self.score_path.exists()
        with abjad.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_score(self.test_directory_path, force=True)
        assert self.score_path.exists()
        shutil.rmtree(str(self.score_path))
        for path in self.test_directory_path.iterdir():
            assert path in self.directory_items
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

    def test_success(self):
        string_io = StringIO()
        with abjad.RedirectedStreams(stdout=string_io):
            pytest.helpers.create_score(self.test_directory_path)
        assert self.score_path.exists()
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
        self.compare_path_contents(self.score_path, expected_files)
        score_metadata_path = self.score_path.joinpath(
            self.score_path.name, 'metadata.json')
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
        shutil.rmtree(str(self.score_path))
        for path in self.test_directory_path.iterdir():
            assert path in self.directory_items
        pytest.helpers.compare_strings(
            actual=string_io.getvalue(),
            expected=r'''
            Creating score package 'Test Score'...
                Writing test_score/metadata.json
                Created test_score/
            '''.replace('/', os.path.sep),
        )
