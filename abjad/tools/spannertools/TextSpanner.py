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
            \new Staff \with {
                \override TextSpanner.staff-padding = #2.5
            } {
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
            \new Staff \with {
                \override TextSpanner.staff-padding = #2.5
            } {
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
            \new Staff \with {
                \override TextSpanner.staff-padding = #2.5
            } {
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
            \new Staff \with {
                \override TextSpanner.staff-padding = #2.5
            } {
                \once \override TextSpanner.Y-extent = ##f
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
            \new Staff \with {
                \override TextSpanner.staff-padding = #2.5
            } {
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left-broken.text = ##f
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
                \once \override TextSpanner.bound-details.left-broken.text = ##f
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
                \once \override TextSpanner.bound-details.left-broken.text = ##f
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
            \new Staff \with {
                \override TextSpanner.staff-padding = #2.5
            } {
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left-broken.text = ##f
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
                \once \override TextSpanner.bound-details.left-broken.text = ##f
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
                \once \override TextSpanner.bound-details.left-broken.text = ##f
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
            \new Staff \with {
                \override TextScript.staff-padding = #5
                \override TextSpanner.staff-padding = #2.5
            } {
                \once \override TextScript.color = #blue
                \once \override TextSpanner.Y-extent = ##f
                \once \override TextSpanner.arrow-width = 0.25
                \once \override TextSpanner.bound-details.left-broken.text = ##f
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
        Exception: TextSpanner() attachment test fails for ...
        <BLANKLINE>
        Selection([Note("c'4")])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_skip_attachment_test_all',
        )

    ### INITIALIZER ###

    def __init__(self, overrides=None):
        Spanner.__init__(self, overrides=overrides)
        self._skip_attachment_test_all = False

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        if self._skip_attachment_test_all:
            return True
        return self._at_least_two_leaves(argument)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(component)
        markup = abjad.inspect(component).get_piecewise(abjad.Markup, None)
        line_segment = abjad.inspect(component).get_piecewise(
            abjad.LineSegment,
            None,
            )
        if self._should_format_last_leaf_markup(component):
            last_leaf_markup = abjad.inspect(self[-1]).get_piecewise(
                abjad.Markup,
                )
        else:
            last_leaf_markup = None
        indicators = (markup, line_segment, last_leaf_markup)
        has_indicators = any(_ is not None for _ in indicators)
        if not has_indicators:
            if component is self[0]:
                bundle.right.spanner_starts.append(r'\startTextSpan')
                if self._wrappers:
                    string = r'\once \override TextSpanner.Y-extent = ##f'
                    bundle.grob_overrides.append(string)
                    line_segment = self._make_invisible_line_segment()
                    overrides = line_segment._get_lilypond_grob_overrides()
                    for override in overrides:
                        override_string = override.override_string
                        bundle.grob_overrides.append(override_string)
            if component is self[-1]:
                bundle.right.spanner_stops.append(r'\stopTextSpan')
            return bundle
        if has_indicators and not component is self[0]:
            bundle.right.spanner_stops.append(r'\stopTextSpan')
        if not component is self[-1]:
            bundle.right.spanner_starts.append(r'\startTextSpan')
            if self._wrappers:
                string = r'\once \override TextSpanner.Y-extent = ##f'
                bundle.grob_overrides.append(string)
            if line_segment is None:
                line_segment = self._make_invisible_line_segment()
            if markup is not None:
                if line_segment.left_hspace is not None:
                    left_hspace = line_segment.left_hspace
                    left_hspace = abjad.Markup.hspace(left_hspace)
                    markup = abjad.Markup.concat([markup, left_hspace])
                override = abjad.LilyPondGrobOverride(
                    grob_name='TextSpanner',
                    once=True,
                    property_path=(
                        'bound-details',
                        'left',
                        'text',
                        ),
                    value=markup,
                    )
                override_string = override.override_string
                bundle.grob_overrides.append(override_string)
            overrides = line_segment._get_lilypond_grob_overrides()
            for override in overrides:
                override_string = override.override_string
                bundle.grob_overrides.append(override_string)
        if last_leaf_markup is not None:
            right_hspace = line_segment.right_padding or 0
            # optical correction to draw last markup left:
            right_hspace -= 0.5
            right_hspace = abjad.Markup.hspace(right_hspace)
            last_leaf_markup = abjad.Markup.concat(
                [right_hspace, last_leaf_markup],
                )
            last_leaf_markup = abjad.new(last_leaf_markup, direction=None)
            override = abjad.LilyPondGrobOverride(
                grob_name='TextSpanner',
                once=True,
                property_path=(
                    'bound-details',
                    'right',
                    'text',
                    ),
                value=last_leaf_markup,
                )
            override_string = override.override_string
            bundle.grob_overrides.append(override_string)
        return bundle

    @staticmethod
    def _make_invisible_line_segment():
        import abjad
        return abjad.LineSegment(
            dash_period=0,
            left_broken_text=False,
            left_hspace=0.25,
            left_stencil_align_direction_y=abjad.Center,
            right_broken_padding=0,
            right_broken_text=False,
            right_padding=1.5,
            right_stencil_align_direction_y=abjad.Center,
            )

    def _should_format_last_leaf_markup(self, component):
        import abjad
        if abjad.inspect(self[-1]).get_piecewise(abjad.Markup, None) is None:
            return
        prototype = (abjad.LineSegment, abjad.Markup)
        leaf = None
        for leaf in reversed(self[:-1]):
            markup = abjad.inspect(leaf).get_piecewise(abjad.Markup, None)
            if markup is not None:
                break
            line_segment = abjad.inspect(leaf).get_piecewise(
                abjad.LineSegment,
                None,
                )
            if line_segment is not None:
                break
        return component is leaf

    ### PUBLIC PROPERTIES ###

    @property
    def overrides(self):
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
                \new Staff {
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
                    \revert TextSpanner.bound-details
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
                    \revert TextSpanner.bound-details
                    f'4 \stopTextSpan
                }

        '''
        superclass = super(TextSpanner, self)
        return superclass.overrides

    ### PUBLIC METHODS ###

    def attach(self, indicator, leaf, deactivate=None, site=None, tag=None):
        r'''Attaches `indicator` to `leaf` in spanner.

        Returns none.
        '''
        superclass = super(TextSpanner, self)
        superclass._attach_piecewise(
            indicator,
            leaf,
            deactivate=deactivate,
            site=site,
            tag=tag,
            )
