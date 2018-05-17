import typing
from abjad.enumerations import Down
from abjad.enumerations import Up
from abjad.tools.indicatortools.Articulation import Articulation
from abjad.tools.indicatortools.BowContactPoint import BowContactPoint
from abjad.tools.indicatortools.BowMotionTechnique import BowMotionTechnique
from abjad.tools.lilypondnametools.LilyPondGrobOverride import (
    LilyPondGrobOverride,
)
from abjad.tools.schemetools.Scheme import Scheme
from abjad.tools.schemetools.SchemeSymbol import SchemeSymbol
from abjad.tools.scoretools.Leaf import Leaf
from abjad.tools.scoretools.MultimeasureRest import MultimeasureRest
from abjad.tools.scoretools.Rest import Rest
from abjad.tools.scoretools.Skip import Skip
from abjad.tools.systemtools.Tag import Tag
from abjad.tools.systemtools.Wrapper import Wrapper
from abjad.tools.topleveltools.inspect import inspect
from .Spanner import Spanner



class BowContactSpanner(Spanner):
    r"""
    Bow contact spanner.

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
                \clef "percussion"
                \tweak Y-offset #-1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                1
                                4
                    }
                c'4.
                ^\downbow
                - \tweak style #'dotted-line
                \glissando
                \tweak Y-offset #1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
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
                    \tweak Y-offset #0.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    2
                        }
                    c'4
                    ^\downbow
                    \glissando
                    \tweak Y-offset #2.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    1
                        }
                    c'4
                    ^\upbow
                    - \tweak style #'zigzag
                    \glissando
                    \tweak Y-offset #-2.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
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
                \tweak Y-offset #1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }
                c'4
                ^\upbow
                \glissando
                \tweak Y-offset #0.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
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

    __slots__ = ()

    _start_command = r'\glissando'

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
        if self._is_my_only(leaf):
            return bundle
        tweaks = self._make_bow_contact_point_tweaks(
            leaf,
            bow_contact_point=bow_contact_point,
            )
        if self._next_leaf_is_bowed(leaf):
            self._make_bow_direction_change_contributions(
                bow_contact_point=bow_contact_point,
                leaf=leaf,
                bundle=bundle,
                )
            # tweaks immediately before start command:
            tweaks = self._make_glissando_tweaks(
                bow_motion_technique=bow_motion_technique,
                )
            bundle.right.spanner_starts.extend(tweaks)
            bundle.right.spanner_starts.extend(self.start_command())
        return bundle

    def _get_piecewise(self, leaf):
        bow_contact_point = inspect(leaf).get_indicator(BowContactPoint, None)
        bow_motion_technique = inspect(leaf).get_indicator(
            BowMotionTechnique,
            None,
            )
        return (
            bow_contact_point,
            bow_motion_technique,
            )

    def _make_bow_contact_point_tweaks(
        self,
        leaf,
        bow_contact_point=None,
        ):
        import abjad
        if bow_contact_point is None:
            return tweaks
        note_head = leaf.note_head
        value = Scheme('ly:text-interface::print')
        abjad.tweak(note_head).stencil = value
        abjad.tweak(note_head).text = bow_contact_point.markup
        y_offset = float((4 * bow_contact_point.contact_point) - 2)
        abjad.tweak(note_head).Y_offset = y_offset

    def _make_bow_direction_change_contributions(
        self,
        bow_contact_point=None,
        leaf=None,
        bundle=None,
        ):
        cautionary_change = False
        direction_change = None
        next_leaf = inspect(leaf).get_leaf(1)
        this_contact_point = bow_contact_point
        if this_contact_point is None:
            return
        next_contact_point = inspect(next_leaf).get_indicator(BowContactPoint)
        if next_contact_point is None:
            return
        previous_leaf = inspect(leaf).get_leaf(-1)
        previous_contact_point = None
        if previous_leaf is not None:
            agent = inspect(previous_leaf)
            previous_contact_points = agent.get_indicators(BowContactPoint)
            if previous_contact_points:
                previous_contact_point = previous_contact_points[0]
        if (leaf is self[0] or
            previous_contact_point is None or
            previous_contact_point.contact_point is None):
            if this_contact_point < next_contact_point:
                direction_change = Down
            elif next_contact_point < this_contact_point:
                direction_change = Up
        else:
            previous_leaf = inspect(leaf).get_leaf(-1)
            agent = inspect(previous_leaf)
            previous_contact_point = agent.get_indicator(BowContactPoint)
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
            if direction_change is Up:
                string = r'^ \parenthesize \upbow'
            elif direction_change is Down:
                string = r'^ \parenthesize \downbow'
        else:
            if direction_change is Up:
                articulation = Articulation('upbow', direction=Up)
            elif direction_change is Down:
                articulation = Articulation('downbow', direction=Up)
            string = str(articulation)
        bundle.right.articulations.append(string)

    def _make_glissando_tweaks(
        self,
        bow_motion_technique=None,
        ):
        tweaks = []
        if bow_motion_technique is not None:
            style = SchemeSymbol(bow_motion_technique.glissando_style)
            override = LilyPondGrobOverride(
                grob_name='Glissando',
                once=True,
                property_path='style',
                value=style,
                )
            string = override.tweak_string()
            tweaks.append(string)
        return tweaks

    def _make_pizzicato_overrides(
        self,
        bundle=None,
        ):
        style = SchemeSymbol('cross')
        override_ = LilyPondGrobOverride(
            grob_name='NoteHead',
            once=True,
            property_path='style',
            value=style,
            )
        string = override_.override_string
        bundle.grob_overrides.append(string)

    def _next_leaf_is_bowed(self, leaf):
        if leaf is self[-1]:
            return False
        prototype = (
            MultimeasureRest,
            Rest,
            Skip,
            )
        next_leaf = inspect(leaf).get_leaf(1)
        if next_leaf is None or isinstance(next_leaf, prototype):
            return False
        next_contact_point = inspect(next_leaf).get_indicator(BowContactPoint)
        if next_contact_point is None:
            return False
        elif next_contact_point.contact_point is None:
            return False
        return True

    ### PUBLIC METHODS ###

    def attach(
        self,
        indicator: typing.Union[BowContactPoint, BowMotionTechnique],
        leaf: Leaf,
        deactivate: bool = None,
        tag: typing.Union[str, Tag] = None,
        wrapper: bool = None,
        ) -> typing.Optional[Wrapper]:
        """
        Attaches ``indicator`` to ``leaf`` in spanner.
        """
        return super(BowContactSpanner, self)._attach_piecewise(
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

            >>> abjad.BowContactSpanner().start_command()
            ['\\glissando']

        """
        return super(BowContactSpanner, self).start_command()

    def stop_command(self) -> typing.Optional[str]:
        """
        Gets stop command.

        ..  container:: example

            >>> abjad.BowContactSpanner().stop_command() is None
            True

        """
        return super(BowContactSpanner, self).stop_command()
