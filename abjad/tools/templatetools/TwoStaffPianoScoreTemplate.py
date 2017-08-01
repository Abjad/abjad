# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class TwoStaffPianoScoreTemplate(AbjadValueObject):
    '''Two-staff piano score template.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> template = abjad.templatetools.TwoStaffPianoScoreTemplate()
            >>> score = template()
            >>> show(score) # doctest: +SKIP

        ::

            >>> f(score)
            \context Score = "Two-Staff Piano Score" <<
                \context PianoStaff = "Piano Staff" <<
                    \context Staff = "RH Staff" {
                        \context Voice = "RH Voice" {
                            \clef "treble"
                            \set PianoStaff.instrumentName = \markup { Piano }
                            \set PianoStaff.shortInstrumentName = \markup { Pf. }
                            s1
                        }
                    }
                    \context Staff = "LH Staff" {
                        \context Voice = "LH Voice" {
                            \clef "bass"
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
        'rh': 'RH Voice',
        'lh': 'LH Voice',
        })

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls two-staff piano score template.

        Returns score.
        '''
        import abjad

        # make RH voice and staff
        rh_voice = abjad.Voice(
            [abjad.Skip('s1')],
            name='RH Voice',
            )
        rh_staff = abjad.Staff(
            [rh_voice],
            name='RH Staff',
            )
        clef = abjad.Clef('treble')
        leaf = abjad.inspect(rh_staff).get_leaf(0)
        abjad.attach(clef, leaf)

        # make LH voice and staff
        lh_voice = abjad.Voice(
            [abjad.Skip('s1')],
            name='LH Voice',
            )
        lh_staff = abjad.Staff(
            [lh_voice],
            name='LH Staff',
            )
        clef = abjad.Clef('bass')
        leaf = abjad.inspect(lh_staff).get_leaf(0)
        abjad.attach(clef, leaf)

        # make piano staff
        staff_group = abjad.StaffGroup(
            [rh_staff, lh_staff],
            context_name='PianoStaff',
            name='Piano Staff',
            )
        piano = abjad.instrumenttools.Piano()
        leaf = abjad.inspect(staff_group).get_leaf(0)
        abjad.attach(piano, leaf)

        # make two-staf piano score
        two_staff_piano_score = abjad.Score(
            [staff_group],
            name='Two-Staff Piano Score',
            )

        # return two-staff piano score
        return two_staff_piano_score
