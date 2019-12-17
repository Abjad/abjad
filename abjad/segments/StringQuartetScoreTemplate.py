from abjad.system.Tag import Tag

from .Part import Part
from .PartManifest import PartManifest
from .ScoreTemplate import ScoreTemplate


class StringQuartetScoreTemplate(ScoreTemplate):
    r"""
    String quartet score template.

    ..  container:: example

        >>> template = abjad.StringQuartetScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=60)
        \context Score = "String_Quartet_Score"                     %! abjad.StringQuartetScoreTemplate.__call__()
        <<                                                          %! abjad.StringQuartetScoreTemplate.__call__()
            \context StaffGroup = "String_Quartet_Staff_Group"      %! abjad.StringQuartetScoreTemplate.__call__()
            <<                                                      %! abjad.StringQuartetScoreTemplate.__call__()
                \tag #'first-violin
                \context Staff = "First_Violin_Staff"               %! abjad.StringQuartetScoreTemplate.__call__()
                {                                                   %! abjad.StringQuartetScoreTemplate.__call__()
                    \context Voice = "First_Violin_Voice"           %! abjad.StringQuartetScoreTemplate.__call__()
                    {                                               %! abjad.StringQuartetScoreTemplate.__call__()
                        \clef "treble"                              %! abjad.ScoreTemplate.attach_defaults(3)
                        s1                                          %! abjad.ScoreTemplate.__illustrate__()
                    }                                               %! abjad.StringQuartetScoreTemplate.__call__()
                }                                                   %! abjad.StringQuartetScoreTemplate.__call__()
                \tag #'second-violin
                \context Staff = "Second_Violin_Staff"              %! abjad.StringQuartetScoreTemplate.__call__()
                {                                                   %! abjad.StringQuartetScoreTemplate.__call__()
                    \context Voice = "Second_Violin_Voice"          %! abjad.StringQuartetScoreTemplate.__call__()
                    {                                               %! abjad.StringQuartetScoreTemplate.__call__()
                        \clef "treble"                              %! abjad.ScoreTemplate.attach_defaults(3)
                        s1                                          %! abjad.ScoreTemplate.__illustrate__()
                    }                                               %! abjad.StringQuartetScoreTemplate.__call__()
                }                                                   %! abjad.StringQuartetScoreTemplate.__call__()
                \tag #'viola
                \context Staff = "Viola_Staff"                      %! abjad.StringQuartetScoreTemplate.__call__()
                {                                                   %! abjad.StringQuartetScoreTemplate.__call__()
                    \context Voice = "Viola_Voice"                  %! abjad.StringQuartetScoreTemplate.__call__()
                    {                                               %! abjad.StringQuartetScoreTemplate.__call__()
                        \clef "alto"                                %! abjad.ScoreTemplate.attach_defaults(3)
                        s1                                          %! abjad.ScoreTemplate.__illustrate__()
                    }                                               %! abjad.StringQuartetScoreTemplate.__call__()
                }                                                   %! abjad.StringQuartetScoreTemplate.__call__()
                \tag #'cello
                \context Staff = "Cello_Staff"                      %! abjad.StringQuartetScoreTemplate.__call__()
                {                                                   %! abjad.StringQuartetScoreTemplate.__call__()
                    \context Voice = "Cello_Voice"                  %! abjad.StringQuartetScoreTemplate.__call__()
                    {                                               %! abjad.StringQuartetScoreTemplate.__call__()
                        \clef "bass"                                %! abjad.ScoreTemplate.attach_defaults(3)
                        s1                                          %! abjad.ScoreTemplate.__illustrate__()
                    }                                               %! abjad.StringQuartetScoreTemplate.__call__()
                }                                                   %! abjad.StringQuartetScoreTemplate.__call__()
            >>                                                      %! abjad.StringQuartetScoreTemplate.__call__()
        >>                                                          %! abjad.StringQuartetScoreTemplate.__call__()

    Returns score template.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _part_manifest = PartManifest(
        Part(section="FirstViolin", section_abbreviation="VN-1"),
        Part(section="SecondViolin", section_abbreviation="VN-2"),
        Part(section="Viola", section_abbreviation="VA"),
        Part(section="Cello", section_abbreviation="VC"),
    )

    ### INITIALIZER ###

    def __init__(self):
        super().__init__()
        self.voice_abbreviations.update(
            {
                "vn1": "First Violin Voice",
                "vn2": "Second Violin Voice",
                "va": "Viola Voice",
                "vc": "Cello Voice",
            }
        )

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls string quartet score template.

        Returns score.
        """
        import abjad

        site = "abjad.StringQuartetScoreTemplate.__call__()"
        tag = Tag(site)

        # make first violin voice and staff
        first_violin_voice = abjad.Voice([], name="First_Violin_Voice", tag=tag)
        first_violin_staff = abjad.Staff(
            [first_violin_voice], name="First_Violin_Staff", tag=tag
        )
        clef = abjad.Clef("treble")
        abjad.annotate(first_violin_staff, "default_clef", clef)
        violin = abjad.Violin()
        abjad.annotate(first_violin_staff, "default_instrument", violin)
        literal = abjad.LilyPondLiteral(r"\tag #'first-violin", "before")
        abjad.attach(literal, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = abjad.Voice([], name="Second_Violin_Voice", tag=tag)
        second_violin_staff = abjad.Staff(
            [second_violin_voice], name="Second_Violin_Staff", tag=tag
        )
        clef = abjad.Clef("treble")
        abjad.annotate(second_violin_staff, "default_clef", clef)
        violin = abjad.Violin()
        abjad.annotate(second_violin_staff, "default_instrument", violin)
        literal = abjad.LilyPondLiteral(r"\tag #'second-violin", "before")
        abjad.attach(literal, second_violin_staff)

        # make viola voice and staff
        viola_voice = abjad.Voice([], name="Viola_Voice", tag=tag)
        viola_staff = abjad.Staff([viola_voice], name="Viola_Staff", tag=tag)
        clef = abjad.Clef("alto")
        abjad.annotate(viola_staff, "default_clef", clef)
        viola = abjad.Viola()
        abjad.annotate(viola_staff, "default_instrument", viola)
        literal = abjad.LilyPondLiteral(r"\tag #'viola", "before")
        abjad.attach(literal, viola_staff)

        # make cello voice and staff
        cello_voice = abjad.Voice([], name="Cello_Voice", tag=tag)
        cello_staff = abjad.Staff([cello_voice], name="Cello_Staff", tag=tag)
        clef = abjad.Clef("bass")
        abjad.annotate(cello_staff, "default_clef", clef)
        cello = abjad.Cello()
        abjad.annotate(cello_staff, "default_instrument", cello)
        literal = abjad.LilyPondLiteral(r"\tag #'cello", "before")
        abjad.attach(literal, cello_staff)

        # make string quartet staff group
        string_quartet_staff_group = abjad.StaffGroup(
            [first_violin_staff, second_violin_staff, viola_staff, cello_staff],
            name="String_Quartet_Staff_Group",
            tag=tag,
        )

        # make string quartet score
        string_quartet_score = abjad.Score(
            [string_quartet_staff_group], name="String_Quartet_Score", tag=tag,
        )

        # return string quartet score
        return string_quartet_score
