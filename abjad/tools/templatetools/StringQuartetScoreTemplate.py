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
                        \context Voice = "First Violin Voice" {
                            \clef "treble"
                            \set Staff.instrumentName = \markup { Violin }
                            \set Staff.shortInstrumentName = \markup { Vn. }
                            s1
                        }
                    }
                    \tag #'second-violin
                    \context Staff = "Second Violin Staff" {
                        \context Voice = "Second Violin Voice" {
                            \clef "treble"
                            \set Staff.instrumentName = \markup { Violin }
                            \set Staff.shortInstrumentName = \markup { Vn. }
                            s1
                        }
                    }
                    \tag #'viola
                    \context Staff = "Viola Staff" {
                        \context Voice = "Viola Voice" {
                            \clef "alto"
                            \set Staff.instrumentName = \markup { Viola }
                            \set Staff.shortInstrumentName = \markup { Va. }
                            s1
                        }
                    }
                    \tag #'cello
                    \context Staff = "Cello Staff" {
                        \context Voice = "Cello Voice" {
                            \clef "bass"
                            \set Staff.instrumentName = \markup { Cello }
                            \set Staff.shortInstrumentName = \markup { Vc. }
                            s1
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
            [abjad.Skip('s1')],
            name='First Violin Voice',
            )
        first_violin_staff = abjad.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )
        leaf = abjad.inspect(first_violin_staff).get_leaf(0)
        clef = abjad.Clef('treble')
        abjad.attach(clef, leaf)
        violin = abjad.instrumenttools.Violin()
        abjad.attach(violin, leaf)
        tag = abjad.LilyPondCommand("tag #'first-violin", 'before')
        abjad.attach(tag, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = abjad.Voice(
            [abjad.Skip('s1')],
            name='Second Violin Voice',
            )
        second_violin_staff = abjad.Staff(
            [second_violin_voice],
            name='Second Violin Staff',
            )
        leaf = abjad.inspect(second_violin_staff).get_leaf(0)
        clef = abjad.Clef('treble')
        abjad.attach(clef, leaf)
        violin = abjad.instrumenttools.Violin()
        abjad.attach(violin, leaf)
        tag = abjad.LilyPondCommand("tag #'second-violin", 'before')
        abjad.attach(tag, second_violin_staff)

        # make viola voice and staff
        viola_voice = abjad.Voice(
            [abjad.Skip('s1')],
            name='Viola Voice',
            )
        viola_staff = abjad.Staff(
            [viola_voice],
            name='Viola Staff',
            )
        leaf = abjad.inspect(viola_staff).get_leaf(0)
        clef = abjad.Clef('alto')
        abjad.attach(clef, leaf)
        viola = abjad.instrumenttools.Viola()
        abjad.attach(viola, leaf)
        tag = abjad.LilyPondCommand("tag #'viola", 'before')
        abjad.attach(tag, viola_staff)

        # make cello voice and staff
        cello_voice = abjad.Voice(
            [abjad.Skip('s1')],
            name='Cello Voice',
            )
        cello_staff = abjad.Staff(
            [cello_voice],
            name='Cello Staff',
            )
        leaf = abjad.inspect(cello_staff).get_leaf(0)
        clef = abjad.Clef('bass')
        abjad.attach(clef, leaf)
        cello = abjad.instrumenttools.Cello()
        abjad.attach(cello, leaf)
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
