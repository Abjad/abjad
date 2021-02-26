import copy

from . import _iterate
from . import score as _score
from . import select
from . import tag as _tag
from .attach import attach
from .indicators.BarLine import BarLine
from .iterate import Iteration
from .overrides import override


def add_final_bar_line(score, abbreviation="|.", to_each_voice=False) -> BarLine:
    r"""
    Adds final bar line to end of score.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
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

        >>> bar_line = abjad.deprecated.add_final_bar_line(score)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \bar "|."
                }
            >>

    Set ``to_each_voice`` to true to make part extraction easier.
    """
    bar_line = BarLine(abbreviation)
    if not to_each_voice:
        last_leaf = _iterate._get_leaf(score, -1)
        attach(bar_line, last_leaf, tag=_tag.Tag("SCORE_1"))
    else:
        for voice in Iteration(score).components(_score.Voice):
            last_leaf = _iterate._get_leaf(voice, -1)
            attach(bar_line, last_leaf, tag=_tag.Tag("SCORE_1"))
    return bar_line


def add_final_markup(score, markup, extra_offset=None) -> None:
    r"""
    Adds ``markup`` to end of score.

    ..  container:: example

        Adds markup to last leaf:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> score = abjad.Score([staff])
        >>> place = "Bremen - Boston - LA."
        >>> date = "July 2010 - May 2011."
        >>> string = rf'\italic \right-column {{ "{place}" "{date}" }}'
        >>> markup = abjad.Markup(string, direction=abjad.Down)
        >>> markup = abjad.deprecated.add_final_markup(
        ...     score,
        ...     markup,
        ...     extra_offset="#'(0.5 . -2)",
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    \once \override TextScript.extra-offset = #'(0.5 . -2)
                    f'4
                    _ \markup {
                        \italic
                            \right-column
                                {
                                    "Bremen - Boston - LA."
                                    "July 2010 - May 2011."
                                }
                        }
                }
            >>

    ..  container:: example

        Adds markup to last multimeasure rest:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> staff.append(abjad.MultimeasureRest((4, 4)))
        >>> score = abjad.Score([staff])
        >>> place = "Bremen - Boston - LA."
        >>> date = "July 2010 - May 2011."
        >>> string = rf'\italic \right-column {{ "{place}" "{date}" }}'
        >>> markup = abjad.Markup(string, direction=abjad.Down)
        >>> markup = abjad.deprecated.add_final_markup(
        ...     score,
        ...     markup,
        ...     extra_offset="#'(14.5 . -2)",
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
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
                    _ \markup {
                        \italic
                            \right-column
                                {
                                    "Bremen - Boston - LA."
                                    "July 2010 - May 2011."
                                }
                        }
                }
            >>

    """
    selection = select.Selection(score)
    last_leaf = selection._get_component(_score.Leaf, -1)
    markup = copy.copy(markup)
    attach(markup, last_leaf, tag=_tag.Tag("SCORE_2"))
    if extra_offset is not None:
        if isinstance(last_leaf, _score.MultimeasureRest):
            grob_proxy = override(last_leaf).MultiMeasureRestText
        else:
            grob_proxy = override(last_leaf).TextScript
        grob_proxy.extra_offset = extra_offset
    return markup
