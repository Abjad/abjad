import pathlib
import pytest
import shutil
import sys
import types
from uqbar.strings import normalize


pytest_plugins = ['helpers_namespace']


package_name = 'test_score'


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


@pytest.helpers.register
def get_fancy_parts_code():
    return normalize(r"""
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
    return normalize(r"""
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
