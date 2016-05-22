# -*- coding: utf-8 -*-
import collections
from abjad.tools import indicatortools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import attach


class StringQuartetScoreTemplate(AbjadObject):
    '''String quartet score template.

    ::

        >>> template = templatetools.StringQuartetScoreTemplate()
        >>> score = template()

    ::

        >>> score
        <Score-"String Quartet Score"<<1>>>

    ..  doctest::

        >>> print(format(score))
        \context Score = "String Quartet Score" <<
            \context StaffGroup = "String Quartet Staff Group" <<
                \tag #'first-violin
                \context Staff = "First Violin Staff" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "First Violin Voice" {
                    }
                }
                \tag #'second-violin
                \context Staff = "Second Violin Staff" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin }
                    \set Staff.shortInstrumentName = \markup { Vn. }
                    \context Voice = "Second Violin Voice" {
                    }
                }
                \tag #'viola
                \context Staff = "Viola Staff" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola }
                    \set Staff.shortInstrumentName = \markup { Va. }
                    \context Voice = "Viola Voice" {
                    }
                }
                \tag #'cello
                \context Staff = "Cello Staff" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello }
                    \set Staff.shortInstrumentName = \markup { Vc. }
                    \context Voice = "Cello Voice" {
                    }
                }
            >>
        >>

    Returns score template.
    '''

    ### CLASS VARIABLES ###

    context_name_abbreviations = collections.OrderedDict({
        'vn1': 'First Violin Voice',
        'vn2': 'Second Violin Voice',
        'va': 'Viola Voice',
        'vc': 'Cello Voice',
        })

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls string quartet score template.

        Returns score.
        '''

        # make first violin voice and staff
        first_violin_voice = scoretools.Voice(name='First Violin Voice')
        first_violin_staff = scoretools.Staff(
            [first_violin_voice], name='First Violin Staff')
        clef = indicatortools.Clef('treble')
        attach(clef, first_violin_staff)
        violin = instrumenttools.Violin()
        attach(violin, first_violin_staff)
        tag = indicatortools.LilyPondCommand("tag #'first-violin", 'before')
        attach(tag, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = scoretools.Voice(name='Second Violin Voice')
        second_violin_staff = scoretools.Staff(
            [second_violin_voice], name='Second Violin Staff')
        clef = indicatortools.Clef('treble')
        attach(clef, second_violin_staff)
        violin = instrumenttools.Violin()
        attach(violin, second_violin_staff)
        tag = indicatortools.LilyPondCommand("tag #'second-violin", 'before')
        attach(tag, second_violin_staff)

        # make viola voice and staff
        viola_voice = scoretools.Voice(name='Viola Voice')
        viola_staff = scoretools.Staff(
            [viola_voice], name='Viola Staff')
        clef = indicatortools.Clef('alto')
        attach(clef, viola_staff)
        viola = instrumenttools.Viola()
        attach(viola, viola_staff)
        tag = indicatortools.LilyPondCommand("tag #'viola", 'before')
        attach(tag, viola_staff)

        # make cello voice and staff
        cello_voice = scoretools.Voice(name='Cello Voice')
        cello_staff = scoretools.Staff(
            [cello_voice], name='Cello Staff')
        clef = indicatortools.Clef('bass')
        attach(clef, cello_staff)
        cello = instrumenttools.Cello()
        attach(cello, cello_staff)
        tag = indicatortools.LilyPondCommand("tag #'cello", 'before')
        attach(tag, cello_staff)

        # make string quartet staff group
        string_quartet_staff_group = scoretools.StaffGroup([
            first_violin_staff,
            second_violin_staff,
            viola_staff,
            cello_staff,
            ],
            name='String Quartet Staff Group',
            )

        # make string quartet score
        string_quartet_score = scoretools.Score(
            [string_quartet_staff_group],
            name='String Quartet Score',
            )

        # return string quartet score
        return string_quartet_score
