import abjad
import pathlib
import pytest
import shutil
import sys
import uqbar.io


class ScorePackageScriptTestCase(abjad.TestCase):
    r'''A base test class for score-package scripts.
    '''

    test_path = pathlib.Path(__file__).parent
    score_path = test_path.joinpath('test_score')
    build_path = score_path.joinpath('test_score', 'builds')
    distribution_path = score_path.joinpath('test_score', 'distribution')
    materials_path = score_path.joinpath('test_score', 'materials')
    segments_path = score_path.joinpath('test_score', 'segments')
    tools_path = score_path.joinpath('test_score', 'tools')

    # ### TEST LIFECYCLE ### #

    def setUp(self):
        super(ScorePackageScriptTestCase, self).setUp()
        if self.score_path.exists():
            shutil.rmtree(self.score_path)
        self.directory_items = set(self.test_path.iterdir())
        sys.path.insert(0, str(self.score_path))

    def tearDown(self):
        super(ScorePackageScriptTestCase, self).tearDown()
        for path in sorted(self.test_path.iterdir()):
            if path in self.directory_items:
                continue
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)
        sys.path.remove(str(self.score_path))
        for path, module in tuple(sys.modules.items()):
            if not path or not module:
                continue
            if path.startswith('test_score'):
                del(sys.modules[path])

    # ### UTILITY METHODS ### #

    def collect_segments(self):
        script = abjad.cli.ManageSegmentScript()
        command = ['--collect']
        with uqbar.io.DirectoryChange(self.score_path):
            script(command)

    def create_build_target(
        self,
        force=False,
        expect_error=False,
    ):
        script = abjad.cli.ManageBuildTargetScript()
        command = ['--new']
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(self.score_path):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        return self.build_path.joinpath('letter-portrait')

    def create_material(
        self,
        material_name='test_material',
        force=False,
        expect_error=False,
    ):
        script = abjad.cli.ManageMaterialScript()
        command = ['--new', material_name]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(self.score_path):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        return self.score_path.joinpath(
            self.score_path.name,
            'materials',
            material_name,
            )

    def create_score(self, force=False, expect_error=False):
        script = abjad.cli.ManageScoreScript()
        command = [
            '--new',
            'Test Score',
            '-y', '2016',
            '-n', 'Josiah Wolf Oberholtzer',
            '-e', 'josiah.oberholtzer@gmail.com',
            '-g', 'josiah-wolf-oberholtzer',
            '-l', 'consort',
            '-w', 'www.josiahwolfoberholtzer.com',
            ]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(self.test_path):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')

    def create_segment(
        self,
        segment_name='test_segment',
        force=False,
        expect_error=False,
    ):
        script = abjad.cli.ManageSegmentScript()
        command = ['--new', segment_name]
        if force:
            command.insert(0, '-f')
        with uqbar.io.DirectoryChange(self.score_path):
            if expect_error:
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
            else:
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        return self.score_path.joinpath(
            self.score_path.name,
            'segments',
            segment_name,
            )

    def illustrate_material(self, material_name):
        script = abjad.cli.ManageMaterialScript()
        command = ['--illustrate', material_name]
        with uqbar.io.DirectoryChange(self.score_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segment(self, segment_name):
        script = abjad.cli.ManageSegmentScript()
        command = ['--illustrate', segment_name]
        with uqbar.io.DirectoryChange(self.score_path):
            try:
                script(command)
            except SystemExit as e:
                raise RuntimeError('SystemExit: {}'.format(e.code))

    def illustrate_segments(self):
        script = abjad.cli.ManageSegmentScript()
        command = ['--illustrate', '*']
        with uqbar.io.DirectoryChange(self.score_path):
            script(command)

    def install_fancy_segment_maker(self):
        segment_maker_path = self.tools_path.joinpath('SegmentMaker.py')
        with segment_maker_path.open('w') as file_pointer:
            file_pointer.write(pytest.helpers.get_fancy_segment_maker_code())
        parts_path = self.build_path.joinpath('parts.ily')
        with parts_path.open('w') as file_pointer:
            file_pointer.write(pytest.helpers.get_fancy_parts_code())
