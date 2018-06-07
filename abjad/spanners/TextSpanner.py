import typing
from .Spanner import Spanner
from abjad.core.Leaf import Leaf
from abjad.enumerations import Center
from abjad.indicators.LineSegment import LineSegment
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.markup.Markup import Markup
from abjad.system.Tag import Tag
from abjad.system.Wrapper import Wrapper
from abjad.top.inspect import inspect
from abjad.top.new import new
from abjad.top.select import select
from abjad.utilities.OrderedDict import OrderedDict


class TextSpanner(Spanner):
    r"""
    Text spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[0])
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
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak dash-period 0
                - \tweak bound-details.left-broken.text ##f
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('tasto').upright(), spanner[-1])
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
                - \tweak Y-extent ##f
                - \tweak dash-period 0
                - \tweak bound-details.left-broken.text ##f
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #1.0
                            \upright
                                tasto
                        }
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[0])
        >>> spanner.attach(abjad.Markup('tasto').upright(), spanner[-1])
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
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak dash-period 0
                - \tweak bound-details.left-broken.text ##f
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #1.0
                            \upright
                                tasto
                        }
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[0])
        >>> spanner.attach(abjad.ArrowLineSegment(), spanner[0])
        >>> spanner.attach(abjad.Markup('tasto').upright(), spanner[-1])
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
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 0.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            \upright
                                tasto
                        }
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> arrow = abjad.ArrowLineSegment()
        >>> spanner.attach(abjad.Markup('one').upright(), spanner[0])
        >>> spanner.attach(arrow, spanner[0])
        >>> spanner.attach(abjad.Markup('two').upright(), spanner[1])
        >>> spanner.attach(arrow, spanner[1])
        >>> spanner.attach(abjad.Markup('three').upright(), spanner[2])
        >>> spanner.attach(arrow, spanner[2])
        >>> spanner.attach(abjad.Markup('four').upright(), spanner[3])
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
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                one
                            \hspace
                                #0.25
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 0.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                \startTextSpan
                d'4
                \stopTextSpan
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                two
                            \hspace
                                #0.25
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 0.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                \startTextSpan
                e'4
                \stopTextSpan
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                three
                            \hspace
                                #0.25
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 0.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            \upright
                                four
                        }
                    }
                \startTextSpan
                f'4
                \stopTextSpan
            }

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> arrow = abjad.ArrowLineSegment(left_hspace=0.75, right_padding=1)
        >>> spanner.attach(abjad.Markup('one').upright(), spanner[0])
        >>> spanner.attach(arrow, spanner[0])
        >>> spanner.attach(abjad.Markup('two').upright(), spanner[1])
        >>> spanner.attach(arrow, spanner[1])
        >>> spanner.attach(abjad.Markup('three').upright(), spanner[2])
        >>> spanner.attach(arrow, spanner[2])
        >>> spanner.attach(abjad.Markup('four').upright(), spanner[3])
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
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                one
                            \hspace
                                #0.75
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1
                - \tweak bound-details.right.stencil-align-dir-y #center
                \startTextSpan
                d'4
                \stopTextSpan
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                two
                            \hspace
                                #0.75
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1
                - \tweak bound-details.right.stencil-align-dir-y #center
                \startTextSpan
                e'4
                \stopTextSpan
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                three
                            \hspace
                                #0.75
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 1
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #0.5
                            \upright
                                four
                        }
                    }
                \startTextSpan
                f'4
                \stopTextSpan
            }

    ..  container:: example

        Nonpiecewise markup can be styled independently:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> spanner = abjad.TextSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> spanner.attach(abjad.Markup('ord.').upright(), spanner[0])
        >>> spanner.attach(abjad.ArrowLineSegment(), spanner[0])
        >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[-1])
        >>> markup = abjad.Markup('leggieriss.', direction=abjad.Up).italic()
        >>> abjad.attach(markup, staff[0])
        >>> abjad.override(staff[0]).text_script.color = 'blue'
        >>> abjad.override(staff).text_spanner.staff_padding = 2.5
        >>> abjad.override(staff).text_script.staff_padding = 5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextScript.staff-padding = #5
                \override TextSpanner.staff-padding = #2.5
            }
            {
                \once \override TextScript.color = #blue
                c'4
                - \tweak Y-extent ##f
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                ord.
                            \hspace
                                #0.25
                        }
                    }
                - \tweak arrow-width 0.25
                - \tweak dash-fraction 1
                - \tweak bound-details.left.stencil-align-dir-y #center
                - \tweak bound-details.right.arrow ##t
                - \tweak bound-details.right-broken.padding 0
                - \tweak bound-details.right-broken.text ##f
                - \tweak bound-details.right.padding 0.5
                - \tweak bound-details.right.stencil-align-dir-y #center
                - \tweak bound-details.right.text \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            \upright
                                pont.
                        }
                    }
                \startTextSpan
                ^ \markup {
                    \italic
                        leggieriss.
                    }
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
        '_commands',
        '_lilypond_id',
        '_skip_attachment_test_all',
        )

    _lilypond_ids = (1, 2, 3)

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        commands: typing.Tuple[str, str] = None,
        leak: bool = None,
        lilypond_id: int = None,
        ) -> None:
        Spanner.__init__(self, leak=leak)
        if commands is not None:
            assert isinstance(commands, tuple), repr(commands)
            assert all(isinstance(_, str) for _ in commands), repr(commands)
        self._commands = commands
        if lilypond_id is not None:
            assert lilypond_id in self._lilypond_ids, repr(lilypond_id)
        self._lilypond_id = lilypond_id
        self._skip_attachment_test_all = False

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        if self._skip_attachment_test_all:
            return True
        result = self._at_least_two_leaves(argument)
        if result is not True:
            return result
        leaves = select(argument).leaves()
        existing_spanners = inspect(leaves).get_spanners(
            prototype=TextSpanner,
            )
        for spanner in existing_spanners:
            if (spanner.lilypond_id == self.lilypond_id and
                spanner.commands == self.commands):
                if leaves[0] is spanner[-1] or leaves[-1] is spanner[0]:
                    continue
                message = 'Overlapping text spanners'
                message += f' with LilyPond ID {self.lilypond_id}'
                message += f' and commands {self.commands}.'
                return [message]
        return True

    def _copy_keywords(self, new):
        Spanner._copy_keywords(self, new)
        new._lilypond_id = self.lilypond_id

    def _get_lilypond_format_bundle(self, component=None):
        bundle = self._get_basic_lilypond_format_bundle(component)
        markup = inspect(component).get_piecewise(self, Markup, None)
        line_segment = inspect(component).get_piecewise(
            self,
            LineSegment,
            None,
            )
        if self._should_format_last_leaf_markup(component):
            last_leaf_markup = inspect(self[-1]).get_piecewise(self, Markup)
        else:
            last_leaf_markup = None
        indicators = (markup, line_segment, last_leaf_markup)
        has_indicators = any(_ is not None for _ in indicators)
        if not has_indicators:
            if component is self[0]:
                if self._wrappers:
                    override = self._y_extent_false()
                    string = override.tweak_string()
                    bundle.right.spanner_starts.append(string)
                    line_segment = self._make_invisible_line_segment()
                    tweaks = line_segment._get_lilypond_grob_overrides(
                        tweaks=True)
                    bundle.right.spanner_starts.extend(tweaks)
                bundle.right.spanner_starts.extend(self.start_command())
            if component is self[-1]:
                bundle.right.spanner_stops.append(self.stop_command())
            return bundle
        if has_indicators and not component is self[0]:
            bundle.right.spanner_stops.append(self.stop_command())
        if not component is self[-1]:
            if self._wrappers:
                override = self._y_extent_false()
                string = override.tweak_string()
                bundle.right.spanner_starts.append(string)
            if line_segment is None:
                line_segment = self._make_invisible_line_segment()
            if markup is not None:
                if line_segment.left_hspace is not None:
                    left_hspace = line_segment.left_hspace
                    left_hspace = Markup.hspace(left_hspace)
                    markup = Markup.concat([markup, left_hspace])
                override = LilyPondGrobOverride(
                    grob_name='TextSpanner',
                    property_path=(
                        'bound-details',
                        'left',
                        'text',
                        ),
                    value=markup,
                    )
                string = override.tweak_string()
                bundle.right.spanner_starts.append(string)
            tweaks = line_segment._get_lilypond_grob_overrides(tweaks=True)
            bundle.right.spanner_starts.extend(tweaks)
        if last_leaf_markup is not None:
            right_hspace = line_segment.right_padding or 0
            # optical correction to draw last markup left:
            right_hspace -= 0.5
            right_hspace = Markup.hspace(right_hspace)
            last_leaf_markup = Markup.concat(
                [right_hspace, last_leaf_markup],
                )
            last_leaf_markup = new(last_leaf_markup, direction=None)
            override = LilyPondGrobOverride(
                grob_name='TextSpanner',
                property_path=(
                    'bound-details',
                    'right',
                    'text',
                    ),
                value=last_leaf_markup,
                )
            string = override.tweak_string()
            bundle.right.spanner_starts.append(string)
        # start- and stop-commands added after tweaks
        if not component is self[-1]:
            bundle.right.spanner_starts.extend(self.start_command())
        return bundle

    @staticmethod
    def _make_invisible_line_segment():
        return LineSegment(
            dash_period=0,
            left_broken_text=False,
            left_hspace=0.25,
            left_stencil_align_direction_y=Center,
            right_broken_padding=0,
            right_broken_text=False,
            right_padding=1.5,
            right_stencil_align_direction_y=Center,
            )

    def _should_format_last_leaf_markup(self, component):
        if inspect(self[-1]).get_piecewise(self, Markup, None) is None:
            return
        leaf = None
        for leaf in reversed(self[:-1]):
            markup = inspect(leaf).get_piecewise(self, Markup, None)
            if markup is not None:
                break
            line_segment = inspect(leaf).get_piecewise(self, LineSegment, None)
            if line_segment is not None:
                break
        return component is leaf

    @property
    def _start_command(self):
        if self.commands is not None:
            start_command, stop_command = self.commands
            return start_command
        if self.lilypond_id is None:
            return r'\startTextSpan'
        elif self.lilypond_id == 1:
            return r'\startTextSpanOne'
        elif self.lilypond_id == 2:
            return r'\startTextSpanTwo'
        elif self.lilypond_id == 3:
            return r'\startTextSpanThree'
        else:
            raise ValueError(self.lilypond_id)

    def _stop_command(self):
        if self.commands is not None:
            start_command, stop_command = self.commands
            return stop_command
        if self.lilypond_id is None:
            return r'\stopTextSpan'
        elif self.lilypond_id == 1:
            return r'\stopTextSpanOne'
        elif self.lilypond_id == 2:
            return r'\stopTextSpanTwo'
        elif self.lilypond_id == 3:
            return r'\stopTextSpanThree'
        else:
            raise ValueError(self.lilypond_id)

    @staticmethod
    def _y_extent_false():
        return LilyPondGrobOverride(
            grob_name='TextSpanner',
            once=True,
            property_path=(
                'Y-extent',
                ),
            value=False,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Optional[typing.Tuple[str, str]]:
        r"""
        Gets custom start- and stop-commands.

        ..  container:: example

            >>> start_command = r'\startParameterXYZTextSpan'
            >>> stop_command = r'\stopParameterXYZTextSpan'
            >>> spanner = abjad.TextSpanner(
            ...     commands=(start_command, stop_command),
            ...     )
            >>> spanner.commands
            ('\\startParameterXYZTextSpan', '\\stopParameterXYZTextSpan')

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \startParameterXYZTextSpan
                d'4
                e'4
                f'4
                \stopParameterXYZTextSpan
            }

            Only LilyPond output is shown here because notational output would
            require the definition of ``\startParameterXYZTextSpan`` and
            ``\stopParameterXYZTextSpan`` beforehand.

        """
        return self._commands

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when spanner leaks one leaf to the right.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d'4 e'4 r4")
            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:-1])
            >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[0])
            >>> spanner.attach(abjad.ArrowLineSegment(), spanner[0])
            >>> spanner.attach(abjad.Markup('tasto').upright(), spanner[-1])
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
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    tasto
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    \stopTextSpan
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d'4 e'4 r4")
            >>> spanner = abjad.TextSpanner(leak=True)
            >>> abjad.attach(spanner, staff[:-1])
            >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[0])
            >>> spanner.attach(abjad.ArrowLineSegment(), spanner[0])
            >>> spanner.attach(abjad.Markup('tasto').upright(), spanner[-1])
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
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    tasto
                            }
                        }
                    \startTextSpan
                    d'4
                    e'4
                    <> \stopTextSpan
                    r4
                }

        """
        return super(TextSpanner, self).leak

    @property
    def lilypond_id(self) -> typing.Optional[int]:
        r"""
        Gets LilyPond ID.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")

            >>> spanner_1 = abjad.TextSpanner(lilypond_id=1)
            >>> abjad.attach(spanner_1, staff[:])
            >>> spanner_1.attach(abjad.Markup('ord.').upright(), spanner_1[0])
            >>> spanner_1.attach(abjad.ArrowLineSegment(), spanner_1[0])
            >>> spanner_1.attach(abjad.Markup('pont.').upright(), spanner_1[-1])
            >>> abjad.tweak(spanner_1).staff_padding = 2.5

            >>> spanner = abjad.TextSpanner()
            >>> abjad.attach(spanner, staff[:])
            >>> spanner.attach(abjad.Markup('A').upright(), spanner[0])
            >>> spanner.attach(abjad.ArrowLineSegment(), spanner[0])
            >>> spanner.attach(abjad.Markup('B').upright(), spanner[-1])
            >>> abjad.tweak(spanner).staff_padding = 5

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    ord.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    pont.
                            }
                        }
                    - \tweak staff-padding #2.5
                    \startTextSpanOne
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    A
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    B
                            }
                        }
                    - \tweak staff-padding #5
                    \startTextSpan
                    d'4
                    e'4
                    fs'4
                    \stopTextSpanOne
                    \stopTextSpan
                }

            Simultaneous text spanners can be freely positioned vertically as
            shown below only when Y-extent is set to false; Abjad text spanners
            set Y-extent to false for this reason:
           
            >>> abjad.tweak(spanner_1).staff_padding = 5
            >>> abjad.tweak(spanner).staff_padding = 2.5

            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    ord.
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    pont.
                            }
                        }
                    - \tweak staff-padding #5
                    \startTextSpanOne
                    - \tweak Y-extent ##f
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    A
                                \hspace
                                    #0.25
                            }
                        }
                    - \tweak arrow-width 0.25
                    - \tweak dash-fraction 1
                    - \tweak bound-details.left.stencil-align-dir-y #center
                    - \tweak bound-details.right.arrow ##t
                    - \tweak bound-details.right-broken.padding 0
                    - \tweak bound-details.right-broken.text ##f
                    - \tweak bound-details.right.padding 0.5
                    - \tweak bound-details.right.stencil-align-dir-y #center
                    - \tweak bound-details.right.text \markup {
                        \concat
                            {
                                \hspace
                                    #0.0
                                \upright
                                    B
                            }
                        }
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    fs'4
                    \stopTextSpanOne
                    \stopTextSpan
                }

        ..  container:: example

            LilyPond ID survives copy:

            >>> import copy

            >>> spanner_1 = abjad.TextSpanner(lilypond_id=1)
            >>> spanner_1
            TextSpanner(lilypond_id=1)

            >>> spanner_2 = copy.copy(spanner_1)
            >>> spanner_2
            TextSpanner(lilypond_id=1)

            >>> spanner_1.lilypond_id == spanner_2.lilypond_id
            True

            And new:

            >>> spanner_1 = abjad.TextSpanner(lilypond_id=1)
            >>> spanner_1
            TextSpanner(lilypond_id=1)

            >>> spanner_2 = abjad.new(spanner_1)
            >>> spanner_2
            TextSpanner(lilypond_id=1)

            >>> spanner_1.lilypond_id == spanner_2.lilypond_id
            True

        ..  container:: example

            Raises exception when attempting to attach text spanners with
            duplicate LilyPond ID / command profile:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> spanner = abjad.TextSpanner(lilypond_id=1)
            >>> spanner_1 = abjad.TextSpanner(lilypond_id=1)
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.attach(spanner_1, staff[:])
            Traceback (most recent call last):
                ...
            Exception: TextSpanner(lilypond_id=1)._attachment_test_all():
              Overlapping text spanners with LilyPond ID 1 and commands None.

        """
        return self._lilypond_id

    ### PUBLIC METHODS ###

    def attach(
        self,
        indicator: typing.Union[LineSegment, Markup, Wrapper], 
        leaf: Leaf,
        deactivate: bool = None,
        tag: typing.Union[str, Tag] = None,
        wrapper: bool = None,
        ) -> typing.Optional[Wrapper]:
        """
        Attaches ``indicator`` to ``leaf`` in spanner.
        """
        prototype = (LineSegment, Markup, Wrapper)
        assert isinstance(indicator, prototype), repr(indicator)
        assert isinstance(leaf, Leaf), repr(leaf)
        if tag is not None:
            assert isinstance(tag, Tag), repr(tag)
        return super(TextSpanner, self)._attach_piecewise(
            indicator,
            leaf,
            deactivate=deactivate,
            tag=tag,
            wrapper=wrapper,
            )

    def start_command(self) -> typing.List[str]:
        r"""
        Gets start command.

        ..  container:: example

            >>> abjad.TextSpanner().start_command()
            ['\\startTextSpan']

        """
        return super(TextSpanner, self).start_command()

    def stop_command(self) -> typing.Optional[str]:
        r"""
        Gets stop command.

        ..  container:: example

            >>> abjad.TextSpanner().stop_command()
            '\\stopTextSpan'

            With leak:

            >>> abjad.TextSpanner(leak=True).stop_command()
            '<> \\stopTextSpan'

        """
        string = self._stop_command()
        string = self._add_leak(string)
        return string
