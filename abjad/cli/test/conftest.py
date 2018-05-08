import abjad.cli
import doctest
import pathlib
import pytest
import re
import shutil
import sys
import types
import uqbar.io
import uqbar.strings
from unittest import mock


pytest_plugins = ['helpers_namespace']


# ### DATA ### #

ansi_escape = re.compile(r'\x1b[^m]*m')
package_name = 'test_score'


# ### FIXTURES ### #

@pytest.fixture
def call_subprocess_mock():
    patcher = mock.patch('abjad.cli.ScorePackageScript._call_subprocess')
    yield patcher.start()
    patcher.stop()


@pytest.fixture
def open_file_mock():
    patcher = mock.patch('abjad.IOManager.open_file')
    yield patcher.start()
    patcher.stop()


@pytest.fixture
def paths(tmpdir):
    test_directory_path = pathlib.Path(tmpdir)
    score_path = test_directory_path / package_name
    inner_path = score_path / package_name
    build_path = inner_path / 'builds'
    distribution_path = inner_path / 'distribution'
    materials_path = inner_path / 'materials'
    segments_path = inner_path / 'segments'
    tools_path = inner_path / 'tools'
    paths = types.SimpleNamespace(
        test_directory_path=test_directory_path,
        score_path=score_path,
        build_path=build_path,
        distribution_path=distribution_path,
        materials_path=materials_path,
        segments_path=segments_path,
        tools_path=tools_path,
    )
    if score_path.exists():
        shutil.rmtree(score_path)
    sys.path.insert(0, str(score_path))
    yield paths
    sys.path.remove(str(score_path))
    for path, module in tuple(sys.modules.items()):
        if not path or not module:
            continue
        if path.startswith(package_name):
            del(sys.modules[path])


# ### HELPERS ### #


@pytest.helpers.register
def collect_segments(test_directory_path):
    script = abjad.cli.ManageSegmentScript()
    command = ['--collect']
    score_path = test_directory_path / package_name
    with uqbar.io.DirectoryChange(score_path):
        script(command)


@pytest.helpers.register
def compare_lilypond_contents(ly_path, expected_contents):
    expected_contents = uqbar.strings.normalize(expected_contents)
    with open(str(ly_path), 'r') as file_pointer:
        contents = file_pointer.read()
    if ly_path.suffix == '.ly':
        contents = contents.splitlines()
        while 'version' not in contents[0]:
            contents.pop(0)
        contents.pop(0)
        contents = '\n'.join(contents)
    contents = uqbar.strings.normalize(contents)
    pytest.helpers.compare_strings(
        expected=expected_contents,
        actual=contents,
    )


@pytest.helpers.register
def compare_path_contents(path_to_search, expected_files, test_path):
    actual_files = sorted(
        str(path.relative_to(test_path))
        for path in sorted(path_to_search.glob('**/*.*'))
        if '__pycache__' not in path.parts and
        path.suffix != '.pyc'
    )
    pytest.helpers.compare_strings(
        actual='\n'.join(str(_) for _ in actual_files),
        expected='\n'.join(str(_) for _ in expected_files),
    )


@pytest.helpers.register
def compare_strings(*, expected='', actual=''):
    actual = uqbar.strings.normalize(ansi_escape.sub('', actual))
    expected = uqbar.strings.normalize(ansi_escape.sub('', expected))
    example = types.SimpleNamespace()
    example.want = expected
    output_checker = doctest.OutputChecker()
    flags = (
        doctest.NORMALIZE_WHITESPACE |
        doctest.ELLIPSIS |
        doctest.REPORT_NDIFF
    )
    success = output_checker.check_output(expected, actual, flags)
    if not success:
        diff = output_checker.output_difference(example, actual, flags)
        raise Exception(diff)


@pytest.helpers.register
def create_build_target(
    test_directory_path,
    force=False,
    expect_error=False,
):
    script = abjad.cli.ManageBuildTargetScript()
    command = ['--new']
    if force:
        command.insert(0, '-f')
    score_path = test_directory_path / package_name
    with uqbar.io.DirectoryChange(score_path):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    return score_path / package_name / 'builds' / 'letter-portrait'


@pytest.helpers.register
def create_material(
    test_directory_path,
    material_name='test_material',
    force=False,
    expect_error=False,
):
    script = abjad.cli.ManageMaterialScript()
    command = ['--new', material_name]
    if force:
        command.insert(0, '-f')
    score_path = test_directory_path / package_name
    with uqbar.io.DirectoryChange(score_path):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    return score_path / package_name / 'materials' / material_name


@pytest.helpers.register
def create_score(test_directory_path, force=False, expect_error=False):
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
    with uqbar.io.DirectoryChange(test_directory_path):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')


