import typing
from abjad.tools.datastructuretools import Center
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from abjad.tools.indicatortools.LineSegment import LineSegment
from abjad.tools.lilypondnametools.LilyPondGrobOverride import \
    LilyPondGrobOverride
from abjad.tools.markuptools.Markup import Markup
from abjad.tools.scoretools.Leaf import Leaf
from abjad.tools.systemtools.Tag import Tag
from abjad.tools.systemtools.Wrapper import Wrapper
from abjad.tools.topleveltools.inspect import inspect
from abjad.tools.topleveltools.new import new
from .Spanner import Spanner


class TextSpanner(Spanner):
    r'''Text spanner.

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
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.bound-details.left-broken.text = ##f
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-period = 0
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
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
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.bound-details.left-broken.text = ##f
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right.text = \markup {
                    \concat
                        {
                            \hspace
                                #1.0
                            \upright
                                tasto
                        }
                    }
                \once \override TextSpanner.dash-period = 0
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
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
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.bound-details.left-broken.text = ##f
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right.text = \markup {
                    \concat
                        {
                            \hspace
                                #1.0
                            \upright
                                tasto
                        }
                    }
                \once \override TextSpanner.dash-period = 0
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
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
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 0.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right.text = \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            \upright
                                tasto
                        }
                    }
                \once \override TextSpanner.dash-fraction = 1
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
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
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                one
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 0.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-fraction = 1
                c'4 \startTextSpan
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                two
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 0.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-fraction = 1
                d'4 \stopTextSpan \startTextSpan
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                three
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 0.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right.text = \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            \upright
                                four
                        }
                    }
                \once \override TextSpanner.dash-fraction = 1
                e'4 \stopTextSpan \startTextSpan
                f'4 \stopTextSpan
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
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                one
                            \hspace
                                #0.75
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 1
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-fraction = 1
                c'4 \startTextSpan
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                two
                            \hspace
                                #0.75
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 1
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-fraction = 1
                d'4 \stopTextSpan \startTextSpan
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                three
                            \hspace
                                #0.75
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 1
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right.text = \markup {
                    \concat
                        {
                            \hspace
                                #0.5
                            \upright
                                four
                        }
                    }
                \once \override TextSpanner.dash-fraction = 1
                e'4 \stopTextSpan \startTextSpan
                f'4 \stopTextSpan
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
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                ord.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 0.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right.text = \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            \upright
                                pont.
                        }
                    }
                \once \override TextSpanner.dash-fraction = 1
                c'4 \startTextSpan
                    ^ \markup {
                        \italic
                            leggieriss.
                        }
                d'4
                e'4
                f'4 \stopTextSpan
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lilypond_id',
        '_skip_attachment_test_all',
        )

    _lilypond_ids = (1, 2, 3)

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_id: int = None,
        overrides: OrderedDict = None,
        ) -> None:
        Spanner.__init__(self, overrides=overrides)
        if lilypond_id is not None:
            assert lilypond_id in self._lilypond_ids, repr(lilypond_id)
        self._lilypond_id = lilypond_id
        self._skip_attachment_test_all = False

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        if self._skip_attachment_test_all:
            return True
        return self._at_least_two_leaves(argument)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = self._get_basic_lilypond_format_bundle(component)
        markup = inspect(component).get_piecewise(Markup, None)
        line_segment = inspect(component).get_piecewise(LineSegment, None)
        if self._should_format_last_leaf_markup(component):
            last_leaf_markup = inspect(self[-1]).get_piecewise(Markup)
        else:
            last_leaf_markup = None
        indicators = (markup, line_segment, last_leaf_markup)
        has_indicators = any(_ is not None for _ in indicators)
        if not has_indicators:
            if component is self[0]:
                bundle.right.spanner_starts.append(self._start_command())
                if self._wrappers:
                    string = r'\once \override TextSpanner.Y-extent = ##f'
                    bundle.grob_overrides.append(string)
                    line_segment = self._make_invisible_line_segment()
                    overrides = line_segment._get_lilypond_grob_overrides()
                    bundle.grob_overrides.extend(overrides)
            if component is self[-1]:
                bundle.right.spanner_stops.append(self._stop_command())
            return bundle
        if has_indicators and not component is self[0]:
            bundle.right.spanner_stops.append(self._stop_command())
        if not component is self[-1]:
            bundle.right.spanner_starts.append(self._start_command())
            if self._wrappers:
                string = r'\once \override TextSpanner.Y-extent = ##f'
                bundle.grob_overrides.append(string)
            if line_segment is None:
                line_segment = self._make_invisible_line_segment()
            if markup is not None:
                if line_segment.left_hspace is not None:
                    left_hspace = line_segment.left_hspace
                    left_hspace = Markup.hspace(left_hspace)
                    markup = Markup.concat([markup, left_hspace])
                override = LilyPondGrobOverride(
                    grob_name='TextSpanner',
                    once=True,
                    property_path=(
                        'bound-details',
                        'left',
                        'text',
                        ),
                    value=markup,
                    )
                string = override.override_string
                bundle.grob_overrides.append(string)
            overrides = line_segment._get_lilypond_grob_overrides()
            bundle.grob_overrides.extend(overrides)
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
                once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'text',
                    ),
                value=last_leaf_markup,
                )
            string = override.override_string
            bundle.grob_overrides.append(string)
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
        if inspect(self[-1]).get_piecewise(Markup, None) is None:
            return
        leaf = None
        for leaf in reversed(self[:-1]):
            markup = inspect(leaf).get_piecewise(Markup, None)
            if markup is not None:
                break
            line_segment = inspect(leaf).get_piecewise(LineSegment, None)
            if line_segment is not None:
                break
        return component is leaf

    def _start_command(self):
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

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_id(self) -> typing.Optional[int]:
        r'''Gets LilyPond ID.

        ..  todo:: finish integration.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> spanner = abjad.TextSpanner(lilypond_id=1)
            >>> abjad.attach(spanner, staff[:])
            >>> spanner.attach(abjad.Markup('ord.').upright(), spanner[0])
            >>> spanner.attach(abjad.ArrowLineSegment(), spanner[0])
            >>> spanner.attach(abjad.Markup('pont.').upright(), spanner[-1])
            >>> abjad.override(staff).text_spanner.staff_padding = 2.5

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #2.5
            }
            {
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                ord.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right-broken.padding = 0
                \once \override TextSpanner.bound-details.right-broken.text = ##f
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 0.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.bound-details.right.text = \markup {
                    \concat
                        {
                            \hspace
                                #0.0
                            \upright
                                pont.
                        }
                    }
                \once \override TextSpanner.dash-fraction = 1
                c'4 \startTextSpanOne
                d'4
                e'4
                f'4 \stopTextSpanOne
            }

        '''
        return self._lilypond_id

    @property
    def overrides(self) -> OrderedDict:
        r'''Gets text spanner overrides.

        ..  container:: example

            REGRESSION: Red spanner reverts color before default spanner
            begins:

            >>> staff = abjad.Staff("c'4 d' e' f' c' d' e' f'")
            >>> text_spanner_1 = abjad.TextSpanner()
            >>> markup = abjad.Markup('red').italic().bold()
            >>> abjad.override(text_spanner_1).text_spanner.bound_details__left__text = markup
            >>> abjad.override(text_spanner_1).text_spanner.bound_details__left__stencil_align_dir_y = 0
            >>> abjad.override(text_spanner_1).text_spanner.bound_details__right__padding = 1
            >>> abjad.override(text_spanner_1).text_spanner.color = 'red'
            >>> abjad.attach(text_spanner_1, staff[:4])
            >>> text_spanner_2 = abjad.TextSpanner()
            >>> markup = abjad.Markup('default').italic().bold()
            >>> abjad.override(text_spanner_2).text_spanner.bound_details__left__text = markup
            >>> abjad.override(text_spanner_2).text_spanner.bound_details__left__stencil_align_dir_y = 0
            >>> abjad.attach(text_spanner_2, staff[-5:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \override TextSpanner.bound-details.left.stencil-align-dir-y = #0
                    \override TextSpanner.bound-details.left.text = \markup {
                        \bold
                            \italic
                                red
                        }
                    \override TextSpanner.bound-details.right.padding = #1
                    \override TextSpanner.color = #red
                    c'4 \startTextSpan
                    d'4
                    e'4
                    \revert TextSpanner.bound-details.left.stencil-align-dir-y
                    \revert TextSpanner.bound-details.left.text
                    \revert TextSpanner.bound-details.right.padding
                    \revert TextSpanner.color
                    \override TextSpanner.bound-details.left.stencil-align-dir-y = #0
                    \override TextSpanner.bound-details.left.text = \markup {
                        \bold
                            \italic
                                default
                        }
                    f'4 \stopTextSpan \startTextSpan
                    c'4
                    d'4
                    e'4
                    \revert TextSpanner.bound-details.left.stencil-align-dir-y
                    \revert TextSpanner.bound-details.left.text
                    f'4 \stopTextSpan
                }

        '''
        return super(TextSpanner, self).overrides

    ### PUBLIC METHODS ###

    def attach(
        self,
        indicator: typing.Union[LineSegment, Markup, Wrapper], 
        leaf: Leaf,
        deactivate: bool = None,
        tag: Tag = None,
        wrapper: bool = None,
        ) -> typing.Optional[Wrapper]:
        r'''Attaches ``indicator`` to ``leaf`` in spanner.
        '''
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
