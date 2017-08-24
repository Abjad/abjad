import abjad
import os
import platform
from base import ScorePackageScriptTestCase
try:
    from unittest import mock
except ImportError:
    import mock


class Test(ScorePackageScriptTestCase):

    @mock.patch('abjad.IOManager.open_file')
    def test_success_all(self, open_file_mock):
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
            expected_files = [_.replace('/', os.path.sep) for _ in expected_files]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        self.create_build_target()
        script = abjad.commandlinetools.ManageBuildTargetScript()
        command = ['--render', 'letter-portrait']
        #with abjad.RedirectedStreams(stdout=self.string_io):
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(self.build_path, expected_files)
        assert open_file_mock.called

    @mock.patch('abjad.IOManager.open_file')
    def test_success_back_cover(self, open_file_mock):
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
            expected_files = [_.replace('/', os.path.sep) for _ in expected_files]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = abjad.commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--back-cover',
            ]
        #with abjad.RedirectedStreams(stdout=self.string_io):
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)
        assert open_file_mock.called

    @mock.patch('abjad.IOManager.open_file')
    def test_success_front_cover(self, open_file_mock):
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
            expected_files = [_.replace('/', os.path.sep) for _ in expected_files]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = abjad.commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--front-cover',
            ]
        #with abjad.RedirectedStreams(stdout=self.string_io):
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)
        assert open_file_mock.called

    @mock.patch('abjad.IOManager.open_file')
    def test_success_music(self, open_file_mock):
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
            expected_files = [_.replace('/', os.path.sep) for _ in expected_files]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = abjad.commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--music',
            ]
        #with abjad.RedirectedStreams(stdout=self.string_io):
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)
        assert open_file_mock.called

    @mock.patch('abjad.IOManager.open_file')
    def test_success_parts(self, open_file_mock):
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
            expected_files = [_.replace('/', os.path.sep) for _ in expected_files]
        self.create_score()
        self.install_fancy_segment_maker()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = abjad.commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--parts',
            ]
        #with abjad.RedirectedStreams(stdout=self.string_io):
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)
        assert open_file_mock.called

    @mock.patch('abjad.IOManager.open_file')
    def test_success_preface(self, open_file_mock):
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
            expected_files = [_.replace('/', os.path.sep) for _ in expected_files]
        self.create_score()
        self.create_segment('test_segment')
        self.illustrate_segments()
        self.collect_segments()
        target_path = self.create_build_target()
        script = abjad.commandlinetools.ManageBuildTargetScript()
        command = [
            '--render', 'letter-portrait',
            '--preface',
            ]
        #with abjad.RedirectedStreams(stdout=self.string_io):
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        self.compare_path_contents(target_path, expected_files)
        assert open_file_mock.called
