# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import contextualize
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import select
from abjad.tools.scoretools.Component import Component


class Leaf(Component):
    r'''Abstract base class from which notes, rests, chords and skips inherit.
    '''

    ### CLASS VARIABLES ##

    # TODO: see if _grace and _after_grace can be removed
    #       or grace and after_grace; should only need one set of attrs
    __slots__ = (
        '_after_grace',
        '_grace',
        '_leaf_index',
        '_written_duration',
        '_written_pitch_indication_is_nonsemantic',
        '_written_pitch_indication_is_at_sounding_pitch',
        'after_grace',
        'grace',
        )

    _is_counttime_component = True

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, written_duration):
        Component.__init__(self)
        self._leaf_index = None
        self.written_duration = durationtools.Duration(written_duration)
        self.written_pitch_indication_is_nonsemantic = False
        self.written_pitch_indication_is_at_sounding_pitch = True

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

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        return '({})'.format(self._formatted_duration)

    @property
    def _duration_in_seconds(self):
        from abjad.tools import indicatortools
        tempo = self._get_effective_context_mark(indicatortools.Tempo)
        if tempo is not None and not tempo.is_imprecise:
            result = (self._get_duration() /
                tempo.duration /
                tempo.units_per_minute * 60
                )
            return durationtools.Duration(result)
        raise MissingTempoError

    @property
    def _format_pieces(self):
        return self._lilypond_format.split('\n')

    @property
    def _formatted_duration(self):
        duration_string = self.written_duration.lilypond_duration_string
        multiplier = None
        multipliers = self._get_indicators(durationtools.Multiplier)
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
            if self._get_indicators(durationtools.Multiplier):
                multipliers = self._get_indicators(
                    durationtools.Multiplier)
                if 1 == len(multipliers):
                    multiplier = multipliers[0]
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

    @property
    def _repr_specification(self):
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            body_text=repr(self._compact_representation),
            positional_argument_values=(),
            )

    @property
    def _storage_format_specification(self):
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                format(self, 'lilypond'),
                ),
            )


    ### PRIVATE METHODS ###

    def _copy_override_and_set_from_leaf(self, leaf):
        if getattr(leaf, '_override', None) is not None:
            self._override = copy.copy(override(leaf))
        if getattr(leaf, '_set', None) is not None:
            self._set = copy.copy(contextualize(leaf))
        new_indicators = []
        for indicator in leaf._indicators:
            new_indicator = copy.copy(indicator)
            new_indicators.append(new_indicator)
        self._indicators = new_indicators

    def _copy_with_marks_but_without_children_or_spanners(self):
        new = Component._copy_with_marks_but_without_children_or_spanners(self)
        for grace_container in self._get_grace_containers():
            new_grace_container = \
                grace_container._copy_with_children_and_marks_but_without_spanners()
            new_grace_container(new)
        return new

    def _format_after_slot(leaf, bundle):
        result = []
        slot_dictionary = bundle.after
        result.append(('spanners', bundle.after.spanners))
        result.append(('context marks', bundle.after.context_marks))
        result.append(('commands', bundle.after.commands))
        result.append(('other marks', bundle.after.other_marks))
        result.append(('comments', bundle.after.comments))
        return result

    def _format_agrace_body(leaf):
        result = []
        if hasattr(leaf, '_after_grace'):
            after_grace = leaf.after_grace
            if len(after_grace):
                result.append(format(after_grace))
        return ['agrace body', result]

    def _format_agrace_opening(leaf):
        result = []
        if hasattr(leaf, '_after_grace'):
            if len(leaf.after_grace):
                result.append(r'\afterGrace')
        return ['agrace opening', result]

    def _format_before_slot(leaf, bundle):
        result = []
        result.append(leaf._format_grace_body())
        result.append(('comments', bundle.before.comments))
        result.append(('commands', bundle.before.commands))
        result.append(('context marks', bundle.before.context_marks))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        result.append(('spanners', bundle.before.spanners))
        return result

    def _format_close_brackets_slot(leaf, bundle):
        return []

    def _format_closing_slot(leaf, bundle):
        result = []
        result.append(leaf._format_agrace_body())
        result.append(('spanners', bundle.closing.spanners))
        result.append(('commands', bundle.closing.commands))
        result.append(('context marks', bundle.closing.context_marks))
        result.append(('comments', bundle.closing.comments))
        return result

    def _format_contents_slot(leaf, bundle):
        result = []
        result.append(leaf._format_leaf_body(bundle))
        return result

    def _format_grace_body(leaf):
        result = []
        if hasattr(leaf, '_grace'):
            grace = leaf.grace
            if len(grace):
                result.append(format(grace))
        return ['grace body', result]

    def _format_leaf_body(leaf, bundle):
        result = leaf._format_leaf_nucleus()[1]
        result.extend(bundle.right.stem_tremolos)
        result.extend(bundle.right.articulations)
        result.extend(bundle.right.commands)
        result.extend(bundle.right.context_marks)
        result.extend(bundle.right.spanners)
        result.extend(bundle.right.comments)
        result = [' '.join(result)]
        markup = bundle.right.markup
        if markup:
            if len(markup) == 1:
                result[0] += ' {}'.format(markup[0])
            else:
                result.extend('\t{}'.format(x) for x in markup)
        return ['leaf body', result]

    # TODO: subclass this properly for chord
    def _format_leaf_nucleus(leaf):
        from abjad.tools import scoretools
        if not isinstance(leaf, scoretools.Chord):
            return ['nucleus', leaf._body]
        result = []
        chord = leaf
        note_heads = chord.note_heads
        if any('\n' in format(x) for x in note_heads):
            for note_head in note_heads:
                current_format = format(note_head)
                format_list = current_format.split('\n')
                format_list = ['\t' + x for x in format_list]
                result.extend(format_list)
            result.insert(0, '<')
            result.append('>')
            result = '\n'.join(result)
            result += str(chord._formatted_duration)
        else:
            result.extend([format(x) for x in note_heads])
            result = '<%s>%s' % (' '.join(result), chord._formatted_duration)
        # single string, but wrapped in list bc contribution
        return ['nucleus', [result]]

    def _format_open_brackets_slot(leaf, bundle):
        return []

    def _format_opening_slot(leaf, bundle):
        result = []
        result.append(('comments', bundle.opening.comments))
        result.append(('context marks', bundle.opening.context_marks))
        result.append(('commands', bundle.opening.commands))
        result.append(('spanners', bundle.opening.spanners))
        result.append(leaf._format_agrace_opening())
        return result

    def _get_leaf(self, n=0):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        Selection = selectiontools.Selection

        def next(component):
            new_component = component._get_nth_component_in_time_order_from(1)
            if new_component is None:
                return
            candidates = new_component._get_descendants_starting_with()
            candidates = \
                [x for x in candidates if isinstance(x, scoretools.Leaf)]
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

    def _get_tie_chain(self):
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        spanner_classes = (spannertools.Tie,)
        for component in self._get_parentage():
            tie_spanners = component._get_spanners(spanner_classes)
            if len(tie_spanners) == 1:
                tie_spanner = tie_spanners.pop()
                return selectiontools.TieChain(music=tie_spanner.leaves)
            elif 1 < len(tie_spanners):
                message = 'multiple tie spanners found.'
                raise ExtraSpannerError(message)
        else:
            return selectiontools.TieChain(music=self)

    def _process_contribution_packet(self, contribution_packet):
        result = ''
        for contributor, contributions in contribution_packet:
            if contributions:
                if isinstance(contributor, tuple):
                    contributor = '\t' + contributor[0] + ':\n'
                else:
                    contributor = '\t' + contributor + ':\n'
                result += contributor
                for contribution in contributions:
                    contribution = '\t\t' + contribution + '\n'
                    result += contribution
        return result

    def _report_format_contributors(self):
        manager = systemtools.LilyPondFormatManager
        bundle = manager.get_all_format_contributions(self)
        report = ''
        report += 'slot 1:\n'
        packet = self._format_before_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 3:\n'
        packet = self._format_opening_slot(bundle)
        report += self._process_contribution_packet(packet)
        report += 'slot 4:\n'
        report += '\tleaf body:\n'
        string = self._format_contents_slot(bundle)[0][1][0]
        report += '\t\t' + string + '\n'
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

    def _set_duration(self, new_duration):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        new_duration = durationtools.Duration(new_duration)
        # change LilyPond multiplier if leaf already has LilyPond multiplier
        if self._get_indicators(durationtools.Multiplier):
            detach(durationtools.Multiplier, self)
            multiplier = new_duration / self.written_duration
            attach(multiplier, self)
            return [self]
        # change written duration if new duration is assignable
        try:
            self.written_duration = new_duration
            return [self]
        except AssignabilityError:
            pass
        # make new notes or tuplets if new duration is nonassignable
        components = scoretools.make_notes(0, new_duration)
        if isinstance(components[0], scoretools.Leaf):
            tied_leaf_count = len(components) - 1
            tied_leaves = tied_leaf_count * self
            all_leaves = [self] + tied_leaves
            for x, component in zip(all_leaves, components):
                x.written_duration = component.written_duration
            self._splice(tied_leaves, grow_spanners=True)
            parentage = self._get_parentage()
            if not parentage._get_spanners(spannertools.Tie):
                tie = spannertools.Tie()
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
                tie = spannertools.Tie()
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
        ):
        from abjad.tools import indicatortools
        from abjad.tools import pitchtools
        from abjad.tools import selectiontools
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        durations = [durationtools.Duration(x) for x in durations]
        if cyclic:
            durations = sequencetools.repeat_sequence_to_weight_exactly(
                durations, self._get_duration())
        durations = [durationtools.Duration(x) for x in durations]
        if sum(durations) < self._get_duration():
            last_duration = self._get_duration() - sum(durations)
            durations.append(last_duration)
        sequencetools.truncate_sequence_to_weight(
            durations, self._get_duration())
        result = []
        leaf_prolation = self._get_parentage(include_self=False).prolation
        leaf_copy = copy.copy(self)
        for duration in durations:
            new_leaf = copy.copy(self)
            preprolated_duration = duration / leaf_prolation
            shard = new_leaf._set_duration(preprolated_duration)
            shard = [x._get_parentage().root for x in shard]
            result.append(shard)
        flattened_result = sequencetools.flatten_sequence(result)
        flattened_result = selectiontools.SliceSelection(flattened_result)
        spanner_classes = (spannertools.Tie,)
        parentage = self._get_parentage()
        if parentage._get_spanners(spanner_classes=spanner_classes):
            selection = select(flattened_result)
            for component in selection:
                # TODO: make top-level detach() work here
                for spanner in component._get_spanners(spanner_classes):
                    spanner.detach()
                #detach(spanner_classes, component)
        # replace leaf with flattened result
        selection = selectiontools.SliceSelection(self)
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
                index = spanner.index(first_shard[-1])
                spanner.fracture(index, direction=Right)
            last_shard = result[-1]
            for spanner in last_shard[0]._get_spanners():
                index = spanner.index(last_shard[0])
                spanner.fracture(index, direction=Left)
            for middle_shard in result[1:-1]:
                for spanner in middle_shard[0]._get_spanners():
                    index = spanner.index(middle_shard[0])
                    spanner.fracture(index, direction=Left)
                for spanner in middle_shard[-1]._get_spanners():
                    index = spanner.index(middle_shard[-1])
                    spanner.fracture(index, direction=Right)
        # adjust first leaf
        first_leaf = flattened_result[0]
        self._detach_grace_containers(kind='after')
        # adjust any middle leaves
        for middle_leaf in flattened_result[1:-1]:
            middle_leaf._detach_grace_containers(kind='grace')
            self._detach_grace_containers(kind='after')
            detach(indicatortools.ContextMark, middle_leaf)
        # adjust last leaf
        last_leaf = flattened_result[-1]
        last_leaf._detach_grace_containers(kind='grace')
        detach(indicatortools.ContextMark, last_leaf)
        # tie split notes, rests and chords as specified
        if pitchtools.Pitch.is_pitch_carrier(self) and tie_split_notes:
            flattened_result_leaves = iterate(flattened_result).by_class(
                scoretools.Leaf)
            # TODO: implement SliceSelection._attach_tie_spanner_to_leaves()
            for leaf_pair in sequencetools.iterate_sequence_pairwise_strict(
                flattened_result_leaves):
                selection = selectiontools.ContiguousSelection(leaf_pair)
                selection._attach_tie_spanner_to_leaf_pair()
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
        detach(indicatortools.ContextMark, new_leaf)
        left_leaf_list = self._set_duration(preprolated_duration)
        right_preprolated_duration = \
            leaf_multiplied_duration - preprolated_duration
        right_leaf_list = new_leaf._set_duration(right_preprolated_duration)
        leaf_left_of_split = left_leaf_list[-1]
        leaf_right_of_split = right_leaf_list[0]
        leaves_around_split = (leaf_left_of_split, leaf_right_of_split)
        if fracture_spanners:
            for spanner in leaf_left_of_split._get_spanners():
                index = spanner.index(leaf_left_of_split)
                spanner.fracture(index, direction=Right)
        # tie split notes, rests and chords as specified
        if pitchtools.Pitch.is_pitch_carrier(self) and tie_split_notes:
            selection = selectiontools.ContiguousSelection(leaves_around_split)
            selection._attach_tie_spanner_to_leaf_pair()
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
        from abjad.tools import scoretools
        # check input
        proportions = mathtools.Ratio(proportions)
        # find target duration of fixed-duration tuplet
        target_duration = self.written_duration
        # find basic duration of note in tuplet
        basic_prolated_duration = target_duration / sum(proportions)
        # find basic written duration of note in tuplet
        basic_written_duration = \
            basic_prolated_duration.equal_or_greater_assignable
        # find written duration of each note in tuplet
        written_durations = [x * basic_written_duration for x in proportions]
        # make tuplet notes
        try:
            notes = [scoretools.Note(0, x) for x in written_durations]
        except AssignabilityError:
            denominator = target_duration._denominator
            note_durations = [durationtools.Duration(x, denominator)
                for x in proportions]
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

    ### PUBLIC PROPERTIES ###

    @apply
    def written_duration():
        def fget(self):
            '''Written duration of leaf.

            Set to duration.

            Returns duration.
            '''
            return self._written_duration
        def fset(self, expr):
            rational = durationtools.Duration(expr)
            if not rational.is_assignable:
                message = 'not assignable duration: {!r}.'
                message = message.format(rational)
                raise AssignabilityError(message)
            self._written_duration = rational
        return property(**locals())

    @apply
    def written_pitch_indication_is_at_sounding_pitch():
        def fget(self):
            r'''Returns true when written pitch is at sounding pitch.
            Returns false when written pitch is transposed.
            '''
            return self._written_pitch_indication_is_at_sounding_pitch
        def fset(self, expr):
            if not isinstance(expr, bool):
                raise TypeError
            self._written_pitch_indication_is_at_sounding_pitch = expr
        return property(**locals())

    @apply
    def written_pitch_indication_is_nonsemantic():
        def fget(self):
            r'''Returns true when pitch is nonsemantic.
            Returns false otherwise.

            Set to true when using leaves only graphically.

            Setting this value to true sets sounding pitch flag to false.
            '''
            return self._written_pitch_indication_is_nonsemantic
        def fset(self, expr):
            if not isinstance(expr, bool):
                raise TypeError
            self._written_pitch_indication_is_nonsemantic = expr
            if expr is True:
                self.written_pitch_indication_is_at_sounding_pitch = False
        return property(**locals())
