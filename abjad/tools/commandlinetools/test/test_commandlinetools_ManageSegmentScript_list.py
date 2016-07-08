# -*- coding: utf-8 -*-
import os
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    def test_list_segments(self):
        self.create_score()
        self.create_segment('segment_one')
        self.create_segment('segment_two')
        self.create_segment('segment_three')
        script = commandlinetools.ManageSegmentScript()
        command = ['--list']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 2
        self.compare_captured_output(r'''
            Available segments:
                Reading test_score/segments/metadata.json ... OK!
                segment_one   [1]
                segment_two   [2]
                segment_three [3]
        '''.replace('/', os.path.sep))

    def test_list_segments_no_segments(self):
        self.create_score()
        script = commandlinetools.ManageSegmentScript()
        command = ['--list']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 2
        self.compare_captured_output(r'''
            Available segments:
                Reading test_score/segments/metadata.json ... JSON does not exist.
                No segments available.
        '''.replace('/', os.path.sep))

    def test_list_segments_unstaged(self):
        self.create_score()
        self.create_segment('segment_one')
        self.create_segment('segment_two')
        self.create_segment('segment_three')
        script = commandlinetools.ManageSegmentScript()
        segment_names = script._read_segments_list_json(
            self.score_path,
            verbose=False,
            )
        segment_names.remove('segment_two')
        script._write_segments_list_json(
            segment_names,
            score_path=self.score_path,
            verbose=False,
            )
        command = ['--list']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 2
        self.compare_captured_output(r'''
            Available segments:
                Reading test_score/segments/metadata.json ... OK!
                segment_one   [1]
                segment_three [2]
                segment_two
        '''.replace('/', os.path.sep))
