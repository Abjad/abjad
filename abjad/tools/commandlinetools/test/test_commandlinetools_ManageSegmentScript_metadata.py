# -*- coding: utf-8 -*-
import json
from base import ScorePackageScriptTestCase
try:
    from unittest import mock
except ImportError:
    import mock


class Test(ScorePackageScriptTestCase):

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_1(self, open_file_mock):
        self.create_score()
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

    @mock.patch('abjad.systemtools.IOManager.open_file')
    def test_2(self, open_file_mock):
        self.create_score()
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
            \header {}
            <BLANKLINE>
            \layout {}
            <BLANKLINE>
            \paper {}
            <BLANKLINE>
            \score {
                \context Score = "String Quartet Score" <<
                    \context StaffGroup = "String Quartet Staff Group" <<
                        \tag #'first-violin
                        \context Staff = "First Violin Staff" {
                            \clef "treble"
                            \set Staff.instrumentName = \markup { Violin }
                            \set Staff.shortInstrumentName = \markup { Vn. }
                            \context Voice = "First Violin Voice" {
                                {
                                    \time 4/4
                                    c'1
                                    \bar "|."
                                }
                            }
                        }
                        \tag #'second-violin
                        \context Staff = "Second Violin Staff" {
                            \clef "treble"
                            \set Staff.instrumentName = \markup { Violin }
                            \set Staff.shortInstrumentName = \markup { Vn. }
                            \context Voice = "Second Violin Voice" {
                                {
                                    \time 4/4
                                    c'1
                                    \bar "|."
                                }
                            }
                        }
                        \tag #'viola
                        \context Staff = "Viola Staff" {
                            \clef "alto"
                            \set Staff.instrumentName = \markup { Viola }
                            \set Staff.shortInstrumentName = \markup { Va. }
                            \context Voice = "Viola Voice" {
                                {
                                    \time 4/4
                                    c'1
                                    \bar "|."
                                }
                            }
                        }
                        \tag #'cello
                        \context Staff = "Cello Staff" {
                            \clef "bass"
                            \set Staff.instrumentName = \markup { Cello }
                            \set Staff.shortInstrumentName = \markup { Vc. }
                            \context Voice = "Cello Voice" {
                                {
                                    \time 4/4
                                    c'1
                                    \bar "|."
                                }
                            }
                        }
                    >>
                >>
            }
            '''
            )
