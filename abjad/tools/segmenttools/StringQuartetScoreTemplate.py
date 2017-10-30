import collections
from .ScoreTemplate import ScoreTemplate


class StringQuartetScoreTemplate(ScoreTemplate):
    r'''String quartet score template.

    ..  container:: example

        >>> template = abjad.StringQuartetScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score])
        \context Score = "String Quartet Score" <<
            \context StaffGroup = "String Quartet Staff Group" <<
                \tag #'first-violin
                \context Staff = "First Violin Staff" {
                    \context Voice = "First Violin Voice" {
                        \set Staff.instrumentName = \markup { Violin }
                        \set Staff.shortInstrumentName = \markup { Vn. }
                        \clef "treble"
                        s1
                    }
                }
                \tag #'second-violin
                \context Staff = "Second Violin Staff" {
                    \context Voice = "Second Violin Voice" {
                        \set Staff.instrumentName = \markup { Violin }
                        \set Staff.shortInstrumentName = \markup { Vn. }
                        \clef "treble"
                        s1
                    }
                }
                \tag #'viola
                \context Staff = "Viola Staff" {
                    \context Voice = "Viola Voice" {
                        \set Staff.instrumentName = \markup { Viola }
                        \set Staff.shortInstrumentName = \markup { Va. }
                        \clef "alto"
                        s1
                    }
                }
                \tag #'cello
                \context Staff = "Cello Staff" {
                    \context Voice = "Cello Voice" {
                        \set Staff.instrumentName = \markup { Cello }
                        \set Staff.shortInstrumentName = \markup { Vc. }
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
            [],
            name='First Violin Voice',
            )
        first_violin_staff = abjad.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )
        clef = abjad.Clef('treble')
        #abjad.attach(clef, first_violin_staff)
        abjad.annotate(first_violin_staff, 'default_clef', clef)
        violin = abjad.instrumenttools.Violin()
        #abjad.attach(violin, first_violin_staff)
        abjad.annotate(first_violin_staff, 'default_instrument', violin)
        tag = abjad.LilyPondCommand("tag #'first-violin", 'before')
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
        #abjad.attach(clef, second_violin_staff)
        abjad.annotate(second_violin_staff, 'default_clef', clef)
        violin = abjad.instrumenttools.Violin()
        #abjad.attach(violin, second_violin_staff)
        abjad.annotate(second_violin_staff, 'default_instrument', violin)
        tag = abjad.LilyPondCommand("tag #'second-violin", 'before')
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
        #abjad.attach(clef, viola_staff)
        abjad.annotate(viola_staff, 'default_clef', clef)
        viola = abjad.instrumenttools.Viola()
        #abjad.attach(viola, viola_staff)
        abjad.annotate(viola_staff, 'default_instrument', viola)
        tag = abjad.LilyPondCommand("tag #'viola", 'before')
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
        #abjad.attach(clef, cello_staff)
        abjad.annotate(cello_staff, 'default_clef', clef)
        cello = abjad.instrumenttools.Cello()
        #abjad.attach(cello, cello_staff)
        abjad.annotate(cello_staff, 'default_instrument', cello)
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
