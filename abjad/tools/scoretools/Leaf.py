# -*- coding: utf-8 -*-
import abc
import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import systemtools
from abjad.tools import timespantools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import select
from abjad.tools.topleveltools import set_
from abjad.tools.scoretools.Component import Component


class Leaf(Component):
    r'''Abstract base class from which leaves inherit.

    Leaves include notes, rests, chords and skips.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_leaf_index',
        '_written_duration',
        )

    _is_counttime_component = True

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, written_duration, name=None):
        Component.__init__(self, name=name)
        self._leaf_index = None
        self.written_duration = durationtools.Duration(written_duration)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Gets new arguments.

        Returns tuple.
        '''
        return (self.written_duration,)

    def __str__(self):
        '''String representation of leaf.

        Returns string.
        '''
        return self._compact_representation

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        from abjad.tools import documentationtools
        lilypond_format = self._compact_representation
        lilypond_format = lilypond_format.replace('<', '&lt;')
        lilypond_format = lilypond_format.replace('>', '&gt;')
        node = Component._as_graphviz_node(self)
        node[0].extend([
            documentationtools.GraphvizTableRow([
                documentationtools.GraphvizTableCell(
                    label=type(self).__name__,
                    attributes={'border': 0},
                    ),
                ]),
            documentationtools.GraphvizTableHorizontalRule(),
            documentationtools.GraphvizTableRow([
                documentationtools.GraphvizTableCell(
                    label=lilypond_format,
                    attributes={'border': 0},
                    ),
                ]),
            ])
        return node

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, '_lilypond_grob_name_manager', None) is not None:
            self._lilypond_grob_name_manager = copy.copy(override(leaf))
        if getattr(leaf, '_lilypond_setting_name_manager', None) is not None:
            self._lilypond_setting_name_manager = copy.copy(
                set_(leaf))
        new_indicators = []
        for indicator in leaf._indicator_expressions:
            new_indicator = copy.copy(indicator)
            new_indicators.append(new_indicator)
        for new_indicator in new_indicators:
            attach(new_indicator, self)

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = Component._copy_with_indicators_but_without_children_or_spanners(self)
        for grace_container in self._get_grace_containers():
            new_grace_container = \
                grace_container._copy_with_children_and_indicators_but_without_spanners()
            attach(new_grace_container, new)
        return new

    def _format_after_grace_body(self):
        result = []
        if self._after_grace is not None:
            after_grace = self._after_grace
            if len(after_grace):
                result.append(format(after_grace))
        return ['after grace body', result]

    def _format_after_grace_opening(self):
        result = []
        if self._after_grace is not None:
            if len(self._after_grace):
                result.append(r'\afterGrace')
        return ['after grace opening', result]

    def _format_after_slot(self, bundle):
        result = []
        result.append(('spanners', bundle.after.spanners))
        result.append(('grob reverts', bundle.grob_reverts))
        result.append(('indicators', bundle.after.indicators))
        result.append(('commands', bundle.after.commands))
        result.append(('comments', bundle.after.comments))
        return result

    def _format_before_slot(self, bundle):
        result = []
        result.append(self._format_grace_body())
        result.append(('comments', bundle.before.comments))
        result.append(('commands', bundle.before.commands))
        result.append(('indicators', bundle.before.indicators))
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
        if self._grace is not None:
            grace = self._grace
            if len(grace):
                result.append(format(grace))
        return ['grace body', result]

    def _format_leaf_body(self, bundle):
        from abjad.tools import systemtools
        indent = systemtools.LilyPondFormatManager.indent
        result = self._format_leaf_nucleus()[1]
        result.extend(bundle.right.stem_tremolos)
        result.extend(bundle.right.articulations)
        result.extend(bundle.right.commands)
        result.extend(bundle.right.indicators)
        result.extend(bundle.right.spanners)
        result.extend(bundle.right.spanner_stops)
        result.extend(bundle.right.spanner_starts)
        result.extend(bundle.right.comments)
        result = [' '.join(result)]
        markup = bundle.right.markup
        if markup:
            if len(markup) == 1:
                result[0] += ' {}'.format(markup[0])
            else:
                result.extend(indent + '{}'.format(x) for x in markup)
        trill_pitches = bundle.right.trill_pitches
        if trill_pitches:
            assert len(trill_pitches) == 1
            result[-1] += ' {}'.format(trill_pitches[0])
        return ['self body', result]

    def _format_leaf_nucleus(self):
        return ['nucleus', self._body]

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

    def _get_format_pieces(self):
        return self._lilypond_format.split('\n')

    def _get_format_specification(self):
        summary = self._compact_representation
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[summary],
            storage_format_args_values=[format(self, 'lilypond')],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    def _get_leaf(self, n=0):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        Selection = selectiontools.Selection

        def next(component):
            new_component = component._get_nth_component_in_time_order_from(1)
            if new_component is None:
                return
            candidates = new_component._get_descendants_starting_with()
            candidates = [
                x for x in candidates if isinstance(x, scoretools.Leaf)
                ]
            for candidate in candidates:
                if Selection._all_are_components_in_same_logical_voice(
                    [component, candidate]):
                    return candidate

        def previous(component):
            new_component = component._get_nth_component_in_time_order_from(-1)
            if new_component is None:
                return
            candidates = new_component._get_descendants_stopping_with()
            candidates = \
                [x for x in candidates if isinstance(x, scoretools.Leaf)]
            for candidate in candidates:
                if Selection._all_are_components_in_same_logical_voice(
                    [component, candidate]):
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

    def _get_leaf_index(self):
        self._update_now(offsets=True)
        return self._leaf_index

    def _get_logical_tie(self):
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        prototype = (spannertools.Tie,)
        for component in self._get_parentage():
            tie_spanners = component._get_spanners(prototype)
            if len(tie_spanners) == 1:
                tie_spanner = tie_spanners.pop()
                return selectiontools.LogicalTie(
                    music=tie_spanner._get_leaves()
                    )
            elif 1 < len(tie_spanners):
                message = 'parentage of {!r} contains {} tie spanners.'
                message = message.format(self, len(tie_spanners))
                raise Exception(message)
        else:
            return selectiontools.LogicalTie(music=self)

    def _process_contribution_packet(self, contribution_packet):
        manager = systemtools.LilyPondFormatManager
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

    def _report_format_contributors(self):
        manager = systemtools.LilyPondFormatManager
        indent = manager.indent
        bundle = manager.bundle_format_contributions(self)
        report = ''
        report += 'slot 1:\n'
        packet = self._format_before_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 3:\n'
        packet = self._format_opening_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 4:\n'
        report += indent + 'leaf body:\n'
        string = self._format_contents_slot(bundle)[0][1][0]
        report += (indent * 2) + string + '\n'
        report += 'slot 5:\n'
        packet = self._format_closing_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 7:\n'
        packet = self._format_after_slot(bundle)
        report += self._process_contribution_packet(packet)
        while report[-1] == '\n':
            report = report[:-1]
        return report

    def _scale(self, multiplier):
        new_duration = multiplier * self._get_duration()
        self._set_duration(new_duration)

    def _set_duration(self, new_duration, use_messiaen_style_ties=False):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        new_duration = durationtools.Duration(new_duration)
        # change LilyPond multiplier if leaf already has LilyPond multiplier
        if self._get_indicators(durationtools.Multiplier):
            detach(durationtools.Multiplier, self)
            multiplier = new_duration.__div__(self.written_duration)
            attach(multiplier, self)
            return [self]
        # change written duration if new duration is assignable
        try:
            self.written_duration = new_duration
            return [self]
        except AssignabilityError:
            pass
        # make new notes or tuplets if new duration is nonassignable
        components = scoretools.make_notes(
            0,
            new_duration,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
        if isinstance(components[0], scoretools.Leaf):
            tied_leaf_count = len(components) - 1
            tied_leaves = tied_leaf_count * self
            all_leaves = [self] + tied_leaves
            for x, component in zip(all_leaves, components):
                x.written_duration = component.written_duration
            self._splice(tied_leaves, grow_spanners=True)
            parentage = self._get_parentage()
            if not parentage._get_spanners(spannertools.Tie):
                #if spannertools.Tie._attachment_test(self):
                tie = spannertools.Tie()
                if tie._attachment_test(self):
                    tie = spannertools.Tie(
                        use_messiaen_style_ties=use_messiaen_style_ties,
                        )
                    attach(tie, all_leaves)
            return all_leaves
        else:
            assert isinstance(components[0], scoretools.Tuplet)
            tuplet = components[0]
            components = tuplet[:]
            tied_leaf_count = len(components) - 1
            tied_leaves = tied_leaf_count * self
            all_leaves = [self] + tied_leaves
            for x, component in zip(all_leaves, components):
                x.written_duration = component.written_duration
            self._splice(tied_leaves, grow_spanners=True)
            if not self._get_spanners(spannertools.Tie):
                #if spannertools.Tie._attachment_test(self):
                tie = spannertools.Tie()
                if tie._attachment_test(self):
                    tie = spannertools.Tie(
                        use_messiaen_style_ties=use_messiaen_style_ties,
                        )
                    attach(tie, all_leaves)
            tuplet_multiplier = tuplet.multiplier
            scoretools.Tuplet(tuplet_multiplier, all_leaves)
            return [tuplet]

    def _split(
        self,
        durations,
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=True,
        use_messiaen_style_ties=False,
        ):
        from abjad.tools import pitchtools
        from abjad.tools import selectiontools
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        durations = [durationtools.Duration(x) for x in durations]
        if cyclic:
            durations = sequencetools.repeat_sequence_to_weight(
                durations, self._get_duration())
        durations = [durationtools.Duration(x) for x in durations]
        if sum(durations) < self._get_duration():
            last_duration = self._get_duration() - sum(durations)
            durations.append(last_duration)
        sequencetools.truncate_sequence(
            durations,
            weight=self._get_duration(),
            )
        result = []
        leaf_prolation = self._get_parentage(include_self=False).prolation
        timespan = self._get_timespan()
        start_offset = timespan.start_offset
        for duration in durations:
            new_leaf = copy.copy(self)
            preprolated_duration = duration / leaf_prolation
            shard = new_leaf._set_duration(
                preprolated_duration,
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            for x in shard:
                if isinstance(x, scoretools.Leaf):
                    x_duration = x.written_duration * leaf_prolation
                else:
                    x_duration = x.multiplied_duration * leaf_prolation
                stop_offset = x_duration + start_offset
                x._start_offset = start_offset
                x._stop_offset = stop_offset
                x._timespan = timespantools.Timespan(
                    start_offset=start_offset,
                    stop_offset=stop_offset,
                    )
                start_offset = stop_offset
            shard = [x._get_parentage().root for x in shard]
            result.append(shard)
        flattened_result = sequencetools.flatten_sequence(result)
        flattened_result = selectiontools.Selection(flattened_result)
        prototype = (spannertools.Tie,)
        parentage = self._get_parentage()
        if parentage._get_spanners(prototype=prototype):
            selection = select(flattened_result)
            for component in selection:
                # TODO: make top-level detach() work here
                for spanner in component._get_spanners(prototype):
                    spanner._sever_all_components()
                #detach(prototype, component)
        # replace leaf with flattened result
        selection = selectiontools.Selection(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        if parent:
            parent.__setitem__(slice(start, stop + 1), flattened_result)
        else:
            selection._give_dominant_spanners(flattened_result)
            selection._withdraw_from_crossing_spanners()
        # fracture spanners
        if fracture_spanners:
            first_shard = result[0]
            for spanner in first_shard[-1]._get_spanners():
                index = spanner._index(first_shard[-1])
                spanner._fracture(index, direction=Right)
            last_shard = result[-1]
            for spanner in last_shard[0]._get_spanners():
                index = spanner._index(last_shard[0])
                spanner._fracture(index, direction=Left)
            for middle_shard in result[1:-1]:
                for spanner in middle_shard[0]._get_spanners():
                    index = spanner._index(middle_shard[0])
                    spanner._fracture(index, direction=Left)
                for spanner in middle_shard[-1]._get_spanners():
                    index = spanner._index(middle_shard[-1])
                    spanner._fracture(index, direction=Right)
        # adjust first leaf
        first_leaf = flattened_result[0]
        self._detach_grace_containers(kind='after')
        # adjust any middle leaves
        for middle_leaf in flattened_result[1:-1]:
            middle_leaf._detach_grace_containers(kind='grace')
            self._detach_grace_containers(kind='after')
            detach(object, middle_leaf)
        # adjust last leaf
        last_leaf = flattened_result[-1]
        last_leaf._detach_grace_containers(kind='grace')
        detach(object, last_leaf)
        # tie split notes, rests and chords as specified
        if pitchtools.Pitch.is_pitch_carrier(self) and tie_split_notes:
            flattened_result_leaves = iterate(flattened_result).by_class(
                scoretools.Leaf)
            # TODO: implement Selection._attach_tie_spanner_to_leaves()
            for leaf_pair in sequencetools.iterate_sequence_nwise(
                flattened_result_leaves):
                selection = selectiontools.Selection(leaf_pair)
                selection._attach_tie_spanner_to_leaf_pair(
                    use_messiaen_style_ties=use_messiaen_style_ties,
                    )
        # return result
        return result

    # TODO: This should be replaced in favor of self._split().
    #       The precondition is that self._split() must be
    #       extended to handle graces.
    def _split_by_duration(
        self,
        duration,
        fracture_spanners=False,
        tie_split_notes=True,
        use_messiaen_style_ties=False,
        ):
        from abjad.tools import indicatortools
        from abjad.tools import pitchtools
        from abjad.tools import selectiontools
        # check input
        duration = durationtools.Duration(duration)
        # calculate durations
        leaf_multiplied_duration = self._multiplied_duration
        prolation = self._get_parentage(include_self=False).prolation
        preprolated_duration = duration / prolation
        # handle boundary cases
        if preprolated_duration <= 0:
            return ([], [self])
        if leaf_multiplied_duration <= preprolated_duration:
            return ([self], [])
        # create new leaf
        new_leaf = copy.copy(self)
        self._splice([new_leaf], grow_spanners=True)
        # adjust leaf
        self._detach_grace_containers(kind='after')
        # adjust new leaf
        new_leaf._detach_grace_containers(kind='grace')
        left_leaf_list = self._set_duration(
            preprolated_duration,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
        right_preprolated_duration = \
            leaf_multiplied_duration - preprolated_duration
        right_leaf_list = new_leaf._set_duration(
            right_preprolated_duration,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
        leaf_left_of_split = left_leaf_list[-1]
        leaf_right_of_split = right_leaf_list[0]
        leaves_around_split = (leaf_left_of_split, leaf_right_of_split)
        if fracture_spanners:
            for spanner in leaf_left_of_split._get_spanners():
                index = spanner._index(leaf_left_of_split)
                spanner._fracture(index, direction=Right)
        # tie split notes, rests and chords as specified
        if pitchtools.Pitch.is_pitch_carrier(self) and tie_split_notes:
            selection = selectiontools.Selection(leaves_around_split)
            selection._attach_tie_spanner_to_leaf_pair(
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
        return left_leaf_list, right_leaf_list
        # TODO: make this substitution work
        #return self._split(
        #    leaf,
        #    [duration],
        #    cyclic=False,
        #    fracture_spanners=fracture_spanners,
        #    tie_split_notes=tie_split_notes,
        #    )

    def _to_tuplet_with_ratio(self, proportions, is_diminution=True):
        from abjad.tools import scoretools
        # check input
        proportions = mathtools.Ratio(proportions)
        # find target duration of fixed-duration tuplet
        target_duration = self.written_duration
        # find basic duration of note in tuplet
        basic_prolated_duration = target_duration / sum(proportions.numbers)
        # find basic written duration of note in tuplet
        basic_written_duration = \
            basic_prolated_duration.equal_or_greater_assignable
        # find written duration of each note in tuplet
        written_durations = [
            _ * basic_written_duration for _ in proportions.numbers
            ]
        # make tuplet notes
        try:
            notes = [scoretools.Note(0, x) for x in written_durations]
        except AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [
                durationtools.Duration(_, denominator)
                for _ in proportions.numbers
                ]
            notes = scoretools.make_notes(0, note_durations)
        # make tuplet
        tuplet = scoretools.FixedDurationTuplet(target_duration, notes)
        # fix tuplet contents if necessary
        tuplet._fix()
        # change prolation if necessary
        if not tuplet.multiplier == 1:
            if is_diminution:
                if not tuplet.is_diminution:
                    tuplet.toggle_prolation()
            else:
                if tuplet.is_diminution:
                    tuplet.toggle_prolation()
        # return tuplet
        return tuplet

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '({})'.format(self._formatted_duration)

    @property
    def _duration_in_seconds(self):
        from abjad.tools import indicatortools
        tempo = self._get_effective(indicatortools.Tempo)
        if tempo is not None and not tempo.is_imprecise:
            result = (self._get_duration() /
                tempo.reference_duration /
                tempo.units_per_minute * 60
                )
            return durationtools.Duration(result)
        raise MissingTempoError

    @property
    def _formatted_duration(self):
        duration_string = self.written_duration.lilypond_duration_string
        multiplier = None
        multiplier_prototype = (
            durationtools.Multiplier,
            mathtools.NonreducedFraction,
            )
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

    @property
    def _multiplied_duration(self):
        if self.written_duration:
            multiplier_prototype = (
                durationtools.Multiplier,
                mathtools.NonreducedFraction,
                )
            if self._get_indicators(multiplier_prototype):
                multipliers = self._get_indicators(multiplier_prototype)
                if 1 == len(multipliers):
                    multiplier = multipliers[0]
                    multiplier = durationtools.Duration(multiplier)
                elif 1 < len(multipliers):
                    message = 'more than one duration multiplier.'
                    raise ValueError(message)
                multiplied_duration = multiplier * self.written_duration
                return multiplied_duration
            else:
                return durationtools.Duration(self.written_duration)
        else:
            return None

    @property
    def _preprolated_duration(self):
        return self._multiplied_duration

    ### PUBLIC PROPERTIES ###

    @property
    def written_duration(self):
        '''Written duration of leaf.

        Set to duration.

        Returns duration.
        '''
        return self._written_duration

    @written_duration.setter
    def written_duration(self, expr):
        rational = durationtools.Duration(expr)
        if not rational.is_assignable:
            message = 'not assignable duration: {!r}.'
            message = message.format(rational)
            raise AssignabilityError(message)
        self._written_duration = rational
