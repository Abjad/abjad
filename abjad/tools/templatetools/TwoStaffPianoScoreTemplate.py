import collections
from abjad.tools.templatetools.ScoreTemplate import ScoreTemplate


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    '''Two-staff piano score template.

    ..  container:: example

        ::

            >>> template = abjad.templatetools.TwoStaffPianoScoreTemplate()
            >>> show(template) # doctest: +SKIP

        ::

            >>> f(template.__illustrate__()[abjad.Score])
            \context Score = "Two-Staff Piano Score" <<
                \context PianoStaff = "Piano Staff" <<
                    \context Staff = "RH Staff" {
                        \context Voice = "RH Voice" {
                            \set PianoStaff.instrumentName = \markup { Piano }
                            \set PianoStaff.shortInstrumentName = \markup { Pf. }
                            \clef "treble"
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

    __slots__ = ()

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
            [],
            name='RH Voice',
            )
        rh_staff = abjad.Staff(
            [rh_voice],
            name='RH Staff',
            )
        clef = abjad.Clef('treble')
        #abjad.attach(clef, rh_staff)
        abjad.annotate(rh_staff, 'default_clef', clef)

        # make LH voice and staff
        lh_voice = abjad.Voice(
            [],
            name='LH Voice',
            )
        lh_staff = abjad.Staff(
            [lh_voice],
            name='LH Staff',
            )
        clef = abjad.Clef('bass')
        #abjad.attach(clef, lh_staff)
        abjad.annotate(lh_staff, 'default_clef', clef)

        # make piano staff
        staff_group = abjad.StaffGroup(
            [rh_staff, lh_staff],
            context_name='PianoStaff',
            name='Piano Staff',
            )
        piano = abjad.instrumenttools.Piano()
        #abjad.attach(piano, staff_group)
        abjad.annotate(staff_group, 'default_instrument', piano)

        # make two-staf piano score
        two_staff_piano_score = abjad.Score(
            [staff_group],
            name='Two-Staff Piano Score',
            )

        # return two-staff piano score
        return two_staff_piano_score
