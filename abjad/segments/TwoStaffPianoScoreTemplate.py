from abjad.utilities.OrderedDict import OrderedDict
from .ScoreTemplate import ScoreTemplate


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    """
    Two-staff piano score template.

    ..  container:: example

        >>> template = abjad.TwoStaffPianoScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score])
        \context Score = "TwoStaffPianoScore"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalRests = "GlobalRests"
                {
                }
                \context GlobalSkips = "GlobalSkips"
                {
                }
            >>
            \context PianoStaff = "PianoStaff"
            <<
                \context Staff = "RHStaff"
                {
                    \context Voice = "RHVoice"
                    {
                        s1
                    }
                }
                \context Staff = "LHStaff"
                {
                    \context Voice = "LHVoice"
                    {
                        \clef "bass" %! ST3
                        s1
                    }
                }
            >>
        >>

    Returns score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        super().__init__()
        self.voice_abbreviations.update({
            'rh': 'RHVoice',
            'lh': 'LHVoice',
            })

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls two-staff piano score template.

        Returns score.
        """
        import abjad
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # RH STAFF
        rh_voice = abjad.Voice(name='RHVoice')
        rh_staff = abjad.Staff(
            [rh_voice],
            name='RHStaff',
            )

        # LH STAFF
        lh_voice = abjad.Voice(name='LHVoice')
        lh_staff = abjad.Staff(
            [lh_voice],
            name='LHStaff',
            )
        abjad.annotate(
            lh_staff,
            'default_clef',
            abjad.Clef('bass'),
            )

        # PIANO STAFF
        staff_group = abjad.StaffGroup(
            [rh_staff, lh_staff],
            lilypond_type='PianoStaff',
            name='PianoStaff',
            )
        abjad.annotate(
            staff_group,
            'default_instrument',
            abjad.Piano(),
            )

        # SCORE
        score = abjad.Score(
            [global_context, staff_group],
            name='TwoStaffPianoScore',
            )
        return score
