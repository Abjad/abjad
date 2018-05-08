import json
import pytest


def test_1(paths, open_file_mock):
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.install_fancy_segment_maker(paths.test_directory_path)
    path_1 = pytest.helpers.create_segment(
        paths.test_directory_path, 'segment_one')
    path_2 = pytest.helpers.create_segment(
        paths.test_directory_path, 'segment_two')
    path_3 = pytest.helpers.create_segment(
        paths.test_directory_path, 'segment_three')
    pytest.helpers.illustrate_segments(paths.test_directory_path)
    with open(str(path_1.joinpath('metadata.json')), 'r') as file_pointer:
        metadata_1 = json.loads(file_pointer.read())
    with open(str(path_2.joinpath('metadata.json')), 'r') as file_pointer:
        metadata_2 = json.loads(file_pointer.read())
    with open(str(path_3.joinpath('metadata.json')), 'r') as file_pointer:
        metadata_3 = json.loads(file_pointer.read())
    assert metadata_1 == {
        'first_bar_number': 1,
        'measure_count': 1,
        'segment_count': 3,
        'segment_number': 1,
    }
    assert metadata_2 == {
        'first_bar_number': 2,
        'measure_count': 1,
        'segment_count': 3,
        'segment_number': 2,
    }
    assert metadata_3 == {
        'first_bar_number': 3,
        'measure_count': 1,
        'segment_count': 3,
        'segment_number': 3,
    }


def test_2(paths, open_file_mock):
    pytest.helpers.create_score(paths.test_directory_path)
    pytest.helpers.install_fancy_segment_maker(paths.test_directory_path)
    segment_path = pytest.helpers.create_segment(
        paths.test_directory_path, 'test_segment')
    pytest.helpers.illustrate_segment(paths.test_directory_path, 'test_segment')
    illustration_path = segment_path.joinpath('illustration.ly')
    pytest.helpers.compare_lilypond_contents(
        illustration_path,
        r'''
        \language "english"
        <BLANKLINE>
        \include "../../stylesheets/stylesheet.ily"
        <BLANKLINE>
        \header {
            tagline = ##f
        }
        <BLANKLINE>
        \layout {}
        <BLANKLINE>
        \paper {}
        <BLANKLINE>
        \score {
            \context Score = "String Quartet Score"
                <<
                \context StaffGroup = "String Quartet Staff Group"
                <<
                    \tag #'first-violin
                    \context Staff = "First Violin Staff"
                    {
                        \context Voice = "First Violin Voice"
                        {
                            {   % measure
                                \time 4/4
                                \set Staff.instrumentName = \markup { Violin }   %! ST1
                                \set Staff.shortInstrumentName = \markup { Vn. } %! ST1
                                \clef "treble" %! ST3
                                c'1
                                \bar "|." %! SCORE1
                            }   % measure
                        }
                    }
                    \tag #'second-violin
                    \context Staff = "Second Violin Staff"
                    {
                        \context Voice = "Second Violin Voice"
                        {
                            {   % measure
                                \time 4/4
                                \set Staff.instrumentName = \markup { Violin }   %! ST1
                                \set Staff.shortInstrumentName = \markup { Vn. } %! ST1
                                \clef "treble" %! ST3
                                c'1
                                \bar "|." %! SCORE1
                            }   % measure
                        }
                    }
                    \tag #'viola
                    \context Staff = "Viola Staff"
                    {
                        \context Voice = "Viola Voice"
                        {
                            {   % measure
                                \time 4/4
                                \set Staff.instrumentName = \markup { Viola }   %! ST1
                                \set Staff.shortInstrumentName = \markup { Va. } %! ST1
                                \clef "alto" %! ST3
                                c'1
                                \bar "|." %! SCORE1
                            }   % measure
                        }
                    }
                    \tag #'cello
                    \context Staff = "Cello Staff"
                    {
                        \context Voice = "Cello Voice"
                        {
                            {   % measure
                                \time 4/4
                                \set Staff.instrumentName = \markup { Cello }   %! ST1
                                \set Staff.shortInstrumentName = \markup { Vc. } %! ST1
                                \clef "bass" %! ST3
                                c'1
                                \bar "|." %! SCORE1
                            }   % measure
                        }
                    }
                >>
            >>
        }
        ''')
