import abc
import copy
from abjad.tools.exceptiontools import AssignabilityError, MissingMetronomeMarkError
from .Component import Component


class Leaf(Component):
    r'''Leaf baseclass.

    Leaves include notes, rests, chords and skips.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_after_grace_container',
        '_grace_container',
        '_leaf_index',
        '_written_duration',
        )

    # TODO: remove?
    _is_counttime_component = True

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, written_duration, name=None):
        import abjad
        Component.__init__(self, name=name)
        self._after_grace_container = None
        self._grace_container = None
        self._leaf_index = None
        self.written_duration = abjad.Duration(written_duration)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        '''Gets new arguments.

        Returns tuple.
        '''
        return (self.written_duration,)

    def __str__(self):
        '''Gets string representation of leaf.

        Returns string.
        '''
        return self._get_compact_representation()

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        import abjad
        lilypond_format = self._get_compact_representation()
        lilypond_format = lilypond_format.replace('<', '&lt;')
        lilypond_format = lilypond_format.replace('>', '&gt;')
        node = Component._as_graphviz_node(self)
        node[0].extend([
            abjad.graphtools.GraphvizTableRow([
                abjad.graphtools.GraphvizTableCell(
                    label=type(self).__name__,
                    attributes={'border': 0},
                    ),
                ]),
            abjad.graphtools.GraphvizTableHorizontalRule(),
            abjad.graphtools.GraphvizTableRow([
                abjad.graphtools.GraphvizTableCell(
                    label=lilypond_format,
                    attributes={'border': 0},
                    ),
                ]),
            ])
        return node

    def _copy_override_and_set_from_leaf(self, leaf):
        import abjad
        if getattr(leaf, '_lilypond_grob_name_manager', None) is not None:
            self._lilypond_grob_name_manager = copy.copy(abjad.override(leaf))
        if getattr(leaf, '_lilypond_setting_name_manager', None) is not None:
            self._lilypond_setting_name_manager = copy.copy(
                abjad.setting(leaf))
        new_indicators = []
        for indicator in leaf._indicator_wrappers:
            new_indicator = copy.copy(indicator)
            new_indicators.append(new_indicator)
        for new_indicator in new_indicators:
            abjad.attach(new_indicator, self)

    def _copy_with_indicators_but_without_children_or_spanners(self):
        import abjad
        new = Component._copy_with_indicators_but_without_children_or_spanners(
            self)
        grace_container = self._grace_container
        if grace_container is not None:
            new_grace_container = \
                grace_container._copy_with_children_and_indicators_but_without_spanners()
            abjad.attach(new_grace_container, new)
        after_grace_container = self._after_grace_container
        if after_grace_container is not None:
            new_after_grace_container = \
                after_grace_container._copy_with_children_and_indicators_but_without_spanners()
            abjad.attach(new_after_grace_container, new)
        return new

    def _detach_after_grace_container(self):
        import abjad
        if self._after_grace_container is not None:
            return abjad.detach(self._after_grace_container, self)

    def _detach_grace_container(self):
        import abjad
        if self._grace_container is not None:
            return abjad.detach(self._grace_container, self)

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
        result.append(('spanners', bundle.after.spanners))
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

    def _format_contents_slot(self, bundle, strict=False):
        result = []
        result.append(self._format_leaf_body(bundle, strict=strict))
        return result

    def _format_grace_body(self):
        result = []
        if self._grace_container is not None:
            grace = self._grace_container
            if len(grace):
                result.append(format(grace))
        return ['grace body', result]

    def _format_leaf_body(self, bundle, strict=False):
        import abjad
        indent = abjad.LilyPondFormatManager.indent
        result = self._format_leaf_nucleus()[1]
        result.extend(bundle.right.stem_tremolos)
        result.extend(bundle.right.articulations)
        result.extend(bundle.right.commands)
        result.extend(bundle.right.indicators)
        result.extend(bundle.right.spanners)
        result.extend(bundle.right.spanner_stops)
        result.extend(bundle.right.spanner_starts)
        result.extend(bundle.right.comments)
        if not strict:
            result = [' '.join(result)]
        markup = bundle.right.markup
        if markup:
            if not strict:
                if len(markup) == 1:
                    result[0] += ' {}'.format(markup[0])
                else:
                    result.extend(indent + '{}'.format(_) for _ in markup)
            else:
                result.extend('{}'.format(_) for _ in markup)
        trill_pitches = bundle.right.trill_pitches
        if trill_pitches:
            assert len(trill_pitches) == 1, repr(trill_pitches)
            result[-1] += ' {}'.format(trill_pitches[0])
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
        return '({})'.format(self._get_formatted_duration())

    def _get_format_pieces(self, strict=False):
        return self._get_lilypond_format(strict=strict).split('\n')

    def _get_format_specification(self):
        import abjad
        summary = self._get_compact_representation()
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=[summary],
            storage_format_args_values=[format(self, 'lilypond')],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    def _get_leaf(self, n):
        import abjad

        def next(component):
            new_component = component._get_nth_component_in_time_order_from(1)
            if new_component is None:
                return
            candidates = new_component._get_descendants_starting_with()
            candidates = [
                x for x in candidates if isinstance(x, abjad.Leaf)
                ]
            for candidate in candidates:
                selection = abjad.select([component, candidate])
                if selection.are_logical_voice():
                    return candidate

        def previous(component):
            new_component = component._get_nth_component_in_time_order_from(-1)
            if new_component is None:
                return
            candidates = new_component._get_descendants_stopping_with()
            candidates = [
                x for x in candidates if isinstance(x, abjad.Leaf)
                ]
            for candidate in candidates:
                selection = abjad.select([component, candidate])
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
        for component in abjad.inspect(self).get_parentage():
            tie_spanners = abjad.inspect(component).get_spanners(abjad.Tie)
            if len(tie_spanners) == 1:
                tie_spanner = tie_spanners.pop()
                return abjad.LogicalTie(items=tie_spanner.leaves)
            elif 1 < len(tie_spanners):
                message = 'parentage of {!r} contains {} tie spanners.'
                message = message.format(self, len(tie_spanners))
                raise Exception(message)
        else:
            return abjad.LogicalTie(items=self)

    def _process_contribution_packet(self, contribution_packet):
        import abjad
        manager = abjad.LilyPondFormatManager
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

    def _report_format_contributions(self, strict=False):
        import abjad
        manager = abjad.LilyPondFormatManager
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
        string = self._format_contents_slot(bundle, strict=strict)[0][1][0]
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
        new_duration = abjad.Duration(new_duration)
        # change LilyPond multiplier if leaf already has LilyPond multiplier
        if self._get_indicators(abjad.Multiplier):
            abjad.detach(abjad.Multiplier, self)
            multiplier = new_duration.__div__(self.written_duration)
            abjad.attach(multiplier, self)
            return abjad.select(self)
        # change written duration if new duration is assignable
        try:
            self.written_duration = new_duration
            return abjad.select(self)
        except AssignabilityError:
            pass
        # make new notes or tuplets if new duration is nonassignable
        maker = abjad.NoteMaker(
            repeat_ties=repeat_ties,
            )
        components = maker(0, new_duration)
        if isinstance(components[0], abjad.Leaf):
            tied_leaf_count = len(components) - 1
            tied_leaves = tied_leaf_count * self
            all_leaves = [self] + tied_leaves
            for leaf, component in zip(all_leaves, components):
                leaf.written_duration = component.written_duration
            self._splice(tied_leaves, grow_spanners=True)
            parentage = abjad.inspect(self).get_parentage()
            if not abjad.inspect(parentage).get_spanners(abjad.Tie):
                tie = abjad.Tie()
                if tie._attachment_test(self):
                    tie = abjad.Tie(
                        repeat_ties=repeat_ties,
                        )
                    abjad.attach(tie, all_leaves)
            return abjad.select(all_leaves)
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
            if not self._get_spanners(abjad.Tie):
                tie = abjad.Tie()
                if tie._attachment_test(self):
                    tie = abjad.Tie(
                        repeat_ties=repeat_ties,
                        )
                    abjad.attach(tie, all_leaves)
            multiplier = tuplet.multiplier
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(all_leaves).wrap(tuplet)
            return abjad.select(tuplet)

    def _split_by_durations(
        self,
        durations,
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=True,
        repeat_ties=False,
        ):
        import abjad
        durations = [abjad.Duration(_) for _ in durations]
        durations = abjad.sequence(durations)
        leaf_duration = abjad.inspect(self).get_duration()
        if cyclic:
            durations = durations.repeat_to_weight(leaf_duration)
        if sum(durations) < leaf_duration:
            last_duration = leaf_duration - sum(durations)
            durations = list(durations)
            durations.append(last_duration)
            durations = abjad.sequence(durations)
        durations = durations.truncate(weight=leaf_duration)
        result_selections = []
        # detach grace containers
        grace_container = self._detach_grace_container()
        after_grace_container = self._detach_after_grace_container()
        leaf_prolation = abjad.inspect(self).get_parentage().prolation
        for duration in durations:
            new_leaf = copy.copy(self)
            preprolated_duration = duration / leaf_prolation
            selection = new_leaf._set_duration(
                preprolated_duration,
                repeat_ties=repeat_ties,
                )
            result_selections.append(selection)
        result_components = abjad.sequence(result_selections).flatten(depth=-1)
        result_components = abjad.select(result_components)
        result_leaves = abjad.select(result_components).leaves()
        assert all(isinstance(_, abjad.Selection) for _ in result_selections)
        assert all(isinstance(_, abjad.Component) for _ in result_components)
        assert result_leaves.are_leaves()
        if abjad.inspect(self).has_spanner(abjad.Tie):
            for leaf in result_leaves:
                abjad.detach(abjad.Tie, leaf)
        # strip result leaves of indicators (other than multipliers)
        for leaf in result_leaves:
            multiplier = abjad.inspect(leaf).get_indicator(abjad.Multiplier)
            abjad.detach(object, leaf)
            abjad.attach(multiplier, leaf)
        # replace leaf with flattened result
        selection = abjad.select(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        if parent:
            parent.__setitem__(slice(start, stop + 1), result_components)
        else:
            selection._give_dominant_spanners(result_components)
            selection._withdraw_from_crossing_spanners()
        # fracture spanners
        if fracture_spanners:
            first_selection = result_selections[0]
            for spanner in abjad.inspect(first_selection[-1]).get_spanners():
                index = spanner._index(first_selection[-1])
                spanner._fracture(index, direction=abjad.Right)
            last_selection = result_selections[-1]
            for spanner in abjad.inspect(last_selection[0]).get_spanners():
                index = spanner._index(last_selection[0])
                spanner._fracture(index, direction=abjad.Left)
            for middle_selection in result_selections[1:-1]:
                spanners = abjad.inspect(middle_selection[0]).get_spanners()
                for spanner in spanners:
                    index = spanner._index(middle_selection[0])
                    spanner._fracture(index, direction=abjad.Left)
                spanners = abjad.inspect(middle_selection[-1]).get_spanners()
                for spanner in spanners:
                    index = spanner._index(middle_selection[-1])
                    spanner._fracture(index, direction=abjad.Right)
        # move indicators
        first_result_leaf = result_leaves[0]
        last_result_leaf = result_leaves[-1]
        for indicator in abjad.inspect(self).get_indicators():
            if isinstance(indicator, abjad.Multiplier):
                continue
            abjad.detach(indicator, self)
            direction = getattr(indicator, '_time_orientation', abjad.Left)
            if direction == abjad.Left:
                abjad.attach(indicator, first_result_leaf)
            elif direction == abjad.Right:
                abjad.attach(indicator, last_result_leaf)
            else:
                raise ValueError(direction)
        # move grace containers
        if grace_container is not None:
            container = grace_container[0]
            assert isinstance(container, abjad.GraceContainer), repr(container)
            abjad.attach(container, first_result_leaf)
        if after_grace_container is not None:
            container = after_grace_container[0]
            prototype = abjad.AfterGraceContainer
            assert isinstance(container, prototype), repr(container)
            abjad.attach(container, last_result_leaf)
        if isinstance(result_components[0], abjad.Tuplet):
            abjad.mutate(result_components).fuse()
        # tie split notes
        if isinstance(self, (abjad.Note, abjad.Chord)) and tie_split_notes:
            result_leaves._attach_tie_spanner_to_leaves(
                repeat_ties=repeat_ties,
                )
        assert isinstance(result_selections, list), repr(result_selections)
        assert all(isinstance(_, abjad.Selection) for _ in result_selections)
        return result_selections

    def _to_tuplet_with_ratio(self, proportions, is_diminution=True):
        import abjad
        # check input
        proportions = abjad.Ratio(proportions)
        # find target duration of tuplet
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
        maker = abjad.NoteMaker()
        try:
            notes = [abjad.Note(0, x) for x in written_durations]
        except AssignabilityError:
            denominator = target_duration.denominator
            note_durations = [
                abjad.Duration(_, denominator)
                for _ in proportions.numbers
                ]
            notes = maker(0, note_durations)
        # make tuplet
        contents_duration = abjad.inspect(notes).get_duration()
        multiplier = target_duration / contents_duration
        tuplet = abjad.Tuplet(multiplier, notes)
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

    def _get_duration_in_seconds(self):
        import abjad
        mark = self._get_effective(abjad.MetronomeMark)
        if mark is not None and not mark.is_imprecise:
            result = (
                self._get_duration() /
                mark.reference_duration /
                mark.units_per_minute * 60
                )
            return abjad.Duration(result)
        raise MissingMetronomeMarkError

    def _get_formatted_duration(self):
        import abjad
        duration_string = self.written_duration.lilypond_duration_string
        multiplier = None
        multiplier_prototype = (abjad.Multiplier, abjad.NonreducedFraction)
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
        import abjad
        if self.written_duration:
            multiplier_prototype = (abjad.Multiplier, abjad.NonreducedFraction)
            if self._get_indicators(multiplier_prototype):
                multipliers = self._get_indicators(multiplier_prototype)
                if 1 == len(multipliers):
                    multiplier = multipliers[0]
                    multiplier = abjad.Duration(multiplier)
                elif 1 < len(multipliers):
                    message = 'more than one duration multiplier.'
                    raise ValueError(message)
                multiplied_duration = multiplier * self.written_duration
                return multiplied_duration
            else:
                return abjad.Duration(self.written_duration)
        else:
            return None

    def _get_preprolated_duration(self):
        return self._get_multiplied_duration()

    ### PUBLIC PROPERTIES ###

    @property
    def written_duration(self):
        '''Written duration of leaf.

        Set to duration.

        Returns duration.
        '''
        return self._written_duration

    @written_duration.setter
    def written_duration(self, argument):
        import abjad
        rational = abjad.Duration(argument)
        if not rational.is_assignable:
            message = 'not assignable duration: {!r}.'
            message = message.format(rational)
            raise AssignabilityError(message)
        self._written_duration = rational
