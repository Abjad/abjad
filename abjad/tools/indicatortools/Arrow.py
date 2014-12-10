# -*- encoding: utf-8 -*-
from abjad.tools.indicatortools.LineSegment import LineSegment


class Arrow(LineSegment):
    r'''An arrow.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> start_markup = Markup('pont.').upright()
            >>> stop_markup = Markup('ord.').upright()
            >>> arrow = indicatortools.Arrow()

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
                \override TextScript #'staff-padding = #1.25
                \override TextSpanner #'staff-padding = #2
            } {
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left.stencil-align-dir-y = 0
                \once \override TextSpanner.bound-details.left.text = \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.25
                        }
                    }
                \once \override TextSpanner.bound-details.right.arrow = ##t
                \once \override TextSpanner.bound-details.right.padding = 1.5
                \once \override TextSpanner.bound-details.right.stencil-align-dir-y = 0
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

    ### INITIALIZER ###

    def __init__(
        self,
        arrow_width=0.25,
        dash_fraction=1,
        dash_period=None,
        left_arrow=None,
        left_broken_padding=None,
        left_hspace=0.25,
        left_padding=None,
        left_stencil_align_direction_y=0,
        right_arrow=True,
        right_broken_padding=None,
        right_padding=1.5,
        right_stencil_align_direction_y=0,
        style=None,
        ):
        superclass = super(Arrow, self)
        superclass.__init__(
            arrow_width=arrow_width,
            dash_fraction=dash_fraction,
            dash_period=dash_period,
            left_arrow=left_arrow,
            left_broken_padding=left_broken_padding,
            left_hspace=left_hspace,
            left_padding=left_padding,
            left_stencil_align_direction_y=left_stencil_align_direction_y,
            right_arrow=right_arrow,
            right_broken_padding=right_broken_padding,
            right_padding=right_padding,
            right_stencil_align_direction_y=right_stencil_align_direction_y,
            style=style,
            )