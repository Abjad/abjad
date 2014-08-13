# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import schemetools
from abjad.tools import spannertools
from abjad.tools.topleveltools import inspect_


class BowSpanner(spannertools.Spanner):
    r'''Bow spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 c'4 c'4 c'4")

        ::

            >>> attach(indicatortools.BowContactPoint((1, 4)), staff[0])
            >>> attach(indicatortools.BowContactPoint((3, 4)), staff[1])
            >>> attach(indicatortools.BowContactPoint((1, 2)), staff[2])
            >>> attach(indicatortools.BowContactPoint((1, 1)), staff[3])

        ::

            >>> from experimental import newspannertools
            >>> attach(newspannertools.BowSpanner(), staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \once \override NoteHead.Y-offset = -1.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \vcenter
                        \fraction
                            1
                            4
                    }
                c'4 ^\upbow \glissando
                \once \override NoteHead.Y-offset = 1.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \vcenter
                        \fraction
                            3
                            4
                    }
                c'4 ^\downbow \glissando
                \once \override NoteHead.Y-offset = 0.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \vcenter
                        \fraction
                            1
                            2
                    }
                c'4 ^\upbow \glissando
                \once \override NoteHead.Y-offset = 2.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \vcenter
                        \fraction
                            1
                            1
                    }
                c'4
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
        spannertools.Spanner.__init__(
            self,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _get_bowing_indicators(self, leaf):
        inspector = inspect_(leaf)
        bow_contact_point = None
        prototype = indicatortools.BowContactPoint
        if inspector.has_indicator(prototype):
            bow_contact_point = inspector.get_indicator(prototype)
        bow_pressure = None
        prototype = indicatortools.BowPressure
        if inspector.has_indicator(prototype):
            bow_pressure = inspector.get_indicator(prototype)
        bow_technique = None
        #prototype = indicatortools.BowTechnique
        #if inspector.has_indicator(prototype):
        #    bow_technique = inspector.get_indicator(prototype)
        string_contact_point = None
        prototype = indicatortools.StringContactPoint
        if inspector.has_indicator(prototype):
            string_contact_point = inspector.get_indicator(prototype)
        return (
            bow_contact_point,
            bow_pressure,
            bow_technique,
            string_contact_point,
            )

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        indicators = self._get_bowing_indicators(leaf)
        bow_contact_point = indicators[0]
        bow_pressure = indicators[1]
        bow_technique = indicators[2]
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
                bow_technique=bow_technique,
                lilypond_format_bundle=lilypond_format_bundle,
                string_contact_point=string_contact_point,
                )
        return lilypond_format_bundle

    def _make_bow_direction_change_contributions(
        self,
        bow_contact_point=None,
        leaf=None,
        lilypond_format_bundle=None,
        ):
        direction_change = None
        next_leaf = inspect_(leaf).get_leaf(1)
        this_contact_point = bow_contact_point
        next_contact_point = inspect_(next_leaf).get_indicator(
            indicatortools.BowContactPoint)
        if self._is_my_first_leaf(leaf):
            if this_contact_point < next_contact_point:
                direction_change = Up
            elif next_contact_point < this_contact_point:
                direction_change = Down
        else:
            previous_leaf = inspect_(leaf).get_leaf(-1)
            previous_contact_point = inspect_(previous_leaf
                ).get_indicator(indicatortools.BowContactPoint)
            if previous_contact_point < this_contact_point and \
                next_contact_point < this_contact_point:
                direction_change = Down
            elif this_contact_point < previous_contact_point and \
                this_contact_point < next_contact_point:
                direction_change = Up
        if direction_change is None:
            return
        if direction_change is Up:
            articulation = indicatortools.Articulation('upbow', Up)
        elif direction_change is Down:
            articulation = indicatortools.Articulation('downbow', Up)
        lilypond_format_bundle.right.articulations.append(str(articulation))

    def _make_bow_contact_point_overrides(
        self,
        lilypond_format_bundle=None,
        bow_contact_point=None,
        ):
        stencil_override = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='stencil',
            value=schemetools.Scheme('ly:text-interface::print'),
            )
        stencil_override_string = '\n'.join(
            stencil_override.override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(stencil_override_string)
        text_override = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='text',
            value=bow_contact_point.markup,
            )
        text_override_string = '\n'.join(text_override.override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(text_override_string)
        y_offset = float((4 * bow_contact_point.contact_point) - 2)
        y_offset_override = lilypondnametools.LilyPondGrobOverride(
            grob_name='NoteHead',
            is_once=True,
            property_path='Y-offset',
            value=y_offset,
            )
        y_offset_override_string = '\n'.join(
            y_offset_override.override_format_pieces)
        lilypond_format_bundle.grob_overrides.append(y_offset_override_string)

    def _make_glissando_overrides(
        self,
        bow_pressure=None,
        bow_technique=None,
        lilypond_format_bundle=None,
        string_contact_point=None,
        ):
        pass