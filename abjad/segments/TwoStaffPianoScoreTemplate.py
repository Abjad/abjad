from abjad.core.Score import Score
from abjad.core.Staff import Staff
from abjad.core.StaffGroup import StaffGroup
from abjad.core.Voice import Voice
from abjad.indicators.Clef import Clef
from abjad.instruments import Piano
from abjad.system.Tag import Tag
from abjad.top.annotate import annotate

from .ScoreTemplate import ScoreTemplate


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    r"""
    Two-staff piano score template.

    ..  container:: example

        >>> template = abjad.TwoStaffPianoScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=60)
        \context Score = "Two_Staff_Piano_Score"                    %! abjad.TwoStaffPianoScoreTemplate.__call__()
        <<                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__()
            \context GlobalContext = "Global_Context"               %! abjad.ScoreTemplate._make_global_context()
            <<                                                      %! abjad.ScoreTemplate._make_global_context()
                \context GlobalRests = "Global_Rests"               %! abjad.ScoreTemplate._make_global_context()
                {                                                   %! abjad.ScoreTemplate._make_global_context()
                }                                                   %! abjad.ScoreTemplate._make_global_context()
                \context GlobalSkips = "Global_Skips"               %! abjad.ScoreTemplate._make_global_context()
                {                                                   %! abjad.ScoreTemplate._make_global_context()
                }                                                   %! abjad.ScoreTemplate._make_global_context()
            >>                                                      %! abjad.ScoreTemplate._make_global_context()
            \context PianoStaff = "Piano_Staff"                     %! abjad.TwoStaffPianoScoreTemplate.__call__()
            <<                                                      %! abjad.TwoStaffPianoScoreTemplate.__call__()
                \context Staff = "RH_Staff"                         %! abjad.TwoStaffPianoScoreTemplate.__call__()
                {                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
                    \context Voice = "RH_Voice"                     %! abjad.TwoStaffPianoScoreTemplate.__call__()
                    {                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        s1                                          %! abjad.ScoreTemplate.__illustrate__()
                    }                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                }                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
                \context Staff = "LH_Staff"                         %! abjad.TwoStaffPianoScoreTemplate.__call__()
                {                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
                    \context Voice = "LH_Voice"                     %! abjad.TwoStaffPianoScoreTemplate.__call__()
                    {                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        \clef "bass"                                %! abjad.ScoreTemplate.attach_defaults(3)
                        s1                                          %! abjad.ScoreTemplate.__illustrate__()
                    }                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                }                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
            >>                                                      %! abjad.TwoStaffPianoScoreTemplate.__call__()
        >>                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__()

    Returns score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        super().__init__()
        self.voice_abbreviations.update({"rh": "RHVoice", "lh": "LHVoice"})

    ### SPECIAL METHODS ###

    def __call__(self) -> Score:
        r"""
        Calls two-staff piano score template.

        ..  container:: example

            REGRESSION. Attaches piano to piano group (rather than just staff):

            >>> template = abjad.TwoStaffPianoScoreTemplate()
            >>> score = template()
            >>> piano_staff = score['Piano_Staff']
            >>> rh_voice = score['RH_Voice']
            >>> lh_voice = score['LH_Voice']

            >>> rh_voice.append("g'4")
            >>> lh_voice.append("c4")
            >>> wrappers = template.attach_defaults(score)

            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score, strict=60)
                \context Score = "Two_Staff_Piano_Score"                    %! abjad.TwoStaffPianoScoreTemplate.__call__()
                <<                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__()
                    \context GlobalContext = "Global_Context"               %! abjad.ScoreTemplate._make_global_context()
                    <<                                                      %! abjad.ScoreTemplate._make_global_context()
                        \context GlobalRests = "Global_Rests"               %! abjad.ScoreTemplate._make_global_context()
                        {                                                   %! abjad.ScoreTemplate._make_global_context()
                        }                                                   %! abjad.ScoreTemplate._make_global_context()
                        \context GlobalSkips = "Global_Skips"               %! abjad.ScoreTemplate._make_global_context()
                        {                                                   %! abjad.ScoreTemplate._make_global_context()
                        }                                                   %! abjad.ScoreTemplate._make_global_context()
                    >>                                                      %! abjad.ScoreTemplate._make_global_context()
                    \context PianoStaff = "Piano_Staff"                     %! abjad.TwoStaffPianoScoreTemplate.__call__()
                    <<                                                      %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        \context Staff = "RH_Staff"                         %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        {                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
                            \context Voice = "RH_Voice"                     %! abjad.TwoStaffPianoScoreTemplate.__call__()
                            {                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                                g'4
                            }                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        }                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        \context Staff = "LH_Staff"                         %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        {                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
                            \context Voice = "LH_Voice"                     %! abjad.TwoStaffPianoScoreTemplate.__call__()
                            {                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                                \clef "bass"                                %! abjad.ScoreTemplate.attach_defaults(3)
                                c4
                            }                                               %! abjad.TwoStaffPianoScoreTemplate.__call__()
                        }                                                   %! abjad.TwoStaffPianoScoreTemplate.__call__()
                    >>                                                      %! abjad.TwoStaffPianoScoreTemplate.__call__()
                >>                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__()

            >>> wrapper = abjad.inspect(rh_voice[0]).wrapper(abjad.Instrument)
            >>> wrapper.context
            'PianoStaff'

        """
        site = "abjad.TwoStaffPianoScoreTemplate.__call__()"
        tag = Tag(site)
        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # RH STAFF
        rh_voice = Voice(name="RH_Voice", tag=tag)
        rh_staff = Staff([rh_voice], name="RH_Staff", tag=tag)

        # LH STAFF
        lh_voice = Voice(name="LH_Voice", tag=tag)
        lh_staff = Staff([lh_voice], name="LH_Staff", tag=tag)
        annotate(lh_staff, "default_clef", Clef("bass"))

        # PIANO STAFF
        staff_group = StaffGroup(
            [rh_staff, lh_staff],
            lilypond_type="PianoStaff",
            name="Piano_Staff",
            tag=tag,
        )
        annotate(staff_group, "default_instrument", Piano())

        # SCORE
        score = Score(
            [global_context, staff_group], name="Two_Staff_Piano_Score", tag=tag,
        )
        return score
