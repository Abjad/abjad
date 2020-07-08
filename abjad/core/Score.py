import typing

from ..tags import Tag
from .Context import Context


class Score(Context):
    r"""
    Score.

    ..  container:: example

        >>> staff_1 = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> staff_2 = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score = abjad.Score([staff_1, staff_2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Contexts"

    __slots__ = ()

    _default_lilypond_type = "Score"

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        lilypond_type: str = "Score",
        simultaneous: bool = True,
        name: str = None,
        tag: Tag = None,
    ) -> None:
        Context.__init__(
            self,
            components=components,
            lilypond_type=lilypond_type,
            simultaneous=simultaneous,
            name=name,
            tag=tag,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'", tag=abjad.Tag('RED'))
            >>> staff = abjad.Staff([voice], tag=abjad.Tag('BLUE'))
            >>> score = abjad.Score([staff], tag=abjad.Tag('GREEN'))
            >>> abjad.show(score) # doctest: +SKIP

            >>> abjad.f(score, strict=20)
            \new Score          %! GREEN
            <<                  %! GREEN
                \new Staff      %! BLUE
                {               %! BLUE
                    \new Voice  %! RED
                    {           %! RED
                        c'4
                        d'4
                        e'4
                        f'4
                    }           %! RED
                }               %! BLUE
            >>                  %! GREEN

        """
        return super().tag
