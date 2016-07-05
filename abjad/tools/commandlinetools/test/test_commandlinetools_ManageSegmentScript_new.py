# -*- coding: utf-8 -*-
import os
import platform
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    expected_files = [
        'test_score/test_score/segments/.gitignore',
        'test_score/test_score/segments/__init__.py',
        'test_score/test_score/segments/metadata.json',
        'test_score/test_score/segments/test_segment/__init__.py',
        'test_score/test_score/segments/test_segment/definition.py',
        ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    def test_exists(self):
        self.create_score()
        self.create_segment('test_segment')
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_segment('test_segment', expect_error=True)
        self.compare_captured_output(r'''
            Creating segment subpackage 'test_segment' ...
                Path exists: test_score/segments/test_segment
        '''.replace('/', os.path.sep))

    def test_force_replace(self):
        self.create_score()
        self.create_segment('test_segment')
        with systemtools.RedirectedStreams(stdout=self.string_io):
            self.create_segment('test_segment', force=True)
        self.compare_captured_output(r'''
            Creating segment subpackage 'test_segment' ...
                Reading test_score/metadata.json ... OK!
                Reading test_score/segments/metadata.json ... OK!
                Created test_score/segments/test_segment/
        '''.replace('/', os.path.sep))

    def test_internal_path(self):
        self.create_score()
        script = commandlinetools.ManageSegmentScript()
        command = ['--new', 'test_segment']
        internal_path = self.score_path.joinpath('test_score', 'build')
        assert internal_path.exists()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(internal_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating segment subpackage 'test_segment' ...
                Reading test_score/metadata.json ... OK!
                Reading test_score/segments/metadata.json ... JSON does not exist.
                Writing test_score/segments/metadata.json
                Created test_score/segments/test_segment/
        '''.replace('/', os.path.sep))

    def test_success(self):
        self.create_score()
        script = commandlinetools.ManageSegmentScript()
        try:
            names = script._read_segments_list_json(
                self.score_path,
                verbose=False,
                )
            assert names == []
        except SystemExit:
            raise RuntimeError('SystemExit')
        command = ['--new', 'test_segment']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
            Creating segment subpackage 'test_segment' ...
                Reading test_score/metadata.json ... OK!
                Reading test_score/segments/metadata.json ... JSON does not exist.
                Writing test_score/segments/metadata.json
                Created test_score/segments/test_segment/
        '''.replace('/', os.path.sep))
        assert self.segments_path.joinpath('test_segment').exists()
        self.compare_path_contents(self.segments_path, self.expected_files)
        try:
            names = script._read_segments_list_json(
                self.score_path,
                verbose=False,
                )
            assert names == ['test_segment']
        except SystemExit:
            raise RuntimeError('SystemExit')
