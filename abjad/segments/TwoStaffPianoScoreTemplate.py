from abjad.utilities.OrderedDict import OrderedDict
from .ScoreTemplate import ScoreTemplate


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    """
    Two-staff piano score template.

    ..  container:: example

        >>> template = abjad.TwoStaffPianoScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=60)
        \context Score = "TwoStaffPianoScore"                       %! TwoStaffPianoScoreTemplate
        <<                                                          %! TwoStaffPianoScoreTemplate
            \context GlobalContext = "GlobalContext"                %! _make_global_context
            <<                                                      %! _make_global_context
                \context GlobalRests = "GlobalRests"                %! _make_global_context
                {                                                   %! _make_global_context
                }                                                   %! _make_global_context
                \context GlobalSkips = "GlobalSkips"                %! _make_global_context
                {                                                   %! _make_global_context
                }                                                   %! _make_global_context
            >>                                                      %! _make_global_context
            \context PianoStaff = "PianoStaff"                      %! TwoStaffPianoScoreTemplate
            <<                                                      %! TwoStaffPianoScoreTemplate
                \context Staff = "RHStaff"                          %! TwoStaffPianoScoreTemplate
                {                                                   %! TwoStaffPianoScoreTemplate
                    \context Voice = "RHVoice"                      %! TwoStaffPianoScoreTemplate
                    {                                               %! TwoStaffPianoScoreTemplate
                        s1                                          %! ScoreTemplate.__illustrate__
                    }                                               %! TwoStaffPianoScoreTemplate
                }                                                   %! TwoStaffPianoScoreTemplate
                \context Staff = "LHStaff"                          %! TwoStaffPianoScoreTemplate
                {                                                   %! TwoStaffPianoScoreTemplate
                    \context Voice = "LHVoice"                      %! TwoStaffPianoScoreTemplate
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
            name='RHVoice',
            tag=tag,
            )
        rh_staff = abjad.Staff(
            [rh_voice],
            name='RHStaff',
            tag=tag,
            )

        # LH STAFF
        lh_voice = abjad.Voice(
            name='LHVoice',
            tag=tag,
            )
        lh_staff = abjad.Staff(
            [lh_voice],
            name='LHStaff',
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
            name='PianoStaff',
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
            name='TwoStaffPianoScore',
            tag=tag,
            )
        return score
