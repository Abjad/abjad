from abjad.utilities.OrderedDict import OrderedDict
from .ScoreTemplate import ScoreTemplate


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    """
    Two-staff piano score template.

    ..  container:: example

        >>> template = abjad.TwoStaffPianoScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=60)
        \context Score = "Two_Staff_Piano_Score"                    %! TwoStaffPianoScoreTemplate
        <<                                                          %! TwoStaffPianoScoreTemplate
            \context GlobalContext = "Global_Context"               %! _make_global_context
            <<                                                      %! _make_global_context
                \context GlobalRests = "Global_Rests"               %! _make_global_context
                {                                                   %! _make_global_context
                }                                                   %! _make_global_context
                \context GlobalSkips = "Global_Skips"               %! _make_global_context
                {                                                   %! _make_global_context
                }                                                   %! _make_global_context
            >>                                                      %! _make_global_context
            \context PianoStaff = "Piano_Staff"                     %! TwoStaffPianoScoreTemplate
            <<                                                      %! TwoStaffPianoScoreTemplate
                \context Staff = "RH_Staff"                         %! TwoStaffPianoScoreTemplate
                {                                                   %! TwoStaffPianoScoreTemplate
                    \context Voice = "RH_Voice"                     %! TwoStaffPianoScoreTemplate
                    {                                               %! TwoStaffPianoScoreTemplate
                        s1                                          %! ScoreTemplate.__illustrate__
                    }                                               %! TwoStaffPianoScoreTemplate
                }                                                   %! TwoStaffPianoScoreTemplate
                \context Staff = "LH_Staff"                         %! TwoStaffPianoScoreTemplate
                {                                                   %! TwoStaffPianoScoreTemplate
                    \context Voice = "LH_Voice"                     %! TwoStaffPianoScoreTemplate
                    {                                               %! TwoStaffPianoScoreTemplate
                        \clef "bass"                                %! attach_defaults
                        s1                                          %! ScoreTemplate.__illustrate__
                    }                                               %! TwoStaffPianoScoreTemplate
                }                                                   %! TwoStaffPianoScoreTemplate
            >>                                                      %! TwoStaffPianoScoreTemplate
        >>                                                          %! TwoStaffPianoScoreTemplate

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
        tag = 'TwoStaffPianoScoreTemplate'
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # RH STAFF
        rh_voice = abjad.Voice(
            name='RH_Voice',
            tag=tag,
            )
        rh_staff = abjad.Staff(
            [rh_voice],
            name='RH_Staff',
            tag=tag,
            )

        # LH STAFF
        lh_voice = abjad.Voice(
            name='LH_Voice',
            tag=tag,
            )
        lh_staff = abjad.Staff(
            [lh_voice],
            name='LH_Staff',
            tag=tag,
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
            name='Piano_Staff',
            tag=tag,
            )
        abjad.annotate(
            staff_group,
            'default_instrument',
            abjad.Piano(),
            )

        # SCORE
        score = abjad.Score(
            [global_context, staff_group],
            name='Two_Staff_Piano_Score',
            tag=tag,
            )
        return score
