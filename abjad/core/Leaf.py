import abc
import copy
import typing

import uqbar.graphs

from abjad import enums, exceptions, mathtools
from abjad.indicators.MetronomeMark import MetronomeMark
from abjad.indicators.RepeatTie import RepeatTie
from abjad.indicators.Tie import Tie
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.Tag import Tag
from abjad.top.attach import attach
from abjad.top.detach import detach
from abjad.top.inspect import inspect
from abjad.top.mutate import mutate
from abjad.top.override import override
from abjad.top.select import select
from abjad.top.setting import setting
from abjad.utilities.Duration import Duration
from abjad.utilities.Multiplier import Multiplier
from abjad.utilities.Sequence import Sequence

from .Component import Component


class Leaf(Component):
    """
    Leaf baseclass.

    Leaves include notes, rests, chords and skips.
    """

    ### CLASS VARIABLES ##

    _allowable_format_slots = (
        "absolute_before",
        "before",
        "after",
        "absolute_after",
    )

    __slots__ = (
        "_after_grace_container",
        "_before_grace_container",
        "_multiplier",
        "_written_duration",
    )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, written_duration, *, multiplier=None, tag: Tag = None) -> None:
        Component.__init__(self, tag=tag)
        self._after_grace_container = None
        self._before_grace_container = None
        self.multiplier = multiplier
        self.written_duration = written_duration

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies leaf.
        """
        new = Component.__copy__(self, *arguments)
        new.multiplier = self.multiplier
        before_grace_container = self._before_grace_container
        if before_grace_container is not None:
            new_grace_container = before_grace_container._copy_with_children()
            attach(new_grace_container, new)
        after_grace_container = self._after_grace_container
        if after_grace_container is not None:
            new_after_grace_container = after_grace_container._copy_with_children()
            attach(new_after_grace_container, new)
        return new

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return (self.written_duration,)

    def __str__(self) -> str:
        """
        Gets string representation of leaf.
        """
        return self._get_compact_representation()

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        lilypond_format = self._get_compact_representation()
        lilypond_format = lilypond_format.replace("<", "&lt;")
        lilypond_format = lilypond_format.replace(">", "&gt;")
        node = Component._as_graphviz_node(self)
        node[0].extend(
            [
                uqbar.graphs.TableRow(
                    [
                        uqbar.graphs.TableCell(
                            type(self).__name__, attributes={"border": 0}
                        )
                    ]
                ),
                uqbar.graphs.HRule(),
                uqbar.graphs.TableRow(
                    [uqbar.graphs.TableCell(lilypond_format, attributes={"border": 0})]
                ),
            ]
        )
        return node

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, "_overrides", None) is not None:
            self._overrides = copy.copy(override(leaf))
        if getattr(leaf, "_lilypond_setting_name_manager", None) is not None:
            self._lilypond_setting_name_manager = copy.copy(setting(leaf))
        new_wrappers = []
        for wrapper in leaf._wrappers:
            new_wrapper = copy.copy(wrapper)
            new_wrappers.append(new_wrapper)
        for new_wrapper in new_wrappers:
            attach(new_wrapper, self)

    def _format_after_grace_body(self):
        result = []
        container = self._after_grace_container
        if container is not None:
            result.append(format(container))
        return result

    def _format_after_grace_command(self):
        result = []
        if self._after_grace_container is not None:
            result.append(r"\afterGrace")
        return result

    def _format_after_slot(self, bundle):
        result = []
        result.append(("stem_tremolos", bundle.after.stem_tremolos))
        result.append(("articulations", bundle.after.articulations))
        result.append(("markup", bundle.after.markup))
        result.append(("spanners", bundle.after.spanners))
        result.append(("spanner_stops", bundle.after.spanner_stops))
        result.append(("spanner_starts", bundle.after.spanner_starts))
        # NOTE: LilyPond demands \startTrillSpan appear after almost all
        #       other format contributions; pitched trills dangerously
        #       suppress markup and the starts of other spanners when
        #       \startTrillSpan appears lexically prior to those commands;
        #       but \startTrillSpan must appear before calls to \set.
        result.append(("trill_spanner_starts", bundle.after.trill_spanner_starts))
        result.append(("commands", bundle.after.commands))
        result.append(("commands", bundle.after.leaks))
        result.append(("after grace body", self._format_after_grace_body()))
        result.append(("comments", bundle.after.comments))
        return result

    def _format_before_slot(self, bundle):
        result = []
        result.append(("grace body", self._format_grace_body()))
        result.append(("comments", bundle.before.comments))
        result.append(("commands", bundle.before.commands))
        result.append(("indicators", bundle.before.indicators))
        result.append(("grob reverts", bundle.grob_reverts))
        result.append(("grob overrides", bundle.grob_overrides))
        result.append(("context settings", bundle.context_settings))
        result.append(("spanners", bundle.before.spanners))
        return result

    def _format_closing_slot(self, bundle):
        result = []
        result.append(("spanners", bundle.closing.spanners))
        result.append(("commands", bundle.closing.commands))
        result.append(("indicators", bundle.closing.indicators))
        result.append(("comments", bundle.closing.comments))
        return result

    def _format_contents_slot(self, bundle):
        result = []
        result.append(("leaf body", self._format_leaf_body(bundle)))
        return result

    def _format_grace_body(self):
        result = []
        container = self._before_grace_container
        if container is not None:
            result.append(format(container))
        return result

    def _format_leaf_body(self, bundle):
        result = self._format_leaf_nucleus()
        return result

    def _format_leaf_nucleus(self):
        strings = self._get_body()
        if self.tag:
            tag = Tag(self.tag)
            strings = LilyPondFormatManager.tag(strings, tag=tag)
        return strings

    def _format_opening_slot(self, bundle):
        result = []
        result.append(("comments", bundle.opening.comments))
        result.append(("indicators", bundle.opening.indicators))
        result.append(("commands", bundle.opening.commands))
        result.append(("spanners", bundle.opening.spanners))
        # IMPORTANT: LilyPond \afterGrace must appear IMMEDIATELY before leaf!
        result.append(("after grace command", self._format_after_grace_command()))
        return result

    def _get_compact_representation(self):
        return f"({self._get_formatted_duration()})"

    def _get_duration_in_seconds(self):
        mark = self._get_effective(MetronomeMark)
        if mark is not None and not mark.is_imprecise:
            result = (
                self._get_duration()
                / mark.reference_duration
                / mark.units_per_minute
                * 60
            )
            return Duration(result)
        raise exceptions.MissingMetronomeMarkError

    def _get_format_pieces(self):
        return self._get_lilypond_format().split("\n")

    def _get_format_specification(self):
        summary = self._get_compact_representation()
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[summary],
            storage_format_args_values=[format(self, "lilypond")],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
        )

    def _get_formatted_duration(self):
        strings = []
        strings.append(self.written_duration.lilypond_duration_string)
        if self.multiplier is not None:
            strings.append(str(self.multiplier))
        if hasattr(self._parent, "_leaf_multiplier"):
            multiplier = self._parent._leaf_multiplier()
            if multiplier is not None:
                strings.append(str(multiplier))
        result = " * ".join(strings)
        return result

    def _get_logical_tie(self):
        from .LogicalTie import LogicalTie

        leaves_before, leaves_after = [], []
        current_leaf = self
        while True:
            previous_leaf = inspect(current_leaf).leaf(-1)
            if previous_leaf is None:
                break
            if inspect(current_leaf).has_indicator(RepeatTie) or inspect(
                previous_leaf
            ).has_indicator(Tie):
                leaves_before.insert(0, previous_leaf)
            else:
                break
            current_leaf = previous_leaf
        current_leaf = self
        while True:
            next_leaf = inspect(current_leaf).leaf(1)
            if next_leaf is None:
                break
            if inspect(current_leaf).has_indicator(Tie) or inspect(
                next_leaf
            ).has_indicator(RepeatTie):
                leaves_after.append(next_leaf)
            else:
                break
            current_leaf = next_leaf
        leaves = leaves_before + [self] + leaves_after
        return LogicalTie(items=leaves)

    def _get_multiplied_duration(self):
        if self.written_duration:
            if self.multiplier is not None:
                duration = self.multiplier * self.written_duration
                return Duration(duration)
            return Duration(self.written_duration)

    def _get_preprolated_duration(self):
        return self._get_multiplied_duration()

    def _leaf(self, n):
        from .Container import Container
        from .OnBeatGraceContainer import OnBeatGraceContainer

        assert n in (-1, 0, 1), repr(n)
        if n == 0:
            return self
        sibling = self._sibling(n)
        if sibling is None:
            return None
        if n == 1:
            components = sibling._get_descendants_starting_with()
        else:
            assert n == -1
            if (
                isinstance(sibling, Container)
                and len(sibling) == 2
                and any(isinstance(_, OnBeatGraceContainer) for _ in sibling)
            ):
                if isinstance(sibling[0], OnBeatGraceContainer):
                    main_voice = sibling[1]
                else:
                    main_voice = sibling[0]
                return main_voice[-1]
            components = sibling._get_descendants_stopping_with()
        for component in components:
            if not isinstance(component, Leaf):
                continue
            if select([self, component]).are_logical_voice():
                return component

    def _process_contribution_packet(self, contribution_packet):
        manager = LilyPondFormatManager
        indent = manager.indent
        result = ""
        for contributor, contributions in contribution_packet:
            if contributions:
                if isinstance(contributor, tuple):
                    contributor = indent + contributor[0] + ":\n"
                else:
                    contributor = indent + contributor + ":\n"
                result += contributor
                for contribution in contributions:
                    contribution = (indent * 2) + contribution + "\n"
                    result += contribution
        return result

    def _report_format_contributions(self):
        manager = LilyPondFormatManager
        indent = manager.indent
        bundle = manager.bundle_format_contributions(self)
        report = ""
        report += 'slot "absolute before":\n'
        packet = self._format_absolute_before_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot "before":\n'
        packet = self._format_before_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot "opening":\n'
        packet = self._format_opening_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot "contents slot":\n'
        report += indent + "leaf body:\n"
        string = self._format_contents_slot(bundle)[0][1][0]
        report += (2 * indent) + string + "\n"
        report += 'slot "closing":\n'
        packet = self._format_closing_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot "after":\n'
        packet = self._format_after_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot "absolute after":\n'
        packet = self._format_absolute_after_slot(bundle)
        report += self._process_contribution_packet(packet)
        while report[-1] == "\n":
            report = report[:-1]
        return report

    def _scale(self, multiplier):
        new_duration = multiplier * self._get_duration()
        self._set_duration(new_duration)

    def _set_duration(self, new_duration):
        from .Chord import Chord
        from .Note import Note
        from .NoteMaker import NoteMaker
        from .Tuplet import Tuplet
        from abjad.spanners import tie as abjad_tie

        new_duration = Duration(new_duration)
        if self.multiplier is not None:
            multiplier = new_duration.__div__(self.written_duration)
            self.multiplier = multiplier
            return select(self)
        try:
            self.written_duration = new_duration
            return select(self)
        except exceptions.AssignabilityError:
            pass
        maker = NoteMaker()
        components = maker(0, new_duration)
        new_leaves = select(components).leaves()
        following_leaf_count = len(new_leaves) - 1
        following_leaves = following_leaf_count * self
        all_leaves = [self] + following_leaves
        for leaf, new_leaf in zip(all_leaves, new_leaves):
            leaf.written_duration = new_leaf.written_duration
        logical_tie = self._get_logical_tie()
        logical_tie_leaves = list(logical_tie.leaves)
        for leaf in logical_tie:
            detach(Tie, leaf)
            detach(RepeatTie, leaf)
        if self._parent is not None:
            index = self._parent.index(self)
            next_ = index + 1
            self._parent[next_:next_] = following_leaves
        index = logical_tie_leaves.index(self)
        next_ = index + 1
        logical_tie_leaves[next_:next_] = following_leaves
        if 1 < len(logical_tie_leaves) and isinstance(self, (Note, Chord)):
            abjad_tie(logical_tie_leaves)
        if isinstance(components[0], Leaf):
            return select(all_leaves)
        else:
            assert isinstance(components[0], Tuplet)
            assert len(components) == 1
            tuplet = components[0]
            multiplier = tuplet.multiplier
            tuplet = Tuplet(multiplier, [])
            mutate(all_leaves).wrap(tuplet)
            return select(tuplet)

    def _split_by_durations(self, durations, cyclic=False):
        from .Chord import Chord
        from .Note import Note
        from .Selection import Selection
        from .Tuplet import Tuplet

        durations = [Duration(_) for _ in durations]
        durations = Sequence(durations)
        leaf_duration = inspect(self).duration()
        if cyclic:
            durations = durations.repeat_to_weight(leaf_duration)
        if sum(durations) < leaf_duration:
            last_duration = leaf_duration - sum(durations)
            durations = list(durations)
            durations.append(last_duration)
            durations = Sequence(durations)
        durations = durations.truncate(weight=leaf_duration)
        originally_tied = inspect(self).has_indicator(Tie)
        originally_repeat_tied = inspect(self).has_indicator(RepeatTie)
        result_selections = []
        # detach grace containers
        before_grace_container = self._before_grace_container
        if before_grace_container is not None:
            detach(before_grace_container, self)
        after_grace_container = self._after_grace_container
        if after_grace_container is not None:
            detach(after_grace_container, self)
        # do other things
        leaf_prolation = inspect(self).parentage().prolation
        for duration in durations:
            new_leaf = copy.copy(self)
            preprolated_duration = duration / leaf_prolation
            selection = new_leaf._set_duration(preprolated_duration)
            result_selections.append(selection)
        result_components = Sequence(result_selections).flatten(depth=-1)
        result_components = select(result_components)
        result_leaves = select(result_components).leaves(grace=False)
        assert all(isinstance(_, Selection) for _ in result_selections)
        assert all(isinstance(_, Component) for _ in result_components)
        assert result_leaves.are_leaves()
        # strip result leaves of all indicators
        for leaf in result_leaves:
            detach(object, leaf)
        # replace leaf with flattened result
        if inspect(self).parentage().parent is not None:
            mutate(self).replace(result_components)
        # move indicators
        first_result_leaf = result_leaves[0]
        last_result_leaf = result_leaves[-1]
        for indicator in inspect(self).indicators():
            detach(indicator, self)
            direction = getattr(indicator, "_time_orientation", enums.Left)
            if direction is enums.Left:
                attach(indicator, first_result_leaf)
            elif direction == enums.Right:
                attach(indicator, last_result_leaf)
            else:
                raise ValueError(direction)
        # reattach grace containers
        if before_grace_container is not None:
            attach(before_grace_container, first_result_leaf)
        if after_grace_container is not None:
            attach(after_grace_container, last_result_leaf)
        # fuse tuplets
        if isinstance(result_components[0], Tuplet):
            mutate(result_components).fuse()
        # tie split notes
        if isinstance(self, (Note, Chord)) and 1 < len(result_leaves):
            result_leaves._attach_tie_to_leaves()
        if originally_repeat_tied and not inspect(result_leaves[0]).has_indicator(
            RepeatTie
        ):
            attach(RepeatTie(), result_leaves[0])
        if originally_tied and not inspect(result_leaves[-1]).has_indicator(Tie):
            attach(Tie(), result_leaves[-1])
        assert isinstance(result_leaves, Selection)
        assert all(isinstance(_, Leaf) for _ in result_leaves)
        return result_leaves

    ### PUBLIC PROPERTIES ###

    @property
    def multiplier(
        self,
    ) -> typing.Union[Multiplier, mathtools.NonreducedFraction, None]:
        """
        Gets multiplier.
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, argument):
        if isinstance(argument, (mathtools.NonreducedFraction, type(None))):
            multiplier = argument
        else:
            multiplier = Multiplier(argument)
        self._multiplier = multiplier

    @property
    def written_duration(self) -> Duration:
        """
        Gets written duration.
        """
        return self._written_duration

    @written_duration.setter
    def written_duration(self, argument):
        duration = Duration(argument)
        if not duration.is_assignable:
            message = f"not assignable duration: {duration!r}."
            raise exceptions.AssignabilityError(message)
        self._written_duration = duration
