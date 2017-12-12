import collections
from .ScoreTemplate import ScoreTemplate


class GroupedStavesScoreTemplate(ScoreTemplate):
    r'''Grouped staves score template.

    ..  container:: example

        >>> class_ = abjad.GroupedStavesScoreTemplate
        >>> template = class_(staff_count=4)
        >>> abjad.show(template) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(template.__illustrate__()[abjad.Score])
            \context Score = "Grouped Staves Score" <<
                \context StaffGroup = "Grouped Staves Staff Group" <<
                    \context Staff = "Staff 1" {
                        \context Voice = "Voice 1" {
                            s1
                        }
                    }
                    \context Staff = "Staff 2" {
                        \context Voice = "Voice 2" {
                            s1
                        }
                    }
                    \context Staff = "Staff 3" {
                        \context Voice = "Voice 3" {
                            s1
                        }
                    }
                    \context Staff = "Staff 4" {
                        \context Voice = "Voice 4" {
                            s1
                        }
                    }
                >>
            >>

        >>> score = template()
        >>> abjad.f(score)
        \context Score = "Grouped Staves Score" <<
            \context StaffGroup = "Grouped Staves Staff Group" <<
                \context Staff = "Staff 1" {
                    \context Voice = "Voice 1" {
                    }
                }
                \context Staff = "Staff 2" {
                    \context Voice = "Voice 2" {
                    }
                }
                \context Staff = "Staff 3" {
                    \context Voice = "Voice 3" {
                    }
                }
                \context Staff = "Staff 4" {
                    \context Voice = "Voice 4" {
                    }
                }
            >>
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_name_abbreviations',
        '_staff_count',
        )

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        self._context_name_abbreviations = collections.OrderedDict()
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls score template.

        Returns score.
        '''
        import abjad
        staves = []
        for index in range(self.staff_count):
            number = index + 1
            voice = abjad.Voice(
                [],
                name='Voice {}'.format(number),
                )
            staff = abjad.Staff(
                [voice],
                name='Staff {}'.format(number),
                )
            staves.append(staff)
            self.context_name_abbreviations['v{}'.format(number)] = voice.name
        staff_group = abjad.StaffGroup(
            staves,
            name='Grouped Staves Staff Group',
            )
        score = abjad.Score(
            [staff_group],
            name='Grouped Staves Score',
            )
        return score

    ### PUBLIC PROPERTIES ###

    @property
    def context_name_abbreviations(self):
        r'''Gets context name abbreviations.

        ..  container::

            >>> class_ = abjad.GroupedStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.context_name_abbreviations
            OrderedDict()

        '''
        return self._context_name_abbreviations

    @property
    def staff_count(self):
        r'''Gets staff count.

        ..  container::

            >>> class_ = abjad.GroupedStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.staff_count
            4

        '''
        return self._staff_count
