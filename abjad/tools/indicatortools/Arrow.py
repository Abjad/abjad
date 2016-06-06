# -*- coding: utf-8 -*-
from abjad.tools.indicatortools.LineSegment import LineSegment


class Arrow(LineSegment):
    r'''An arrow.

    ..  container:: example

        **Example 1.** String contact position spanner:
            
        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> start_markup = Markup('pont.').upright()
            >>> stop_markup = Markup('ord.').upright()
            >>> arrow = indicatortools.Arrow()

        ::

            >>> print(format(arrow))
            indicatortools.Arrow(
                arrow_width=0.25,
                dash_fraction=1,
                left_broken_text=False,
                left_hspace=0.25,
                left_stencil_align_direction_y=Center,
                right_arrow=True,
                right_broken_padding=0,
                right_padding=1.5,
                right_stencil_align_direction_y=Center,
                )

        ::

            >>> attach(start_markup, staff[0], is_annotation=True)
            >>> attach(stop_markup, staff[-1], is_annotation=True)
            >>> attach(arrow, staff[0])
            >>> attach(spannertools.TextSpanner(), staff[:])

        ::

            >>> override(staff).text_script.staff_padding = 1.25
            >>> override(staff).text_spanner.staff_padding = 2
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff \with {
                \override TextScript.staff-padding = #1.25
                \override TextSpanner.staff-padding = #2
            } {
                \once \override TextSpanner.arrow-width = 0.25
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
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                \once \override TextSpanner.dash-fraction = 1
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan ^ \markup {
                    \upright
                        ord.
                    }
            }

    Arrow is a preconfigured line segment.

    Arrow formats as a text spanner.

    Follow the piecewise definition protocol shown here.
    '''

    ### CLASS VARIABLES ###

    # must be present for copy, deepcopy, pickle
    __slots__ = (
        '_default_scope',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        arrow_width=0.25,
        dash_fraction=1,
        dash_period=None,
        left_broken_padding=None,
        left_broken_text=False,
        left_hspace=0.25,
        left_padding=None,
        left_stencil_align_direction_y=Center,
        right_arrow=True,
        right_broken_arrow=None,
        right_broken_padding=0,
        right_padding=1.5,
        right_stencil_align_direction_y=Center,
        style=None,
        ):
        superclass = super(Arrow, self)
        self._default_scope = None
        superclass.__init__(
            arrow_width=arrow_width,
            dash_fraction=dash_fraction,
            dash_period=dash_period,
            left_broken_padding=left_broken_padding,
            left_broken_text=left_broken_text,
            left_hspace=left_hspace,
            left_padding=left_padding,
            left_stencil_align_direction_y=left_stencil_align_direction_y,
            right_arrow=right_arrow,
            right_broken_arrow=right_broken_arrow,
            right_broken_padding=right_broken_padding,
            right_padding=right_padding,
            right_stencil_align_direction_y=right_stencil_align_direction_y,
            style=style,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def arrow_width(self):
        r'''Gets arrow width of arrow.
        
        ..  container:: example

            **Example 1.** Arrow width equals ``0.25``:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(arrow_width=0.25)

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            Results in thin arrow head.

            This is default behavior.

        ..  container:: example

            **Example 2.** Arrow width equals ``0.5``:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(arrow_width=0.5)

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.5
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            Results in wide arrow head.

        ..  container:: example

            **Example 3.** Arrow width equals ``1``:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(arrow_width=1)

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 1
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            Results in very wide arrow head.

        Defaults to ``0.25``.

        Returns integer or float.
        '''
        superclass = super(Arrow, self)
        return superclass.arrow_width

    @property
    def dash_fraction(self):
        r'''Gets dash fraction of arrow.
        
        ..  container:: example

            **Example 1.** Dash fraction equals 100% of dash period:


            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(dash_fraction=1)

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            This is default behavior.

        ..  container:: example

            **Example 2.** Dash fraction equals 50% of dash period:


            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(dash_fraction=0.5)

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.5
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

        ..  container:: example

            **Example 3.** Dash fraction equals 10% of dash period:


            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(dash_fraction=0.1)

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

        Defaults to ``1``.

        Returns integer or float.
        '''
        superclass = super(Arrow, self)
        return superclass.dash_fraction

    @property
    def dash_period(self):
        r'''Gets dash period of arrow.

        ..  container:: example

            **Example 1.** Dash period equals none:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(
                ...     dash_period=None,
                ...     )

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            Results in a solid line.

            This is default behavior.

        ..  container:: example

            **Example 2.** Dash period equals ``1`` (with dash fraction equal
            to 25%):

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(
                ...     dash_fraction=0.25,
                ...     dash_period=1,
                ...     )

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            Results in fine dashes.

        ..  container:: example

            **Example 3.** Dash period equals ``4`` (with dash fraction equal
            to 25%):

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(
                ...     dash_fraction=0.25,
                ...     dash_period=4,
                ...     )

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 0.25
                    \once \override TextSpanner.dash-period = 4
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            Results in coarse dashes.

        Defaults to none.

        Returns integer or float.
        '''
        superclass = super(Arrow, self)
        return superclass.dash_period

    @property
    def default_scope(self):
        r'''Gets default scope of arrow.

        ..  container:: example

            >>> arrow = indicatortools.Arrow()
            >>> arrow.default_scope is None
            True

        Returns none.
        '''
        return self._default_scope

    @property
    def left_broken_text(self):
        r'''Gets left broken text of arrow.

        ..  container:: example

            **Example 1.** Left broken text set to false:

            ..  container:: example

                ::

                    >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                    >>> attach(TimeSignature((3, 8)), staff)
                    >>> score = Score([staff])
                    >>> command = indicatortools.LilyPondCommand('break', 'after')
                    >>> attach(command, staff[3])

                ::

                    >>> start_markup = Markup('pont.').upright()
                    >>> stop_markup = Markup('ord.').upright()
                    >>> arrow = indicatortools.Arrow()

                ::

                    >>> print(format(arrow))
                    indicatortools.Arrow(
                        arrow_width=0.25,
                        dash_fraction=1,
                        left_broken_text=False,
                        left_hspace=0.25,
                        left_stencil_align_direction_y=Center,
                        right_arrow=True,
                        right_broken_padding=0,
                        right_padding=1.5,
                        right_stencil_align_direction_y=Center,
                        )

                ::

                    >>> attach(start_markup, staff[2], is_annotation=True)
                    >>> attach(stop_markup, staff[6], is_annotation=True)
                    >>> attach(arrow, staff[2])
                    >>> attach(spannertools.TextSpanner(), staff[2:])

                ::

                    >>> override(staff).text_script.staff_padding = 1.25
                    >>> override(staff).text_spanner.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  doctest::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    } {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
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
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1.5
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 1
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \upright
                                ord.
                            }
                        c''4.
                    }

            Results in no text immediately after line break.
            (This is default behavior.)

        ..  container:: example

            **Example 2.** Left broken text set explicitly:

            ..  container:: example

                ::

                    >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                    >>> attach(TimeSignature((3, 8)), staff)
                    >>> score = Score([staff])
                    >>> command = indicatortools.LilyPondCommand('break', 'after')
                    >>> attach(command, staff[3])

                ::

                    >>> start_markup = Markup('pont.').upright()
                    >>> stop_markup = Markup('ord.').upright()
                    >>> left_broken_markup = Markup('(pont./ord.)').upright()
                    >>> arrow = indicatortools.Arrow(
                    ...     left_broken_text=left_broken_markup,
                    ... )

                ::

                    >>> print(format(arrow))
                    indicatortools.Arrow(
                        arrow_width=0.25,
                        dash_fraction=1,
                        left_broken_text=markuptools.Markup(
                            contents=(
                                markuptools.MarkupCommand(
                                    'upright',
                                    '(pont./ord.)'
                                    ),
                                ),
                            ),
                        left_hspace=0.25,
                        left_stencil_align_direction_y=Center,
                        right_arrow=True,
                        right_broken_padding=0,
                        right_padding=1.5,
                        right_stencil_align_direction_y=Center,
                        )

                ::

                    >>> attach(start_markup, staff[2], is_annotation=True)
                    >>> attach(stop_markup, staff[6], is_annotation=True)
                    >>> attach(arrow, staff[2])
                    >>> attach(spannertools.TextSpanner(), staff[2:])

                ::

                    >>> override(staff).text_script.staff_padding = 1.25
                    >>> override(staff).text_spanner.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  doctest::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    } {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \upright
                                (pont./ord.)
                            }
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
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1.5
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 1
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \upright
                                ord.
                            }
                        c''4.
                    }

        Set to markup, boolean or none.
        '''
        return self._left_broken_text

    @property
    def right_broken_arrow(self):
        r'''Is true when arrow should appear immediately before line break.
        Otherwise false.

        ..  container:: example

            **Example 1.** Right broken arrow set to none:

            ..  container:: example

                ::

                    >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                    >>> attach(TimeSignature((3, 8)), staff)
                    >>> score = Score([staff])
                    >>> command = indicatortools.LilyPondCommand('break', 'after')
                    >>> attach(command, staff[3])

                ::

                    >>> start_markup = Markup('pont.').upright()
                    >>> stop_markup = Markup('ord.').upright()
                    >>> arrow = indicatortools.Arrow()

                ::

                    >>> print(format(arrow))
                    indicatortools.Arrow(
                        arrow_width=0.25,
                        dash_fraction=1,
                        left_broken_text=False,
                        left_hspace=0.25,
                        left_stencil_align_direction_y=Center,
                        right_arrow=True,
                        right_broken_padding=0,
                        right_padding=1.5,
                        right_stencil_align_direction_y=Center,
                        )

                ::

                    >>> attach(start_markup, staff[2], is_annotation=True)
                    >>> attach(stop_markup, staff[6], is_annotation=True)
                    >>> attach(arrow, staff[2])
                    >>> attach(spannertools.TextSpanner(), staff[2:])

                ::

                    >>> override(staff).text_script.staff_padding = 1.25
                    >>> override(staff).text_spanner.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  doctest::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    } {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
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
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1.5
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 1
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \upright
                                ord.
                            }
                        c''4.
                    }

            Results in arrow immediately before line break.
            (This is default behavior.)

        ..  container:: example

            **Example 2.** Right broken arrow set to false:

            ..  container:: example

                ::

                    >>> staff = Staff("c'4. d' e' f' g' a' b' c''")
                    >>> attach(TimeSignature((3, 8)), staff)
                    >>> score = Score([staff])
                    >>> command = indicatortools.LilyPondCommand('break', 'after')
                    >>> attach(command, staff[3])

                ::

                    >>> start_markup = Markup('pont.').upright()
                    >>> stop_markup = Markup('ord.').upright()
                    >>> arrow = indicatortools.Arrow(
                    ...     right_broken_arrow=False,
                    ... )

                ::

                    >>> print(format(arrow))
                    indicatortools.Arrow(
                        arrow_width=0.25,
                        dash_fraction=1,
                        left_broken_text=False,
                        left_hspace=0.25,
                        left_stencil_align_direction_y=Center,
                        right_arrow=True,
                        right_broken_arrow=False,
                        right_broken_padding=0,
                        right_padding=1.5,
                        right_stencil_align_direction_y=Center,
                        )

                ::

                    >>> attach(start_markup, staff[2], is_annotation=True)
                    >>> attach(stop_markup, staff[6], is_annotation=True)
                    >>> attach(arrow, staff[2])
                    >>> attach(spannertools.TextSpanner(), staff[2:])

                ::

                    >>> override(staff).text_script.staff_padding = 1.25
                    >>> override(staff).text_spanner.staff_padding = 2
                    >>> show(staff) # doctest: +SKIP

                ..  doctest::

                    >>> f(staff)
                    \new Staff \with {
                        \override TextScript.staff-padding = #1.25
                        \override TextSpanner.staff-padding = #2
                    } {
                        \time 3/8
                        c'4.
                        d'4.
                        \once \override TextSpanner.arrow-width = 0.25
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
                        \once \override TextSpanner.bound-details.right-broken.arrow = ##f
                        \once \override TextSpanner.bound-details.right-broken.padding = 0
                        \once \override TextSpanner.bound-details.right.arrow = ##t
                        \once \override TextSpanner.bound-details.right.padding = 1.5
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                        \once \override TextSpanner.dash-fraction = 1
                        e'4. \startTextSpan
                        f'4.
                        \break
                        g'4.
                        a'4.
                        b'4. \stopTextSpan ^ \markup {
                            \upright
                                ord.
                            }
                        c''4.
                    }

        Set to true, false or none.
        '''
        return self._right_broken_arrow

    @property
    def style(self):
        r'''Gets style of arrow.

        ..  container:: example

            **Example 1.** Style equals none:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(style=None)

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

            LilyPond defaults to solid line.

            This is default behavior.

        ..  container:: example

            **Example 2.** Style equals zig-zag:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(style='zigzag')

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    \once \override TextSpanner.style = #'zigzag
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

        ..  container:: example

            **Example 3.** Style equals trill:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(style='trill')

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    \once \override TextSpanner.style = #'trill
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

        ..  container:: example

            **Example 4.** Style equals dotted line:

            ::

                >>> staff = Staff("c'4 d'4 e'4 f'4")
                >>> start_markup = Markup('pont.').upright()
                >>> stop_markup = Markup('ord.').upright()
                >>> arrow = indicatortools.Arrow(style='dotted-line')

            ::

                >>> attach(start_markup, staff[0], is_annotation=True)
                >>> attach(stop_markup, staff[-1], is_annotation=True)
                >>> attach(arrow, staff[0])
                >>> attach(spannertools.TextSpanner(), staff[:])

            ::

                >>> override(staff).text_script.staff_padding = 1.25
                >>> override(staff).text_spanner.staff_padding = 2
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override TextScript.staff-padding = #1.25
                    \override TextSpanner.staff-padding = #2
                } {
                    \once \override TextSpanner.arrow-width = 0.25
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
                    \once \override TextSpanner.bound-details.right.arrow = ##t
                    \once \override TextSpanner.bound-details.right.padding = 1.5
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center
                    \once \override TextSpanner.dash-fraction = 1
                    \once \override TextSpanner.style = #'dotted-line
                    c'4 \startTextSpan
                    d'4
                    e'4
                    f'4 \stopTextSpan ^ \markup {
                        \upright
                            ord.
                        }
                }

        Defaults to none.

        Returns string or none.
        '''
        superclass = super(Arrow, self)
        return superclass.style
