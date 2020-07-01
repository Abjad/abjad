import copy
import typing

from ..indicators.BarLine import BarLine
from ..lilypondnames.LilyPondGrobNameManager import override
from ..tags import Tag
from .Component import attach, inspect
from .Context import Context
from .Iteration import iterate
from .Selection import Selection
from .Voice import Voice


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

    ### PUBLIC METHODS ###

    # TODO: remove
    def add_final_bar_line(self, abbreviation="|.", to_each_voice=False):
        r"""
        Add final bar line to end of score.


            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> score = abjad.Score([staff])
            >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>


        >>> bar_line = score.add_final_bar_line()
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \bar "|." %! SCORE_1
                }
            >>

        Set ``to_each_voice`` to true to make part extraction easier.

        Returns bar line.
        """
        bar_line = BarLine(abbreviation)
        if not to_each_voice:
            last_leaf = inspect(self).leaf(-1)
            attach(bar_line, last_leaf, tag=Tag("SCORE_1"))
        else:
            for voice in iterate(self).components(Voice):
                last_leaf = inspect(voice).leaf(-1)
                attach(bar_line, last_leaf, tag=Tag("SCORE_1"))
        return bar_line

    # TODO: remove
    def add_final_markup(self, markup, extra_offset=None):
        r"""
        Adds ``markup`` to end of score.

        ..  container:: example

            Adds markup to last leaf:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> score = abjad.Score([staff])
            >>> place = abjad.Markup('Bremen - Boston - LA.', direction=abjad.Down)
            >>> date = abjad.Markup('July 2010 - May 2011.')
            >>> markup = abjad.Markup.right_column([place, date], direction=abjad.Down)
            >>> markup = markup.italic()
            >>> markup = score.add_final_markup(
            ...     markup,
            ...     extra_offset=(0.5, -2),
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    {
                        c'4
                        d'4
                        e'4
                        \once \override TextScript.extra-offset = #'(0.5 . -2)
                        f'4
                        _ \markup {                             %! SCORE_2
                            \italic                             %! SCORE_2
                                \right-column                   %! SCORE_2
                                    {                           %! SCORE_2
                                        "Bremen - Boston - LA." %! SCORE_2
                                        "July 2010 - May 2011." %! SCORE_2
                                    }                           %! SCORE_2
                            }                                   %! SCORE_2
                    }
                >>

        ..  container:: example

            Adds markup to last multimeasure rest:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff.append(abjad.MultimeasureRest((4, 4)))
            >>> score = abjad.Score([staff])
            >>> place = abjad.Markup(
            ...     'Bremen - Boston - LA.',
            ...     direction=abjad.Down,
            ...     )
            >>> date = abjad.Markup('July 2010 - May 2011.')
            >>> markup = abjad.Markup.right_column(
            ...     [place, date],
            ...     direction=abjad.Down,
            ...     )
            >>> markup = markup.italic()
            >>> markup = score.add_final_markup(
            ...     markup,
            ...     extra_offset=(14.5, -2),
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \once \override MultiMeasureRestText.extra-offset = #'(14.5 . -2)
                        R1
                        _ \markup {                             %! SCORE_2
                            \italic                             %! SCORE_2
                                \right-column                   %! SCORE_2
                                    {                           %! SCORE_2
                                        "Bremen - Boston - LA." %! SCORE_2
                                        "July 2010 - May 2011." %! SCORE_2
                                    }                           %! SCORE_2
                            }                                   %! SCORE_2
                    }
                >>

        Returns none.
        """
        from .Leaf import Leaf
        from .MultimeasureRest import MultimeasureRest

        selection = Selection(self)
        last_leaf = selection._get_component(Leaf, -1)
        markup = copy.copy(markup)
        attach(markup, last_leaf, tag=Tag("SCORE_2"))
        if extra_offset is not None:
            if isinstance(last_leaf, MultimeasureRest):
                grob_proxy = override(last_leaf).multi_measure_rest_text
            else:
                grob_proxy = override(last_leaf).text_script
            grob_proxy.extra_offset = extra_offset
        return markup
