# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StringQuartetScoreTemplate(AbjadValueObject):
    '''String quartet score template.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> template = abjad.templatetools.StringQuartetScoreTemplate()
            >>> score = template()
            >>> show(score) # doctest: +SKIP

        ..  docs::

            >>> f(score)
            \context Score = "String Quartet Score" <<
                \context StaffGroup = "String Quartet Staff Group" <<
                    \tag #'first-violin
                    \context Staff = "First Violin Staff" {
                        \set Staff.instrumentName = \markup { Violin }
                        \set Staff.shortInstrumentName = \markup { Vn. }
                        \clef "treble"
                        \context Voice = "First Violin Voice" {
                        }
                    }
                    \tag #'second-violin
                    \context Staff = "Second Violin Staff" {
                        \set Staff.instrumentName = \markup { Violin }
                        \set Staff.shortInstrumentName = \markup { Vn. }
                        \clef "treble"
                        \context Voice = "Second Violin Voice" {
                        }
                    }
                    \tag #'viola
                    \context Staff = "Viola Staff" {
                        \set Staff.instrumentName = \markup { Viola }
                        \set Staff.shortInstrumentName = \markup { Va. }
                        \clef "alto"
                        \context Voice = "Viola Voice" {
                        }
                    }
                    \tag #'cello
                    \context Staff = "Cello Staff" {
                        \set Staff.instrumentName = \markup { Cello }
                        \set Staff.shortInstrumentName = \markup { Vc. }
                        \clef "bass"
                        \context Voice = "Cello Voice" {
                        }
                    }
                >>
            >>

    Returns score template.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

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
        import abjad

        # make first violin voice and staff
        first_violin_voice = abjad.Voice(
            [],
            name='First Violin Voice',
            )
        first_violin_staff = abjad.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )
        clef = abjad.Clef('treble')
        abjad.attach(clef, first_violin_staff)
        violin = abjad.instrumenttools.Violin()
        abjad.attach(violin, first_violin_staff)
        tag = abjad.LilyPondCommand("tag #'first-violin", 'before')
        abjad.attach(tag, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = abjad.Voice(
            [],
            name='Second Violin Voice',
            )
        second_violin_staff = abjad.Staff(
            [second_violin_voice],
            name='Second Violin Staff',
            )
        clef = abjad.Clef('treble')
        abjad.attach(clef, second_violin_staff)
        violin = abjad.instrumenttools.Violin()
        abjad.attach(violin, second_violin_staff)
        tag = abjad.LilyPondCommand("tag #'second-violin", 'before')
        abjad.attach(tag, second_violin_staff)

        # make viola voice and staff
        viola_voice = abjad.Voice(
            [],
            name='Viola Voice',
            )
        viola_staff = abjad.Staff(
            [viola_voice],
            name='Viola Staff',
            )
        clef = abjad.Clef('alto')
        abjad.attach(clef, viola_staff)
        viola = abjad.instrumenttools.Viola()
        abjad.attach(viola, viola_staff)
        tag = abjad.LilyPondCommand("tag #'viola", 'before')
        abjad.attach(tag, viola_staff)

        # make cello voice and staff
        cello_voice = abjad.Voice(
            [],
            name='Cello Voice',
            )
        cello_staff = abjad.Staff(
            [cello_voice],
            name='Cello Staff',
            )
        clef = abjad.Clef('bass')
        abjad.attach(clef, cello_staff)
        cello = abjad.instrumenttools.Cello()
        abjad.attach(cello, cello_staff)
        tag = abjad.LilyPondCommand("tag #'cello", 'before')
        abjad.attach(tag, cello_staff)

        # make string quartet staff group
        string_quartet_staff_group = abjad.StaffGroup([
            first_violin_staff,
            second_violin_staff,
            viola_staff,
            cello_staff,
            ],
            name='String Quartet Staff Group',
            )

        # make string quartet score
        string_quartet_score = abjad.Score(
            [string_quartet_staff_group],
            name='String Quartet Score',
            )

        # return string quartet score
        return string_quartet_score
