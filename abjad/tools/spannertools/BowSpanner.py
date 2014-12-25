# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import schemetools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_


class BowSpanner(Spanner):
    r'''Bow spanner.

    ..  container:: example

        ::

            >>> staff = Staff()
            >>> staff.extend(r"c'4. c'8 \times 2/3 { c'4 c'4 c'4 }")

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

            >>> leaves = staff.select_leaves()
            >>> attach(indicatortools.BowMotionTechnique('jete'), leaves[0])
            >>> attach(indicatortools.BowContactPoint((1, 4)), leaves[0])
            >>> attach(indicatortools.BowContactPoint((3, 4)), leaves[1])
            >>> attach(indicatortools.BowContactPoint((1, 2)), leaves[2])
            >>> attach(indicatortools.BowMotionTechnique('circular'),
            ...     leaves[3])
            >>> attach(indicatortools.BowContactPoint((1, 1)), leaves[3])
            >>> attach(indicatortools.BowContactPoint((0, 1)), leaves[4])

        ::

            >>> attach(spannertools.BowSpanner(), leaves)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff \with {
                \override BarLine #'transparent = ##t
                \override Dots #'staff-position = #-8
                \override Flag #'Y-offset = #-8.5
                \override Glissando #'bound-details #'left #'padding = #1.5
                \override Glissando #'bound-details #'right #'padding = #1.5
                \override Glissando #'thickness = #2
                \override Script #'staff-padding = #3
                \override StaffSymbol #'transparent = ##t
                \override Stem #'direction = #down
                \override Stem #'length = #8
                \override Stem #'stem-begin-position = #-9
                \override TimeSignature #'stencil = ##f
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _get_annotations(self, leaf):
        inspector = inspect_(leaf)
        bow_contact_point = None
        prototype = indicatortools.BowContactPoint
        if inspector.has_indicator(prototype):
            bow_contact_point = inspector.get_indicator(prototype)
        bow_pressure = None
        prototype = indicatortools.BowPressure
        if inspector.has_indicator(prototype):
            bow_pressure = inspector.get_indicator(prototype)
        bow_motion_technique = None
        prototype = indicatortools.BowMotionTechnique
        if inspector.has_indicator(prototype):
            bow_motion_technique = inspector.get_indicator(prototype)
        string_contact_point = None
        prototype = indicatortools.StringContactPoint
        if inspector.has_indicator(prototype):
            string_contact_point = inspector.get_indicator(prototype)
        return (
            bow_contact_point,
            bow_pressure,
            bow_motion_technique,
            string_contact_point,
            )

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        indicators = self._get_annotations(leaf)
        bow_contact_point = indicators[0]
        bow_pressure = indicators[1]
        bow_motion_technique = indicators[2]
        string_contact_point = indicators[3]
        if self._is_my_only_leaf(leaf):
            return lilypond_format_bundle
        self._make_bow_contact_point_overrides(
            bow_contact_point=bow_contact_point,
            lilypond_format_bundle=lilypond_format_bundle,
            )
        if not self._is_my_last_leaf(leaf):
            lilypond_format_bundle.right.spanner_starts.append(r'\glissando')
            self._make_bow_direction_change_contributions(
                bow_contact_point=bow_contact_point,
                leaf=leaf,
                lilypond_format_bundle=lilypond_format_bundle,
                )
            self._make_glissando_overrides(
                bow_pressure=bow_pressure,
                bow_motion_technique=bow_motion_technique,
                lilypond_format_bundle=lilypond_format_bundle,
                string_contact_point=string_contact_point,
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
        string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(string)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='text',
            value=bow_contact_point.markup,
            )
        string = '\n'.join(override_._override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(string)
        y_offset = float((4 * bow_contact_point.contact_point) - 2)
        override_ = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='Y-offset',
            value=y_offset,
            )
        string = '\n'.join(override_._override_format_pieces)
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
        if self._is_my_first_leaf(leaf):
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
        bow_pressure=None,
        bow_motion_technique=None,
        lilypond_format_bundle=None,
        string_contact_point=None,
        ):
        if bow_motion_technique is not None:
            # TODO: should we have schemetools.SchemeSymbol?
            #       This could remove quoting="'"
            style = schemetools.Scheme(
                bow_motion_technique.glissando_style,
                quoting="'",
                )
            override_ = lilypondnametools.LilyPondGrobOverride(
                grob_name='Glissando',
                is_once=True,
                property_path='style',
                value=style,
                )
            string = '\n'.join(override_._override_format_pieces)
            lilypond_format_bundle.grob_overrides.append(string)