import json
import pytest
from base import ScorePackageScriptTestCase
from unittest import mock


class Test(ScorePackageScriptTestCase):

    @mock.patch('abjad.IOManager.open_file')
    def test_1(self, open_file_mock):
        pytest.helpers.create_score(self.test_directory_path)
        self.install_fancy_segment_maker()
        path_1 = self.create_segment('segment_one')
        path_2 = self.create_segment('segment_two')
        path_3 = self.create_segment('segment_three')
        self.illustrate_segments()
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

    @mock.patch('abjad.IOManager.open_file')
    def test_2(self, open_file_mock):
        pytest.helpers.create_score(self.test_directory_path)
        self.install_fancy_segment_maker()
        segment_path = self.create_segment('test_segment')
        self.illustrate_segment('test_segment')
        illustration_path = segment_path.joinpath('illustration.ly')
        self.compare_lilypond_contents(
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
            '''
            )
