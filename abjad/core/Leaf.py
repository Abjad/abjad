import abc
import copy
import uqbar.graphs
from abjad import enums
from abjad import exceptions
from abjad.indicators.MetronomeMark import MetronomeMark
from abjad.mathtools.NonreducedFraction import NonreducedFraction
from abjad.mathtools.Ratio import Ratio
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.top.attach import attach
from abjad.top.detach import detach
from abjad.top.inspect import inspect
from abjad.top.override import override
from abjad.top.select import select
from abjad.top.sequence import sequence
from abjad.top.setting import setting
from abjad.utilities.Duration import Duration
from abjad.utilities.Multiplier import Multiplier
from .Component import Component


class Leaf(Component):
    """
    Leaf baseclass.

    Leaves include notes, rests, chords and skips.
    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_after_grace_container',
        '_grace_container',
        '_leaf_index',
        '_spanners',
        '_written_duration',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, written_duration):
        Component.__init__(self)
        self._after_grace_container = None
        self._grace_container = None
        self._leaf_index = None
        self._spanners = []
        self.written_duration = Duration(written_duration)

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies leaf.

        Returns new leaf.
        """
        new = Component.__copy__(self, *arguments)
        grace_container = self._grace_container
        if grace_container is not None:
            new_grace_container = grace_container._copy_with_children()
            attach(new_grace_container, new)
        after_grace_container = self._after_grace_container
        if after_grace_container is not None:
            new_after_grace_container = \
                after_grace_container._copy_with_children()
            attach(new_after_grace_container, new)
        return new

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return (self.written_duration,)

    def __str__(self):
        """
        Gets string representation of leaf.

        Returns string.
        """
        return self._get_compact_representation()

    ### PRIVATE METHODS ###

    def _append_spanner(self, spanner):
        if id(spanner) in [id(_) for _ in self._spanners]:
            return
        self._spanners.append(spanner)

    def _as_graphviz_node(self):
        lilypond_format = self._get_compact_representation()
        lilypond_format = lilypond_format.replace('<', '&lt;')
        lilypond_format = lilypond_format.replace('>', '&gt;')
        node = Component._as_graphviz_node(self)
        node[0].extend([
            uqbar.graphs.TableRow([
                uqbar.graphs.TableCell(
                    type(self).__name__,
                    attributes={'border': 0},
                    ),
                ]),
            uqbar.graphs.HRule(),
            uqbar.graphs.TableRow([
                uqbar.graphs.TableCell(
                    lilypond_format,
                    attributes={'border': 0},
                    ),
                ]),
            ])
        return node

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, '_overrides', None) is not None:
            self._overrides = copy.copy(override(leaf))
        if getattr(leaf, '_lilypond_setting_name_manager', None) is not None:
            self._lilypond_setting_name_manager = copy.copy(
                setting(leaf))
        new_wrappers = []
        for wrapper in leaf._wrappers:
            new_wrapper = copy.copy(wrapper)
            new_wrappers.append(new_wrapper)
        for new_wrapper in new_wrappers:
            attach(new_wrapper, self)

    def _detach_after_grace_container(self):
        if self._after_grace_container is not None:
            return detach(self._after_grace_container, self)

    def _detach_grace_container(self):
        if self._grace_container is not None:
            return detach(self._grace_container, self)

    def _detach_spanners(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
        for spanner in spanners:
            spanner._sever_all_leaves()
        return spanners

    def _format_after_grace_body(self):
        result = []
        if self._after_grace_container is not None:
            after_grace = self._after_grace_container
            if len(after_grace):
                result.append(format(after_grace))
        return ['after grace body', result]

    def _format_after_grace_opening(self):
        result = []
        if self._after_grace_container is not None:
            if len(self._after_grace_container):
                result.append(r'\afterGrace')
        return ['after grace opening', result]

    def _format_absolute_after_slot(self, bundle):
        result = []
        result.append(('literals', bundle.absolute_after.commands))
        return result

    def _format_absolute_before_slot(self, bundle):
        result = []
        result.append(('literals', bundle.absolute_before.commands))
        return result

    def _format_after_slot(self, bundle):
        result = []
        result.append(('stem_tremolos', bundle.after.stem_tremolos))
        result.append(('articulations', bundle.after.articulations))
        result.append(('markup', bundle.after.markup))
        result.append(('spanners', bundle.after.spanners))
        result.append(('spanner_stops', bundle.after.spanner_stops))
        result.append(('spanner_starts', bundle.after.spanner_starts))
        # NOTE: LilyPond demands \startTrillSpan appear after almost all
        #       other format contributions; pitched trills dangerously
        #       suppress markup and the starts of other spanners when
        #       \startTrillSpan appears lexically prior to those commands;
        #       but \startTrillSpan must appear before calls to \set.
        result.append(('trill_spanner_starts', bundle.after.trill_spanner_starts))
        result.append(('commands', bundle.after.commands))
        result.append(('commands', bundle.after.leaks))
        result.append(('comments', bundle.after.comments))
        return result

    def _format_before_slot(self, bundle):
        result = []
        result.append(self._format_grace_body())
        result.append(('comments', bundle.before.comments))
        result.append(('commands', bundle.before.commands))
        result.append(('indicators', bundle.before.indicators))
        result.append(('grob reverts', bundle.grob_reverts))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        result.append(('spanners', bundle.before.spanners))
        return result

    def _format_close_brackets_slot(self, bundle):
        return []

    def _format_closing_slot(self, bundle):
        result = []
        result.append(self._format_after_grace_body())
        result.append(('spanners', bundle.closing.spanners))
        result.append(('commands', bundle.closing.commands))
        result.append(('indicators', bundle.closing.indicators))
        result.append(('comments', bundle.closing.comments))
        return result

    def _format_contents_slot(self, bundle):
        result = []
        result.append(self._format_leaf_body(bundle))
        return result

    def _format_grace_body(self):
        result = []
        if self._grace_container is not None:
            grace = self._grace_container
            if len(grace):
                result.append(format(grace))
        return ['grace body', result]

    def _format_leaf_body(self, bundle):
        indent = LilyPondFormatManager.indent
        result = self._format_leaf_nucleus()[1]
        return ['self body', result]

    def _format_leaf_nucleus(self):
        return ['nucleus', self._get_body()]

    def _format_open_brackets_slot(self, bundle):
        return []

    def _format_opening_slot(self, bundle):
        result = []
        result.append(('comments', bundle.opening.comments))
        result.append(('indicators', bundle.opening.indicators))
        result.append(('commands', bundle.opening.commands))
        result.append(self._format_after_grace_opening())
        result.append(('spanners', bundle.opening.spanners))
        return result

    def _get_compact_representation(self):
        return f'({self._get_formatted_duration()})'

    def _get_format_pieces(self):
        return self._get_lilypond_format().split('\n')

    def _get_format_specification(self):
        summary = self._get_compact_representation()
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[summary],
            storage_format_args_values=[format(self, 'lilypond')],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    def _get_leaf(self, n):

        def next(component):
            new_component = component._get_nth_component_in_time_order_from(1)
            if new_component is None:
                return
            candidates = new_component._get_descendants_starting_with()
            candidates = [
                x for x in candidates if isinstance(x, Leaf)
                ]
            for candidate in candidates:
                selection = select([component, candidate])
                if selection.are_logical_voice():
                    return candidate

        def previous(component):
            new_component = component._get_nth_component_in_time_order_from(-1)
            if new_component is None:
                return
            candidates = new_component._get_descendants_stopping_with()
            candidates = [
                x for x in candidates if isinstance(x, Leaf)
                ]
            for candidate in candidates:
                selection = select([component, candidate])
                if selection.are_logical_voice():
                    return candidate
        current_leaf = self
        if n < 0:
            for i in range(abs(n)):
                current_leaf = previous(current_leaf)
                if current_leaf is None:
                    break
        elif n == 0:
            pass
        else:
            for i in range(n):
                current_leaf = next(current_leaf)
                if current_leaf is None:
                    break
        return current_leaf

    def _get_logical_tie(self):
        import abjad
        for component in [self]:
            ties = inspect(component).spanners(abjad.Tie)
            if len(ties) == 1:
                tie = ties.pop()
                return abjad.LogicalTie(items=tie.leaves)
            elif 1 < len(ties):
                message = f'parentage of {self!r} contains {len(ties)} ties.'
                raise Exception(ties)
        else:
            return abjad.LogicalTie(items=self)

    def _get_spanner(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
        if not spanners:
            raise exceptions.MissingSpannerError('no spanner found.')
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            message = f'multiple spanners found: {spanners!r}'
            raise ExtraSpannerError(message)

    def _get_spanners(self, prototype=None):
        import abjad
        prototype = prototype or (abjad.Spanner,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        spanner_items = prototype[:]
        prototype, spanner_objects = [], []
        for spanner_item in spanner_items:
            if isinstance(spanner_item, type):
                prototype.append(spanner_item)
            elif isinstance(spanner_item, abjad.Spanner):
                spanner_objects.append(spanner_item)
            else:
                message = 'must be spanner class or spanner object: {!r}'
                message = message.format(spanner_item)
        prototype = tuple(prototype)
        spanner_objects = tuple(spanner_objects)
        matching_spanners = []
        for spanner in self._spanners:
            if isinstance(spanner, prototype):
                if id(spanner) not in [id(_) for _ in matching_spanners]:
                    matching_spanners.append(spanner)
            elif any(spanner == x for x in spanner_objects):
                if id(spanner) not in [id(_) for _ in matching_spanners]:
                    matching_spanners.append(spanner)
        return matching_spanners

    def _has_spanner(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
        return bool(spanners)

    def _process_contribution_packet(self, contribution_packet):
        manager = LilyPondFormatManager
        indent = manager.indent
        result = ''
        for contributor, contributions in contribution_packet:
            if contributions:
                if isinstance(contributor, tuple):
                    contributor = indent + contributor[0] + ':\n'
                else:
                    contributor = indent + contributor + ':\n'
                result += contributor
                for contribution in contributions:
                    contribution = (indent * 2) + contribution + '\n'
                    result += contribution
        return result

    def _remove_spanner(self, spanner):
        if id(spanner) not in [id(_) for _ in self._spanners]:
            raise Exception(f'{self!s} has no {spanner}.')
        spanners = [_ for _ in self._spanners if id(_) != id(spanner)]
        self._spanners = spanners

    def _report_format_contributions(self):
        manager = LilyPondFormatManager
        indent = manager.indent
        bundle = manager.bundle_format_contributions(self)
        report = ''
        report += 'slot absolute before:\n'
        packet = self._format_absolute_before_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 1:\n'
        packet = self._format_before_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 3:\n'
        packet = self._format_opening_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 4:\n'
        report += indent + 'leaf body:\n'
        string = self._format_contents_slot(bundle)[0][1][0]
        report += (2 * indent) + string + '\n'
        report += 'slot 5:\n'
        packet = self._format_closing_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 7:\n'
        packet = self._format_after_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot absolute after:\n'
        packet = self._format_absolute_after_slot(bundle)
        report += self._process_contribution_packet(packet)
        while report[-1] == '\n':
            report = report[:-1]
        return report

    def _scale(self, multiplier):
        new_duration = multiplier * self._get_duration()
        self._set_duration(new_duration)

    def _set_duration(self, new_duration, repeat_ties=False):
        import abjad
        new_duration = Duration(new_duration)
        # change LilyPond multiplier if leaf already has LilyPond multiplier
        if self._get_indicators(Multiplier):
            detach(Multiplier, self)
            multiplier = new_duration.__div__(self.written_duration)
            attach(multiplier, self)
            return select(self)
        # change written duration if new duration is assignable
        try:
            self.written_duration = new_duration
            return select(self)
        except exceptions.AssignabilityError:
            pass
        # make new notes or tuplets if new duration is nonassignable
        maker = abjad.NoteMaker(
            repeat_ties=repeat_ties,
            )
        components = maker(0, new_duration)
        if isinstance(components[0], Leaf):
            tied_leaf_count = len(components) - 1
            tied_leaves = tied_leaf_count * self
            all_leaves = [self] + tied_leaves
            for leaf, component in zip(all_leaves, components):
                leaf.written_duration = component.written_duration
            self._splice(tied_leaves, grow_spanners=True)
            if not inspect(self).has_spanner(abjad.Tie):
                tie = abjad.Tie()
                if tie._attachment_test(self):
                    tie = abjad.Tie(repeat=repeat_ties)
                    attach(tie, all_leaves)
            return select(all_leaves)
        else:
            assert isinstance(components[0], abjad.Tuplet)
            tuplet = components[0]
            components = tuplet[:]
            tied_leaf_count = len(components) - 1
            tied_leaves = tied_leaf_count * self
            all_leaves = [self] + tied_leaves
            for leaf, component in zip(all_leaves, components):
                leaf.written_duration = component.written_duration
            self._splice(tied_leaves, grow_spanners=True)
            if not inspect(self).has_spanner(abjad.Tie):
                tie = abjad.Tie()
                if tie._attachment_test(self):
                    tie = abjad.Tie(repeat=repeat_ties)
                    attach(tie, all_leaves)
            multiplier = tuplet.multiplier
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(all_leaves).wrap(tuplet)
            return select(tuplet)

    def _split_by_durations(
        self,
        durations,
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=True,
        repeat_ties=False,
        ):
        import abjad
        durations = [Duration(_) for _ in durations]
        durations = sequence(durations)
        leaf_duration = inspect(self).duration()
        if cyclic:
            durations = durations.repeat_to_weight(leaf_duration)
        if sum(durations) < leaf_duration:
            last_duration = leaf_duration - sum(durations)
            durations = list(durations)
            durations.append(last_duration)
            durations = sequence(durations)
        durations = durations.truncate(weight=leaf_duration)
        result_selections = []
        # detach grace containers
        grace_container = self._detach_grace_container()
        after_grace_container = self._detach_after_grace_container()
        leaf_prolation = inspect(self).parentage().prolation
        for duration in durations:
            new_leaf = copy.copy(self)
            preprolated_duration = duration / leaf_prolation
            selection = new_leaf._set_duration(
                preprolated_duration,
                repeat_ties=repeat_ties,
                )
            result_selections.append(selection)
        result_components = sequence(result_selections).flatten(depth=-1)
        result_components = select(result_components)
        result_leaves = select(result_components).leaves()
        assert all(isinstance(_, abjad.Selection) for _ in result_selections)
        assert all(isinstance(_, Component) for _ in result_components)
        assert result_leaves.are_leaves()
        if inspect(self).has_spanner(abjad.Tie):
            for leaf in result_leaves:
                detach(abjad.Tie, leaf)
        # strip result leaves of indicators (other than multipliers)
        for leaf in result_leaves:
            multiplier = inspect(leaf).indicator(Multiplier)
            detach(object, leaf)
            if multiplier is not None:
                attach(multiplier, leaf)
        # replace leaf with flattened result
        selection = select(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        if parent:
            parent.__setitem__(slice(start, stop + 1), result_components)
        else:
            selection._give_dominant_spanners(result_components)
            selection._withdraw_from_crossing_spanners()
        # fracture spanners
        if fracture_spanners:
            first_selection = result_selections[0]
            for spanner in inspect(first_selection[-1]).spanners():
                index = spanner._index(first_selection[-1])
                spanner._fracture(index, direction=enums.Right)
            last_selection = result_selections[-1]
            for spanner in inspect(last_selection[0]).spanners():
                index = spanner._index(last_selection[0])
                spanner._fracture(index, direction=enums.Left)
            for middle_selection in result_selections[1:-1]:
                spanners = inspect(middle_selection[0]).spanners()
                for spanner in spanners:
                    index = spanner._index(middle_selection[0])
                    spanner._fracture(index, direction=enums.Left)
                spanners = inspect(middle_selection[-1]).spanners()
                for spanner in spanners:
                    index = spanner._index(middle_selection[-1])
                    spanner._fracture(index, direction=enums.Right)
        # move indicators
        first_result_leaf = result_leaves[0]
        last_result_leaf = result_leaves[-1]
        for indicator in inspect(self).indicators():
            if isinstance(indicator, Multiplier):
                continue
            detach(indicator, self)
            direction = getattr(indicator, '_time_orientation', enums.Left)
            if direction is enums.Left:
                attach(indicator, first_result_leaf)
            elif direction == enums.Right:
                attach(indicator, last_result_leaf)
            else:
                raise ValueError(direction)
        # move grace containers
        if grace_container is not None:
            container = grace_container[0]
            assert isinstance(container, abjad.GraceContainer), repr(container)
            attach(container, first_result_leaf)
        if after_grace_container is not None:
            container = after_grace_container[0]
            prototype = abjad.AfterGraceContainer
            assert isinstance(container, prototype), repr(container)
            attach(container, last_result_leaf)
        if isinstance(result_components[0], abjad.Tuplet):
            abjad.mutate(result_components).fuse()
        # tie split notes
        if isinstance(self, (abjad.Note, abjad.Chord)) and tie_split_notes:
            result_leaves._attach_tie_to_leaves(
                repeat_ties=repeat_ties,
                )
        assert isinstance(result_selections, list), repr(result_selections)
        assert all(isinstance(_, abjad.Selection) for _ in result_selections)
        return result_selections

    ### PRIVATE PROPERTIES ###

    def _get_duration_in_seconds(self):
        mark = self._get_effective(MetronomeMark)
        if mark is not None and not mark.is_imprecise:
            result = (
                self._get_duration() /
                mark.reference_duration /
                mark.units_per_minute * 60
                )
            return Duration(result)
        raise exceptions.MissingMetronomeMarkError

    def _get_formatted_duration(self):
        duration_string = self.written_duration.lilypond_duration_string
        multiplier = None
        multiplier_prototype = (Multiplier, NonreducedFraction)
        multipliers = self._get_indicators(multiplier_prototype)
        if not multipliers:
            pass
        elif len(multipliers) == 1:
            multiplier = multipliers[0]
        elif 1 < len(multipliers):
            message = 'more than one LilyPond duration multiplier.'
            raise ValueError(message)
        if multiplier is not None:
            result = '{} * {!s}'.format(duration_string, multiplier)
        else:
            result = duration_string
        return result

    def _get_multiplied_duration(self):
        if self.written_duration:
            multiplier_prototype = (Multiplier, NonreducedFraction)
            if self._get_indicators(multiplier_prototype):
                multipliers = self._get_indicators(multiplier_prototype)
                if 1 == len(multipliers):
                    multiplier = multipliers[0]
                    multiplier = Duration(multiplier)
                elif 1 < len(multipliers):
                    message = 'more than one duration multiplier.'
                    raise ValueError(message)
                multiplied_duration = multiplier * self.written_duration
                return multiplied_duration
            else:
                return Duration(self.written_duration)
        else:
            return None

    def _get_preprolated_duration(self):
        return self._get_multiplied_duration()

    ### PUBLIC PROPERTIES ###

    @property
    def written_duration(self):
        """
        Written duration of leaf.

        Set to duration.

        Returns duration.
        """
        return self._written_duration

    @written_duration.setter
    def written_duration(self, argument):
        rational = Duration(argument)
        if not rational.is_assignable:
            message = 'not assignable duration: {!r}.'
            message = message.format(rational)
            raise exceptions.AssignabilityError(message)
        self._written_duration = rational
