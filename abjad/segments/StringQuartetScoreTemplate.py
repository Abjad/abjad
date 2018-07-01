from abjad.utilities.OrderedDict import OrderedDict
from .Part import Part
from .PartManifest import PartManifest
from .ScoreTemplate import ScoreTemplate


class StringQuartetScoreTemplate(ScoreTemplate):
    r"""
    String quartet score template.

    ..  container:: example

        >>> template = abjad.StringQuartetScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score])
        \context Score = "String Quartet Score"
        <<
            \context StaffGroup = "String Quartet Staff Group"
            <<
                \tag #'first-violin
                \context Staff = "First Violin Staff"
                {
                    \context Voice = "First Violin Voice"
                    {
                        \clef "treble" %! ST3
                        s1
                    }
                }
                \tag #'second-violin
                \context Staff = "Second Violin Staff"
                {
                    \context Voice = "Second Violin Voice"
                    {
                        \clef "treble" %! ST3
                        s1
                    }
                }
                \tag #'viola
                \context Staff = "Viola Staff"
                {
                    \context Voice = "Viola Voice"
                    {
                        \clef "alto" %! ST3
                        s1
                    }
                }
                \tag #'cello
                \context Staff = "Cello Staff"
                {
                    \context Voice = "Cello Voice"
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

    __slots__ = ()


    _part_manifest = PartManifest(
        Part(section='FirstViolin', section_abbreviation='VN-1'),
        Part(section='SecondViolin', section_abbreviation='VN-2'),
        Part(section='Viola', section_abbreviation='VA'),
        Part(section='Cello', section_abbreviation='VC'),
        )

    ### INITIALIZER ###

    def __init__(self):
        super().__init__()
        self.voice_abbreviations.update({
            'vn1': 'First Violin Voice',
            'vn2': 'Second Violin Voice',
            'va': 'Viola Voice',
            'vc': 'Cello Voice',
            })

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls string quartet score template.

        Returns score.
        """
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
        abjad.annotate(first_violin_staff, 'default_clef', clef)
        violin = abjad.Violin()
        abjad.annotate(first_violin_staff, 'default_instrument', violin)
        tag = abjad.LilyPondLiteral(r"\tag #'first-violin", 'before')
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
        abjad.annotate(second_violin_staff, 'default_clef', clef)
        violin = abjad.Violin()
        abjad.annotate(second_violin_staff, 'default_instrument', violin)
        tag = abjad.LilyPondLiteral(r"\tag #'second-violin", 'before')
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
        abjad.annotate(viola_staff, 'default_clef', clef)
        viola = abjad.Viola()
        abjad.annotate(viola_staff, 'default_instrument', viola)
        tag = abjad.LilyPondLiteral(r"\tag #'viola", 'before')
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
        abjad.annotate(cello_staff, 'default_clef', clef)
        cello = abjad.Cello()
        abjad.annotate(cello_staff, 'default_instrument', cello)
        tag = abjad.LilyPondLiteral(r"\tag #'cello", 'before')
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
