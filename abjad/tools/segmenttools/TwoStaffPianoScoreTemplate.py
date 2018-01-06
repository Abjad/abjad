import collections
from .ScoreTemplate import ScoreTemplate


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    '''Two-staff piano score template.

    ..  container:: example

        >>> template = abjad.TwoStaffPianoScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score])
        \context Score = "Two-Staff Piano Score" <<
            \context PianoStaff = "Piano Staff" <<
                \context Staff = "RH Staff" {
                    \context Voice = "RH Voice" {
                        \set PianoStaff.instrumentName = \markup { Piano }    %! ST1
                        \set PianoStaff.shortInstrumentName = \markup { Pf. } %! ST1
                        s1
                    }
                }
                \context Staff = "LH Staff" {
                    \context Voice = "LH Voice" {
                        \clef "bass" %! ST3
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
        # RH STAFF
        rh_voice = abjad.Voice(name='RH Voice')
        rh_staff = abjad.Staff(
            [rh_voice],
            name='RH Staff',
            )

        # LH STAFF
        lh_voice = abjad.Voice(name='LH Voice')
        lh_staff = abjad.Staff(
            [lh_voice],
            name='LH Staff',
            )
        abjad.annotate(
            lh_staff,
            'default_clef',
            abjad.Clef('bass'),
            )

        # PIANO STAFF
        staff_group = abjad.StaffGroup(
            [rh_staff, lh_staff],
            context_name='PianoStaff',
            name='Piano Staff',
            )
        abjad.annotate(
            staff_group,
            'default_instrument',
            abjad.Piano(),
            )

        # SCORE
        score = abjad.Score(
            [staff_group],
            name='Two-Staff Piano Score',
            )
        return score
