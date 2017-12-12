from .Spanner import Spanner


class BowContactSpanner(Spanner):
    r'''Bow contact spanner.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> staff.extend(r"c'4. c'8 \times 2/3 { c'4 c'4 c'4 }")

        >>> leaves = abjad.select(staff).leaves()
        >>> spanner = abjad.BowContactSpanner()
        >>> abjad.attach(spanner, leaves)
        >>> spanner.attach(abjad.BowMotionTechnique('jete'), leaves[0])
        >>> spanner.attach(abjad.BowContactPoint((1, 4)), leaves[0])
        >>> spanner.attach(abjad.BowContactPoint((3, 4)), leaves[1])
        >>> spanner.attach(abjad.BowContactPoint((1, 2)), leaves[2])
        >>> spanner.attach(abjad.BowMotionTechnique('circular'),
        ...     leaves[3])
        >>> spanner.attach(abjad.BowContactPoint((1, 1)), leaves[3])
        >>> spanner.attach(abjad.BowContactPoint((0, 1)), leaves[4])

        >>> abjad.attach(abjad.Clef('percussion'), staff[0])
        >>> abjad.override(staff).bar_line.transparent = True
        >>> abjad.override(staff).dots.staff_position = -8
        >>> abjad.override(staff).flag.Y_offset = -8.5
        >>> abjad.override(staff).glissando.bound_details__left__padding = 1.5
        >>> abjad.override(staff).glissando.bound_details__right__padding = 1.5
        >>> abjad.override(staff).glissando.thickness = 2
        >>> abjad.override(staff).script.staff_padding = 3
        >>> abjad.override(staff).staff_symbol.transparent = True
        >>> abjad.override(staff).stem.direction = abjad.Down
        >>> abjad.override(staff).stem.length = 8
        >>> abjad.override(staff).stem.stem_begin_position = -9
        >>> abjad.override(staff).time_signature.stencil = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                \override BarLine.transparent = ##t
                \override Dots.staff-position = #-8
                \override Flag.Y-offset = #-8.5
                \override Glissando.bound-details.left.padding = #1.5
                \override Glissando.bound-details.right.padding = #1.5
                \override Glissando.thickness = #2
                \override Script.staff-padding = #3
                \override StaffSymbol.transparent = ##t
                \override Stem.direction = #down
                \override Stem.length = #8
                \override Stem.stem-begin-position = #-9
                \override TimeSignature.stencil = ##f
            } {
                \once \override Glissando.style = #'dotted-line
                \once \override NoteHead.Y-offset = -1.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \center-align
                        \vcenter
                            \fraction
                                1
                                4
                    }
                \clef "percussion"
                c'4. ^\downbow \glissando
                \once \override NoteHead.Y-offset = 1.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }
                c'8 ^\upbow \glissando
                \times 2/3 {
                    \once \override NoteHead.Y-offset = 0.0
                    \once \override NoteHead.stencil = #ly:text-interface::print
                    \once \override NoteHead.text = \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    2
                        }
                    c'4 ^\downbow \glissando
                    \once \override Glissando.style = #'zigzag
                    \once \override NoteHead.Y-offset = 2.0
                    \once \override NoteHead.stencil = #ly:text-interface::print
                    \once \override NoteHead.text = \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    1
                        }
                    c'4 ^\upbow \glissando
                    \once \override NoteHead.Y-offset = -2.0
                    \once \override NoteHead.stencil = #ly:text-interface::print
                    \once \override NoteHead.text = \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    0
                                    1
                        }
                    c'4
                }
            }

    ..  container:: example

        Use ``abjad.BowContactPoint(None)`` to indicate unbowed actions, such
        as pizzicato:

        >>> staff = abjad.Staff()
        >>> staff.extend(r"c'4 c'4 c'4 c'4")

        >>> leaves = abjad.select(staff).leaves()
        >>> spanner = abjad.BowContactSpanner()
        >>> abjad.attach(spanner, leaves)
        >>> spanner.attach(abjad.BowContactPoint(None), leaves[0])
        >>> spanner.attach(abjad.BowContactPoint((3, 4)), leaves[1])
        >>> spanner.attach(abjad.BowContactPoint((1, 2)), leaves[2])
        >>> spanner.attach(abjad.BowContactPoint(None), leaves[3])

        >>> abjad.attach(abjad.Clef('percussion'), staff[0])
        >>> abjad.override(staff).bar_line.transparent = True
        >>> abjad.override(staff).dots.staff_position = -8
        >>> abjad.override(staff).flag.Y_offset = -8.5
        >>> abjad.override(staff).glissando.bound_details__left__padding = 1.5
        >>> abjad.override(staff).glissando.bound_details__right__padding = 1.5
        >>> abjad.override(staff).glissando.thickness = 2
        >>> abjad.override(staff).script.staff_padding = 3
        >>> abjad.override(staff).staff_symbol.transparent = True
        >>> abjad.override(staff).stem.direction = abjad.Down
        >>> abjad.override(staff).stem.length = 8
        >>> abjad.override(staff).stem.stem_begin_position = -9
        >>> abjad.override(staff).time_signature.stencil = False
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff \with {
                \override BarLine.transparent = ##t
                \override Dots.staff-position = #-8
                \override Flag.Y-offset = #-8.5
                \override Glissando.bound-details.left.padding = #1.5
                \override Glissando.bound-details.right.padding = #1.5
                \override Glissando.thickness = #2
                \override Script.staff-padding = #3
                \override StaffSymbol.transparent = ##t
                \override Stem.direction = #down
                \override Stem.length = #8
                \override Stem.stem-begin-position = #-9
                \override TimeSignature.stencil = ##f
            } {
                \once \override NoteHead.style = #'cross
                \clef "percussion"
                c'4
                \once \override NoteHead.Y-offset = 1.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }
                c'4 ^\upbow \glissando
                \once \override NoteHead.Y-offset = 0.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \center-align
                        \vcenter
                            \fraction
                                1
                                2
                    }
                c'4
                \once \override NoteHead.style = #'cross
                c'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, overrides=None):
        Spanner.__init__(self, overrides=overrides)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        indicators = self._get_piecewise(leaf)
        bow_contact_point = indicators[0]
        bow_motion_technique = indicators[1]
        if bow_contact_point is None:
            return bundle
        if bow_contact_point.contact_point is None:
            self._make_pizzicato_overrides(bundle)
            return bundle
        if self._is_my_only_leaf(leaf):
            return bundle
        self._make_bow_contact_point_overrides(
            bow_contact_point=bow_contact_point,
            bundle=bundle,
            )
        if self._next_leaf_is_bowed(leaf):
            bundle.right.spanner_starts.append(r'\glissando')
            self._make_bow_direction_change_contributions(
                bow_contact_point=bow_contact_point,
                leaf=leaf,
                bundle=bundle,
                )
            self._make_glissando_overrides(
                bow_motion_technique=bow_motion_technique,
                bundle=bundle,
                )
        return bundle

    def _get_piecewise(self, leaf):
        import abjad
        bow_contact_point = abjad.inspect(leaf).get_indicator(
            abjad.BowContactPoint,
            None,
            )
        bow_motion_technique = abjad.inspect(leaf).get_indicator(
            abjad.BowMotionTechnique,
            None,
            )
        return (
            bow_contact_point,
            bow_motion_technique,
            )

    def _make_bow_contact_point_overrides(
        self,
        bow_contact_point=None,
        bundle=None,
        ):
        import abjad
        if bow_contact_point is None:
            return
        override_ = abjad.LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='stencil',
            value=abjad.Scheme('ly:text-interface::print'),
            )
        string = override_.override_string
        bundle.grob_overrides.append(string)
        override_ = abjad.LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='text',
            value=bow_contact_point.markup,
            )
        string = override_.override_string
        bundle.grob_overrides.append(string)
        y_offset = float((4 * bow_contact_point.contact_point) - 2)
        override_ = abjad.LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='Y-offset',
            value=y_offset,
            )
        string = override_.override_string
        bundle.grob_overrides.append(string)

    def _make_bow_direction_change_contributions(
        self,
        bow_contact_point=None,
        leaf=None,
        bundle=None,
        ):
        import abjad
        cautionary_change = False
        direction_change = None
        next_leaf = abjad.inspect(leaf).get_leaf(1)
        this_contact_point = bow_contact_point
        if this_contact_point is None:
            return
        next_contact_point = abjad.inspect(next_leaf).get_indicator(
            abjad.BowContactPoint)
        if next_contact_point is None:
            return
        previous_leaf = abjad.inspect(leaf).get_leaf(-1)
        previous_contact_point = None
        if previous_leaf is not None:
            agent = abjad.inspect(previous_leaf)
            previous_contact_points = agent.get_indicators(
                abjad.BowContactPoint
                )
            if previous_contact_points:
                previous_contact_point = previous_contact_points[0]
        if (self._is_my_first_leaf(leaf) or
            previous_contact_point is None or
            previous_contact_point.contact_point is None
            ):
            if this_contact_point < next_contact_point:
                direction_change = abjad.Down
            elif next_contact_point < this_contact_point:
                direction_change = abjad.Up
        else:
            previous_leaf = abjad.inspect(leaf).get_leaf(-1)
            agent = abjad.inspect(previous_leaf)
            previous_contact_point = agent.get_indicator(abjad.BowContactPoint)
            if (previous_contact_point < this_contact_point and
                next_contact_point < this_contact_point):
                direction_change = abjad.Up
            elif (this_contact_point < previous_contact_point and
                this_contact_point < next_contact_point):
                direction_change = abjad.Down
            elif (this_contact_point == previous_contact_point):
                if this_contact_point < next_contact_point:
                    cautionary_change = True
                    direction_change = abjad.Down
                elif next_contact_point < this_contact_point:
                    cautionary_change = True
                    direction_change = abjad.Up
        if direction_change is None:
            return
        if cautionary_change:
            if direction_change == abjad.Up:
                string = r'^ \parenthesize \upbow'
            elif direction_change == abjad.Down:
                string = r'^ \parenthesize \downbow'
        else:
            if direction_change == abjad.Up:
                articulation = abjad.Articulation('upbow', abjad.Up)
            elif direction_change == abjad.Down:
                articulation = abjad.Articulation('downbow', abjad.Up)
            string = str(articulation)
        bundle.right.articulations.append(string)

    def _make_glissando_overrides(
        self,
        bow_motion_technique=None,
        bundle=None,
        ):
        import abjad
        if bow_motion_technique is not None:
            style = abjad.SchemeSymbol(bow_motion_technique.glissando_style)
            override_ = abjad.LilyPondGrobOverride(
                grob_name='Glissando',
                once=True,
                property_path='style',
                value=style,
                )
            string = override_.override_string
            bundle.grob_overrides.append(string)

    def _make_pizzicato_overrides(
        self,
        bundle=None,
        ):
        import abjad
        style = abjad.SchemeSymbol('cross')
        override_ = abjad.LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='style',
            value=style,
            )
        string = override_.override_string
        bundle.grob_overrides.append(string)

    def _next_leaf_is_bowed(self, leaf):
        import abjad
        if self._is_my_last_leaf(leaf):
            return False
        prototype = (
            abjad.MultimeasureRest,
            abjad.Rest,
            abjad.Skip,
            )
        next_leaf = abjad.inspect(leaf).get_leaf(1)
        if next_leaf is None or isinstance(next_leaf, prototype):
            return False
        next_contact_point = abjad.inspect(next_leaf).get_indicator(
            abjad.BowContactPoint)
        if next_contact_point is None:
            return False
        elif next_contact_point.contact_point is None:
            return False
        return True

    ### PUBLIC METHODS ###

    def attach(self, indicator, leaf):
        r'''Attaches `indicator` to `leaf` in spanner.

        Returns none.
        '''
        superclass = super(BowContactSpanner, self)
        superclass._attach_piecewise(indicator, leaf)
