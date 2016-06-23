# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_


class BowContactSpanner(Spanner):
    r'''Bow contact spanner.

    ..  container:: example

        ::

            >>> staff = Staff()
            >>> staff.extend(r"c'4. c'8 \times 2/3 { c'4 c'4 c'4 }")

        ::

            >>> selector = select().by_leaf(flatten=True)
            >>> leaves = selector(staff)
            >>> attach(indicatortools.BowMotionTechnique('jete'), leaves[0])
            >>> attach(indicatortools.BowContactPoint((1, 4)), leaves[0])
            >>> attach(indicatortools.BowContactPoint((3, 4)), leaves[1])
            >>> attach(indicatortools.BowContactPoint((1, 2)), leaves[2])
            >>> attach(indicatortools.BowMotionTechnique('circular'),
            ...     leaves[3])
            >>> attach(indicatortools.BowContactPoint((1, 1)), leaves[3])
            >>> attach(indicatortools.BowContactPoint((0, 1)), leaves[4])

        ::

            >>> attach(Clef('percussion'), staff)
            >>> override(staff).bar_line.transparent = True
            >>> override(staff).dots.staff_position = -8
            >>> override(staff).flag.Y_offset = -8.5
            >>> override(staff).glissando.bound_details__left__padding = 1.5
            >>> override(staff).glissando.bound_details__right__padding = 1.5
            >>> override(staff).glissando.thickness = 2
            >>> override(staff).script.staff_padding = 3
            >>> override(staff).staff_symbol.transparent = True
            >>> override(staff).stem.direction = Down
            >>> override(staff).stem.length = 8
            >>> override(staff).stem.stem_begin_position = -9
            >>> override(staff).time_signature.stencil = False

        ::

            >>> attach(spannertools.BowContactSpanner(), leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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
                \clef "percussion"
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

        Use ``BowContactPoint(None)`` to indicate un-bowed actions, such as
        pizzicato.

        ::

            >>> staff = Staff()
            >>> staff.extend(r"c'4 c'4 c'4 c'4")

        ::

            >>> leaves = staff[:]
            >>> attach(indicatortools.BowContactPoint(None), leaves[0])
            >>> attach(indicatortools.BowContactPoint((3, 4)), leaves[1])
            >>> attach(indicatortools.BowContactPoint((1, 2)), leaves[2])
            >>> attach(indicatortools.BowContactPoint(None), leaves[3])

        ::

            >>> attach(Clef('percussion'), staff)
            >>> override(staff).bar_line.transparent = True
            >>> override(staff).dots.staff_position = -8
            >>> override(staff).flag.Y_offset = -8.5
            >>> override(staff).glissando.bound_details__left__padding = 1.5
            >>> override(staff).glissando.bound_details__right__padding = 1.5
            >>> override(staff).glissando.thickness = 2
            >>> override(staff).script.staff_padding = 3
            >>> override(staff).staff_symbol.transparent = True
            >>> override(staff).stem.direction = Down
            >>> override(staff).stem.length = 8
            >>> override(staff).stem.stem_begin_position = -9
            >>> override(staff).time_signature.stencil = False

        ::

            >>> attach(spannertools.BowContactSpanner(), leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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
                \clef "percussion"
                \once \override NoteHead.style = #'cross
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

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, overrides=None):
        Spanner.__init__(self, overrides=overrides)

    ### PRIVATE METHODS ###

    def _get_annotations(self, leaf):
        inspector = inspect_(leaf)
        bow_contact_point = None
        prototype = indicatortools.BowContactPoint
        if inspector.has_indicator(prototype):
            bow_contact_point = inspector.get_indicator(prototype)
        bow_motion_technique = None
        prototype = indicatortools.BowMotionTechnique
        if inspector.has_indicator(prototype):
            bow_motion_technique = inspector.get_indicator(prototype)
        return (
            bow_contact_point,
            bow_motion_technique,
            )

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        indicators = self._get_annotations(leaf)
        bow_contact_point = indicators[0]
        bow_motion_technique = indicators[1]
        #print(leaf)
        if bow_contact_point is None:
            #print('\t', None)
            return lilypond_format_bundle
        if bow_contact_point.contact_point is None:
            #print('\t', 'PIZZ')
            self._make_pizzicato_overrides(lilypond_format_bundle)
            return lilypond_format_bundle
        if self._is_my_only_leaf(leaf):
            #print('\t', 'ONLY')
            return lilypond_format_bundle
        #print('\t', 'NORM')
        self._make_bow_contact_point_overrides(
            bow_contact_point=bow_contact_point,
            lilypond_format_bundle=lilypond_format_bundle,
            )
        if self._next_leaf_is_bowed(leaf):
            lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
            self._make_bow_direction_change_contributions(
                bow_contact_point=bow_contact_point,
                leaf=leaf,
                lilypond_format_bundle=lilypond_format_bundle,
                )
            self._make_glissando_overrides(
                bow_motion_technique=bow_motion_technique,
                lilypond_format_bundle=lilypond_format_bundle,
                )
        return lilypond_format_bundle

    def _make_bow_contact_point_overrides(
        self,
        bow_contact_point=None,
        lilypond_format_bundle=None,
        ):
        if bow_contact_point is None:
            return
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='stencil',
            value=schemetools.Scheme('ly:text-interface::print'),
            )
        string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(string)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='text',
            value=bow_contact_point.markup,
            )
        string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(string)
        y_offset = float((4 * bow_contact_point.contact_point) - 2)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='Y-offset',
            value=y_offset,
            )
        string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(string)

    def _make_bow_direction_change_contributions(
        self,
        bow_contact_point=None,
        leaf=None,
        lilypond_format_bundle=None,
        ):
        cautionary_change = False
        direction_change = None
        next_leaf = inspect_(leaf).get_leaf(1)
        this_contact_point = bow_contact_point
        if this_contact_point is None:
            return
        next_contact_point = inspect_(next_leaf).get_indicator(
            indicatortools.BowContactPoint)
        if next_contact_point is None:
            return
        previous_leaf = inspect_(leaf).get_leaf(-1)
        previous_contact_point = None
        if previous_leaf is not None:
            previous_contact_points = inspect_(previous_leaf
                ).get_indicators(indicatortools.BowContactPoint)
            if previous_contact_points:
                previous_contact_point = previous_contact_points[0]
        if self._is_my_first_leaf(leaf) or \
            previous_contact_point is None or \
            previous_contact_point.contact_point is None:
            if this_contact_point < next_contact_point:
                direction_change = Down
            elif next_contact_point < this_contact_point:
                direction_change = Up
        else:
            previous_leaf = inspect_(leaf).get_leaf(-1)
            previous_contact_point = inspect_(previous_leaf
                ).get_indicator(indicatortools.BowContactPoint)
            if (previous_contact_point < this_contact_point and
                next_contact_point < this_contact_point):
                direction_change = Up
            elif (this_contact_point < previous_contact_point and
                this_contact_point < next_contact_point):
                direction_change = Down
            elif (this_contact_point == previous_contact_point):
                if this_contact_point < next_contact_point:
                    cautionary_change = True
                    direction_change = Down
                elif next_contact_point < this_contact_point:
                    cautionary_change = True
                    direction_change = Up
        if direction_change is None:
            return
        if cautionary_change:
            if direction_change == Up:
                string = r'^ \parenthesize \upbow'
            elif direction_change == Down:
                string = r'^ \parenthesize \downbow'
        else:
            if direction_change == Up:
                articulation = indicatortools.Articulation('upbow', Up)
            elif direction_change == Down:
                articulation = indicatortools.Articulation('downbow', Up)
            string = str(articulation)
        lilypond_format_bundle.right.articulations.append(string)

    def _make_glissando_overrides(
        self,
        bow_motion_technique=None,
        lilypond_format_bundle=None,
        ):
        if bow_motion_technique is not None:
            style = schemetools.SchemeSymbol(
                bow_motion_technique.glissando_style,
                )
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='Glissando',
                is_once=True,
                property_path='style',
                value=style,
                )
            string = override_.override_string
            lilypond_format_bundle.grob_overrides.append(string)

    def _make_pizzicato_overrides(
        self,
        lilypond_format_bundle=None,
        ):
        style = schemetools.SchemeSymbol('cross')
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='style',
            value=style,
            )
        string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(string)

    def _next_leaf_is_bowed(self, leaf):
        if self._is_my_last_leaf(leaf):
            return False
        prototype = (
            scoretools.MultimeasureRest,
            scoretools.Rest,
            scoretools.Skip,
            )
        next_leaf = inspect_(leaf).get_leaf(1)
        if next_leaf is None or isinstance(next_leaf, prototype):
            return False
        next_contact_point = inspect_(next_leaf).get_indicator(
            indicatortools.BowContactPoint)
        if next_contact_point is None:
            return False
        elif next_contact_point.contact_point is None:
            return False
        return True