@pytest.helpers.register
def create_segment(
    test_directory_path,
    segment_name='test_segment',
    force=False,
    expect_error=False,
):
    script = abjad.cli.ManageSegmentScript()
    command = ['--new', segment_name]
    if force:
        command.insert(0, '-f')
    score_path = test_directory_path / package_name
    with uqbar.io.DirectoryChange(score_path):
        if expect_error:
            with pytest.raises(SystemExit) as exception_info:
                script(command)
            assert exception_info.value.code == 1
        else:
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
    return score_path / package_name / 'segments' / segment_name


@pytest.helpers.register
def get_fancy_parts_code():
    return uqbar.strings.normalize(r"""
        \book {
            \bookOutputSuffix "cello"
            \score {
                \keepWithTag #'(time cello)
                \include "../segments.ily"
            }
        }
        \book {
            \bookOutputSuffix "viola"
            \score {
                \keepWithTag #'(viola)
                \include "../segments.ily"
            }
        }
        \book {
            \bookOutputSuffix "violin-i"
            \score {
                \keepWithTag #'(first-violin)
                \include "../segments.ily"
            }
        }
        \book {
            \bookOutputSuffix "violin-ii"
            \score {
                \keepWithTag #'(second-violin)
                \include "../segments.ily"
            }
        }
        """)


@pytest.helpers.register
def get_fancy_segment_maker_code():
    return uqbar.strings.normalize(r"""
        import abjad

        class SegmentMaker(abjad.AbjadObject):

            ### INITIALIZER ###

            def __init__(self, measure_count=1):
                measure_count = int(measure_count)
                assert 0 < measure_count
                self.measure_count = measure_count
                self.score_template = abjad.StringQuartetScoreTemplate()

            ### PUBLIC METHODS ###

            def run(
                self,
                metadata=None,
                previous_metadata=None,
                ):
                self.metadata = metadata
                score = self.score_template()
                for i in range(self.measure_count):
                    for voice in abjad.iterate(score).components(abjad.Voice):
                        measure = abjad.Measure((4, 4), "c'1")
                        voice.append(measure)
                self.score_template.attach_defaults(score)
                lilypond_file = abjad.LilyPondFile.new(
                    score,
                    includes=['../../stylesheets/stylesheet.ily'],
                    )
                first_bar_number = metadata.get('first_bar_number', 1)
                if 1 < first_bar_number:
                    abjad.setting(score).current_bar_number = first_bar_number
                segment_number = metadata.get('segment_number', 1)
                segment_count = metadata.get('segment_count', 1)
                if 1 < segment_number:
                    rehearsal_mark = abjad.RehearsalMark()
                    for voice in abjad.iterate(score).components(abjad.Voice):
                        for leaf in abjad.iterate(voice).leaves():
                            abjad.attach(rehearsal_mark, leaf)
                            break
                if segment_count <= segment_number:
                    score.add_final_bar_line(
                        abbreviation='|.',
                        to_each_voice=True,
                        )
                metadata['measure_count'] = self.measure_count
                return lilypond_file
        """)


@pytest.helpers.register
def illustrate_material(test_directory_path, material_name):
    script = abjad.cli.ManageMaterialScript()
    command = ['--illustrate', material_name]
    score_path = test_directory_path / package_name
    with uqbar.io.DirectoryChange(score_path):
        try:
            script(command)
        except SystemExit as e:
            raise RuntimeError('SystemExit: {}'.format(e.code))


@pytest.helpers.register
def illustrate_segment(test_directory_path, segment_name):
    script = abjad.cli.ManageSegmentScript()
    command = ['--illustrate', segment_name]
    score_path = test_directory_path / package_name
    with uqbar.io.DirectoryChange(score_path):
        try:
            script(command)
        except SystemExit as e:
            raise RuntimeError('SystemExit: {}'.format(e.code))


@pytest.helpers.register
def illustrate_segments(test_directory_path):
    script = abjad.cli.ManageSegmentScript()
    command = ['--illustrate', '*']
    score_path = test_directory_path / package_name
    with uqbar.io.DirectoryChange(score_path):
        script(command)


@pytest.helpers.register
def install_fancy_segment_maker(test_directory_path):
    score_path = test_directory_path / package_name / package_name
    tools_path = score_path / 'tools'
    segment_maker_path = tools_path / 'SegmentMaker.py'
    with segment_maker_path.open('w') as file_pointer:
        file_pointer.write(pytest.helpers.get_fancy_segment_maker_code())
    build_path = score_path / 'builds'
    parts_path = build_path / 'parts.ily'
    with parts_path.open('w') as file_pointer:
        file_pointer.write(pytest.helpers.get_fancy_parts_code())
