import typing
from abjad import enums
from abjad.core.Leaf import Leaf
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Rest import Rest
from abjad.core.Skip import Skip
from abjad.indicators.Articulation import Articulation
from abjad.indicators.BowContactPoint import BowContactPoint
from abjad.indicators.BowMotionTechnique import BowMotionTechnique
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.scheme import Scheme
from abjad.scheme import SchemeSymbol
from abjad.system.Tag import Tag
from abjad.system.Wrapper import Wrapper
from abjad.top.inspect import inspect
from .Spanner import Spanner


class BowContactSpanner(Spanner):
    r"""
    Bow contact spanner.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> staff.extend(r"c'4. c'8 \times 2/3 { c'4 c'4 c'4 }")

        >>> leaves = abjad.select(staff).leaves()
        >>> abjad.attach(abjad.BowMotionTechnique('jete'), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((1, 4)), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((3, 4)), leaves[1])
        >>> abjad.attach(abjad.BowContactPoint((1, 2)), leaves[2])
        >>> abjad.attach(abjad.BowMotionTechnique('circular'), leaves[3])
        >>> abjad.attach(abjad.BowContactPoint((1, 1)), leaves[3])
        >>> abjad.attach(abjad.BowContactPoint((0, 1)), leaves[4])

        >>> abjad.attach(abjad.Clef('percussion'), leaves[0])
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

        >>> abjad.attach(abjad.BowContactSpanner(), leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
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
            }
            {
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
                c'4.
                ^\downbow
                \glissando
                \once \override NoteHead.Y-offset = 1.0
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }
                c'8
                ^\upbow
                \glissando
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
                    c'4
                    ^\downbow
                    \glissando
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
                    c'4
                    ^\upbow
                    \glissando
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

        >>> staff = abjad.Staff(r"c'4 c'4 c'4 c'4")

        >>> leaves = staff[:]
        >>> abjad.attach(abjad.BowContactPoint(None), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((3, 4)), leaves[1])
        >>> abjad.attach(abjad.BowContactPoint((1, 2)), leaves[2])
        >>> abjad.attach(abjad.BowContactPoint(None), leaves[3])

        >>> abjad.attach(abjad.Clef('percussion'), staff[0])
        >>> abjad.override(staff).bar_line.transparent = True
        >>> abjad.override(staff).dots.staff_position = -8
        >>> abjad.override(staff).flag.Y_offset = -8.5
        >>> abjad.override(staff).glissando.bound_details__left__padding = 1.5
        >>> abjad.override(staff).glissando.bound_details__right__padding = 1.5
        >>> abjad.override(staff).glissando.thickness = 2
        >>> abjad.override(staff).script.staff_padding = 3
        >>> abjad.override(staff).staff_symbol.transparent = True
        >>> abjad.override(staff).stem.direction =abjad.Down
        >>> abjad.override(staff).stem.length = 8
        >>> abjad.override(staff).stem.stem_begin_position = -9
        >>> abjad.override(staff).time_signature.stencil = False

        >>> abjad.abjad.attach(abjad.BowContactSpanner(), leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
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
            }
            {
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
                c'4
                ^\upbow
                \glissando
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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _get_annotations(self, leaf):
        inspector = inspect(leaf)
        bow_contact_point = None
        prototype = BowContactPoint
        if inspector.has_indicator(prototype):
            bow_contact_point = inspector.indicator(prototype)
        bow_motion_technique = None
        prototype = BowMotionTechnique
        if inspector.has_indicator(prototype):
            bow_motion_technique = inspector.indicator(prototype)
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
        if len(self) == 1:
            #print('\t', 'ONLY')
            return lilypond_format_bundle
        #print('\t', 'NORM')
        self._make_bow_contact_point_overrides(
            bow_contact_point=bow_contact_point,
            lilypond_format_bundle=lilypond_format_bundle,
            )
        if self._next_leaf_is_bowed(leaf):
            lilypond_format_bundle.after.spanner_starts.append(r'\glissando')
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
        override_ = LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='stencil',
            value=Scheme('ly:text-interface::print'),
            )
        string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(string)
        override_ = LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='text',
            value=bow_contact_point.markup,
            )
        string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(string)
        y_offset = float((4 * bow_contact_point.contact_point) - 2)
        override_ = LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
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
        next_leaf = inspect(leaf).leaf(1)
        this_contact_point = bow_contact_point
        if this_contact_point is None:
            return
        next_contact_point = inspect(next_leaf).indicator(BowContactPoint)
        if next_contact_point is None:
            return
        previous_leaf = inspect(leaf).leaf(-1)
        previous_contact_point = None
        if previous_leaf is not None:
            previous_contact_points = inspect(previous_leaf
                ).indicators(BowContactPoint)
            if previous_contact_points:
                previous_contact_point = previous_contact_points[0]
        if (leaf is self[0] or
            previous_contact_point is None or
            previous_contact_point.contact_point is None
            ):
            if this_contact_point < next_contact_point:
                direction_change = enums.Down
            elif next_contact_point < this_contact_point:
                direction_change = enums.Up
        else:
            previous_leaf = inspect(leaf).leaf(-1)
            previous_contact_point = inspect(previous_leaf).indicator(
                BowContactPoint)
            if (previous_contact_point < this_contact_point and
                next_contact_point < this_contact_point):
                direction_change = enums.Up
            elif (this_contact_point < previous_contact_point and
                this_contact_point < next_contact_point):
                direction_change = enums.Down
            elif (this_contact_point == previous_contact_point):
                if this_contact_point < next_contact_point:
                    cautionary_change = True
                    direction_change = enums.Down
                elif next_contact_point < this_contact_point:
                    cautionary_change = True
                    direction_change = enums.Up
        if direction_change is None:
            return
        if cautionary_change:
            if direction_change == enums.Up:
                string = r'^ \parenthesize \upbow'
            elif direction_change == enums.Down:
                string = r'^ \parenthesize \downbow'
        else:
            if direction_change == enums.Up:
                articulation = Articulation('upbow', direction=enums.Up)
            elif direction_change == enums.Down:
                articulation = Articulation('downbow', direction=enums.Up)
            string = str(articulation)
        lilypond_format_bundle.after.articulations.append(string)

    def _make_glissando_overrides(
        self,
        bow_motion_technique=None,
        lilypond_format_bundle=None,
        ):
        if bow_motion_technique is not None:
            style = SchemeSymbol(bow_motion_technique.glissando_style)
            override_ = LilyPondGrobOverride(
                grob_name='Glissando',
                once=True,
                property_path='style',
                value=style,
                )
            string = override_.override_string
            lilypond_format_bundle.grob_overrides.append(string)

    def _make_pizzicato_overrides(
        self,
        lilypond_format_bundle=None,
        ):
        style = SchemeSymbol('cross')
        override_ = LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='style',
            value=style,
            )
        string = override_.override_string
        lilypond_format_bundle.grob_overrides.append(string)

    def _next_leaf_is_bowed(self, leaf):
        if leaf is self[-1]:
            return False
        prototype = (
            MultimeasureRest,
            Rest,
            Skip,
            )
        next_leaf = inspect(leaf).leaf(1)
        if next_leaf is None or isinstance(next_leaf, prototype):
            return False
        next_contact_point = inspect(next_leaf).indicator(BowContactPoint)
        if next_contact_point is None:
            return False
        elif next_contact_point.contact_point is None:
            return False
        return True
