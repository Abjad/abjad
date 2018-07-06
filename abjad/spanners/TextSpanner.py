import typing
from abjad import enums
from abjad import typings
from abjad.core.Component import Component
from abjad.core.Leaf import Leaf
from abjad.core.Selection import Selection
from abjad.indicators.StartTextSpan import StartTextSpan
from abjad.indicators.StopTextSpan import StopTextSpan
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.markups import Markup
from abjad.system.Tag import Tag
from abjad.system.Wrapper import Wrapper
from abjad.top.attach import attach
from abjad.top.inspect import inspect
from abjad.top.new import new
from abjad.top.select import select
from abjad.utilities.Expression import Expression
from abjad.utilities.OrderedDict import OrderedDict
from .Spanner import Spanner


class TextSpanner(Spanner):
    r"""
    Text spanner.

    ..  note:: ``abjad.TextSpanner`` spanner is deprecated. Use the
        ``abjad.text_spanner()`` factory function instead.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.override(staff).text_spanner.staff_padding = 2.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #2.5
            }
            {
                c'4
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        Raises exception on fewer than two leaves:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:1])
        Traceback (most recent call last):
            ...
        Exception: TextSpanner()._attachment_test_all():
          Requires at least two leaves.
          Not just Note("c'4").

    ..  container:: example

        Raises exception on noncontiguous leaves:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:1] + staff[-1:])
        Traceback (most recent call last):
            ...
        Exception: TextSpanner() leaves must be contiguous:
          abjad.Selection(
            [
                abjad.Note("c'4"),
                abjad.Note("f'4"),
                ]
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_skip_attachment_test_all',
        )

    _start_command = r'\startTextSpan'

    _stop_command = r'\stopTextSpan'

    ### INITIALIZER ###

    def __init__(self) -> None:
        Spanner.__init__(self)
        self._skip_attachment_test_all = False

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        if self._skip_attachment_test_all:
            return True
        result = self._at_least_two_leaves(argument)
        if result is not True:
            return result
        leaves = select(argument).leaves()
        return True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = self._get_basic_lilypond_format_bundle(component)
        if component is self[0]:
            strings = self._tweaked_start_command_strings()
            bundle.after.spanner_starts.extend(strings)
        if component is self[-1]:
            string = self._stop_command_string()
            bundle.after.spanner_stops.append(string)
        return bundle

def text_spanner(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.Selector = 'abjad.select().leaves()',
    start_text_span: StartTextSpan = None,
    stop_text_span: StopTextSpan = None,
    ) -> None:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single spanner:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     right_text=abjad.Markup('tasto').upright(),
        ...     style='solid_line_with_arrow',
        ...     )
        >>> abjad.text_spanner(staff[:], start_text_span=start_text_span)
        >>> abjad.override(staff[0]).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override TextSpanner.staff-padding = #4
                c'4
                - \abjad_solid_line_with_arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                - \tweak bound-details.right.text \markup {
                    \upright
                        tasto
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        Enchained spanners:

        >>> staff = abjad.Staff("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     style='dashed_line_with_arrow',
        ...     )
        >>> abjad.text_spanner(staff[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('tasto').upright(),
        ...     right_text=abjad.Markup('pont.').upright(),
        ...     style='dashed_line_with_arrow',
        ...     )
        >>> abjad.text_spanner(staff[-3:], start_text_span=start_text_span)
        >>> abjad.override(staff).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #4
            }
            {
                c'4
                - \abjad_dashed_line_with_arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad_dashed_line_with_arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                tasto
                            \hspace
                                #0.5
                        }
                    }
                - \tweak bound-details.right.text \markup {
                    \upright
                        pont.
                    }
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

        >>> staff = abjad.Staff("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     style='dashed_line_with_arrow',
        ...     )
        >>> abjad.text_spanner(staff[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('tasto').upright(),
        ...     style='solid_line_with_hook',
        ...     )
        >>> abjad.text_spanner(staff[-3:], start_text_span=start_text_span)
        >>> abjad.override(staff).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #4
            }
            {
                c'4
                - \abjad_dashed_line_with_arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad_solid_line_with_hook
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                tasto
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

    """
    import abjad
    start_text_span = start_text_span or StartTextSpan()
    stop_text_span = stop_text_span or StopTextSpan()

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    
    attach(start_text_span, start_leaf)
    attach(stop_text_span, stop_leaf)
