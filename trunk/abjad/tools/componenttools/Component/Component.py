# -*- encoding: utf-8 -*-
import abc
import copy
import fractions
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import lilypondproxytools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import timespantools
from abjad.tools.abctools import AbjadObject
from abjad.tools.selectiontools import mutate


class Component(AbjadObject):
    r'''Any score component.

    Notes, rests, chords, tuplets, voices, staves
    and scores are all components.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_dependent_context_marks',
        '_is_forbidden_to_update', 
        '_marks_are_current',
        '_offsets_are_current', 
        '_offsets_in_seconds_are_current', 
        '_override', 
        '_parent',
        '_set', 
        '_spanners',
        '_start_marks',
        '_start_offset', 
        '_start_offset_in_seconds', 
        '_stop_offset', 
        '_stop_offset_in_seconds',
        '_timespan',
        'lilypond_file',
        )

    _is_counttime_component = False

    ### INITIALIZER ###

    def __init__(self):
        self._dependent_context_marks = list()
        self._is_forbidden_to_update = False
        self._marks_are_current = False
        self._start_marks = list()
        self._offsets_in_seconds_are_current = False
        self._offsets_are_current = False
        self._parent = None
        self._spanners = set([])
        self._start_offset = None
        self._start_offset_in_seconds = None
        self._stop_offset = None
        self._stop_offset_in_seconds = None
        self._timespan = timespantools.Timespan()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        '''Copies component with marks but without children of component
        or spanners attached to component.

        Returns new component.
        '''
        return self._copy_with_marks_but_without_children_or_spanners()

    def __getnewargs__(self):
        '''Gets new arguments.

        Returns tuple.
        '''
        return ()

    def __mul__(self, n):
        '''Copies component `n` times and detaches spanners.

        Returns list of new components.
        '''
        from abjad.tools import spannertools
        result = mutate(self).copy(n=n)
        spannertools.detach_spanners_attached_to_components_in_expr(result)
        if isinstance(result, type(self)):
            result = [result]
        else:
            result = list(result)
        return result

    def __rmul__(self, n):
        '''Copies component `n` times and detach spanners.

        Returns list of new components.
        '''
        return self * n

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._format_component(pieces=True)

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = {}
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.iteritems():
                name_dictionary[name] = copy.copy(children)
        if hasattr(self, 'name') and self.name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = []
            name_dictionary[self.name].append(self)
        return name_dictionary

    def _copy_with_children_and_marks_but_without_spanners(self):
        return self._copy_with_marks_but_without_children_or_spanners()

    def _copy_with_marks_but_without_children_or_spanners(self):
        from abjad.tools import marktools
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(self.override)
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(self.set)
        for mark in self._get_marks():
            new_mark = copy.copy(mark)
            new_mark.attach(new)
        return new

    def _detach_grace_containers(self, kind=None):
        grace_containers = self._get_grace_containers(kind=kind)
        for grace_container in grace_containers:
            grace_container.detach()
        return grace_containers

    def _detach_marks(
        self,
        mark_classes=None,
        ):
        marks = []
        for mark in self._get_marks(mark_classes=mark_classes):
            mark.detach()
            marks.append(mark)
        return tuple(marks)

    def _detach_spanners(self, spanner_classes=None):
        spanners = self._get_spanners(spanner_classes=spanner_classes)
        for spanner in spanners:
            spanner.detach()
        return spanners

    def _format_after_slot(self, format_contributions):
        pass

    def _format_before_slot(self, format_contributions):
        pass

    def _format_close_brackets_slot(self, format_contributions):
        pass

    def _format_closing_slot(self, format_contributions):
        pass

    def _format_component(self, pieces=False):
        result = []
        format_contributions = formattools.get_all_format_contributions(self)
        result.extend(self._format_before_slot(format_contributions))
        result.extend(self._format_open_brackets_slot(format_contributions))
        result.extend(self._format_opening_slot(format_contributions))
        result.extend(self._format_contents_slot(format_contributions))
        result.extend(self._format_closing_slot(format_contributions))
        result.extend(self._format_close_brackets_slot(format_contributions))
        result.extend(self._format_after_slot(format_contributions))
        contributions = []
        for contributor, contribution in result:
            contributions.extend(contribution)
        if pieces:
            return contributions
        else:
            return '\n'.join(contributions)

    def _format_contents_slot(self, format_contributions):
        pass

    def _format_open_brackets_slot(self, format_contributions):
        pass

    def _format_opening_slot(self, format_contributions):
        pass

    def _get_duration(self, in_seconds=False):
        if in_seconds:
            return self._duration_in_seconds
        else:
            parentage = self._select_parentage(include_self=False)
            return parentage.prolation * self._preprolated_duration

    def _get_effective_context_mark(self, context_mark_classes=None):
        from abjad.tools import contexttools
        from abjad.tools import datastructuretools
        from abjad.tools import measuretools
        # do special things for time signature marks
        if context_mark_classes == contexttools.TimeSignatureMark:
            if isinstance(self, measuretools.Measure):
                if self._has_mark(contexttools.TimeSignatureMark):
                    return self._get_mark(contexttools.TimeSignatureMark)
        # updating marks of entire score tree if necessary
        self._update_now(marks=True)
        # gathering candidate marks
        candidate_marks = datastructuretools.SortedCollection(
            key=lambda x: x.start_component._get_timespan().start_offset)
        for parent in self._select_parentage(include_self=True):
            parent_marks = parent._dependent_context_marks
            for mark in parent_marks:
                if isinstance(mark, context_mark_classes):
                    if mark.effective_context is not None:
                        candidate_marks.insert(mark)
                    elif isinstance(mark, contexttools.TimeSignatureMark):
                        if isinstance(
                            mark.start_component, measuretools.Measure):
                            candidate_marks.insert(mark)
        # elect most recent candidate mark
        if candidate_marks:
            try:
                start_offset = self._get_timespan().start_offset
                return candidate_marks.find_le(start_offset)
            except ValueError:
                pass

    def _get_effective_staff(self):
        from abjad.tools import contexttools
        from abjad.tools import stafftools
        staff_change_mark = self._get_effective_context_mark(
            contexttools.StaffChangeMark)
        if staff_change_mark is not None:
            effective_staff = staff_change_mark.staff
        else:
            parentage = self._select_parentage()
            effective_staff = parentage.get_first(stafftools.Staff)
        return effective_staff

    def _get_format_contributions_for_slot(self, n, format_contributions=None):
        if format_contributions is None:
            format_contributions = \
                formattools.get_all_format_contributions(self)
        result = []
        slots = (
            'before', 
            'open_brackets', 
            'opening',
            'contents', 
            'closing', 
            'close_brackets', 
            'after',
            )
        if isinstance(n, str):
            n = n.replace(' ', '_')
        elif isinstance(n, int):
            n = slots[n-1]
        attr = getattr(self, '_format_{}_slot'.format(n))
        for source, contributions in attr(format_contributions):
            result.extend(contributions)
        return result

    def _get_grace_containers(self, kind=None):
        result = []
        if kind in (None, 'grace') and hasattr(self, '_grace'):
            result.append(self._grace)
        if kind in (None, 'after') and hasattr(self, '_after_grace'):
            result.append(self._after_grace)
        return tuple(result)

    def _get_in_my_logical_voice(self, n, component_class=None):
        from abjad.tools import iterationtools
        if 0 <= n:
            generator = iterationtools.iterate_logical_voice_from_component(
                self, component_class=component_class, reverse=False)
            for i, component in enumerate(generator):
                if i == n:
                    return component
        else:
            n = abs(n)
            generator = iterationtools.iterate_logical_voice_from_component(
                self, component_class=component_class, reverse=True)
            for i, component in enumerate(generator):
                if i == n:
                    return component

    def _get_mark(self, mark_classes=None):
        marks = self._get_marks(mark_classes=mark_classes)
        if not marks:
            raise MissingMarkError
        elif 1 < len(marks):
            raise ExtraMarkError
        else:
            return marks[0]

    def _get_marks(self, mark_classes=None):
        from abjad.tools import marktools
        mark_classes = mark_classes or (marktools.Mark,)
        if not isinstance(mark_classes, tuple):
            mark_classes = (mark_classes,)
        marks = []
        for mark in self._start_marks:
            if isinstance(mark, mark_classes):
                marks.append(mark)
        return tuple(marks)

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        markup = self._get_marks(mark_classes=(markuptools.Markup,))
        if direction is Up:
            return tuple(x for x in markup if x.direction is Up)
        elif direction is Down:
            return tuple(x for x in markup if x.direction is Down)
        return markup

    def _get_nth_component_in_time_order_from(self, n):
        from abjad.tools import componenttools
        assert mathtools.is_integer_equivalent_expr(n)
        def next(component):
            if component is not None:
                for parent in component._select_parentage(include_self=True):
                    next_sibling = parent._get_sibling(1)
                    if next_sibling is not None:
                        return next_sibling
        def previous(component):
            if component is not None:
                for parent in component._select_parentage(include_self=True):
                    next_sibling = parent._get_sibling(-1)
                    if next_sibling is not None:
                        return next_sibling
        result = self
        if 0 < n:
            for i in range(n):
                result = next(result)
        elif n < 0:
            for i in range(abs(n)):
                result = previous(result)
        return result

    def _get_sibling(self, n):
        if n == 0:
            return self
        elif 0 < n:
            if self._parent is not None:
                if not self._parent.is_simultaneous:
                    index = self._parent.index(self)
                    if index + n < len(self._parent):
                        return self._parent[index + n]
        elif n < 0:
            if self._parent is not None:
                if not self._parent.is_simultaneous:
                    index = self._parent.index(self)
                    if 0 <= index + n:
                        return self._parent[index + n]

    def _get_spanner(self, spanner_classes=None):
        spanners = self._get_spanners(spanner_classes=spanner_classes)
        if not spanners:
            raise MissingSpannerError
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            raise ExtraSpannerError

    def _get_spanners(self, spanner_classes=None):
        from abjad.tools import spannertools
        spanner_classes = spanner_classes or (spannertools.Spanner,)
        if not isinstance(spanner_classes, tuple):
            spanner_classes = (spanner_classes, )
        spanners = set()
        for spanner in set(self._spanners):
            if isinstance(spanner, spanner_classes):
                spanners.add(spanner)
        return spanners

    def _get_timespan(self, in_seconds=False):
        if in_seconds:
            self._update_now(offsets_in_seconds=True)
            if self._start_offset_in_seconds is None:
                raise MissingTempoError
            return timespantools.Timespan(
                start_offset=self._start_offset_in_seconds, 
                stop_offset=self._stop_offset_in_seconds,
                )
        else:
            self._update_now(offsets=True)
            return self._timespan

    def _has_mark(self, mark_classes=None):
        marks = self._get_marks(mark_classes=mark_classes)
        return bool(marks)

    def _has_spanner(self, spanner_classes=None):
        spanners = self._get_spanners(spanner_classes=spanner_classes)
        return bool(spanners)

    def _initialize_keyword_values(self, **kwargs):
        for key, value in kwargs.iteritems():
            self._set_keyword_value(key, value)

    def _is_immediate_temporal_successor_of(self, component):
        from abjad.tools import componenttools
        temporal_successors = []
        current = self
        while current is not None:
            next_sibling = current._get_sibling(1)
            if next_sibling is None:
                current = current._parent
            else:
                temporal_successors = \
                    next_sibling._select_descendants_starting_with()
                break
        return component in temporal_successors

    def _move_marks(self, recipient_component):
        result = []
        for mark in self._get_marks():
            result.append(mark.attach(recipient_component))
        return tuple(result)

    def _remove_from_parent(self):
        self._update_later(offsets=True)
        if self._parent is not None:
            self._parent._music.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        from abjad.tools import componenttools
        if self._parent is not None and name_dictionary:
            for parent in self._select_parentage(include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    for component in name_dictionary[name]:
                        named_children[name].remove(component)
                    if not named_children[name]:
                        del named_children[name]

    def _restore_named_children_to_parentage(self, name_dictionary):
        from abjad.tools import componenttools
        if self._parent is not None and name_dictionary:
            for parent in self._select_parentage(include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].extend(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

    def _select_components(self, component_classes=None, include_self=True):
        from abjad.tools import iterationtools
        expr = self
        if include_self:
            expr = [self]
        components = iterationtools.iterate_components_in_expr(
            expr, component_class=component_classes)
        return selectiontools.FreeComponentSelection(components)

    def _select_contents(self, include_self=True):
        result = []
        if include_self:
            result.append(self)
        result.extend(getattr(self, '_music', []))
        result = selectiontools.SliceSelection(result)
        return result

    def _select_descendants(
        self,
        include_self=True,
        ):
        return selectiontools.Descendants(
            self,
            include_self=include_self,
            )

    def _select_descendants_starting_with(self):
        from abjad.tools import containertools
        result = []
        result.append(self)
        if isinstance(self, containertools.Container):
            if self.is_simultaneous:
                for x in self:
                    result.extend(x._select_descendants_starting_with())
            elif self:
                result.extend(self[0]._select_descendants_starting_with())
        return result

    def _select_descendants_stopping_with(self):
        from abjad.tools import containertools
        result = []
        result.append(self)
        if isinstance(self, containertools.Container):
            if self.is_simultaneous:
                for x in self:
                    result.extend(x._select_descendants_stopping_with())
            elif self:
                result.extend(self[-1]._select_descendants_stopping_with())
        return result

    def _select_lineage(self):
        return selectiontools.Lineage(self)

    def _select_parentage(self, include_self=True):
        return selectiontools.Parentage(self, include_self=include_self)

    def _select_vertical_moment(self, governor=None):
        offset = self._get_timespan().start_offset
        if governor is None:
            governor = self._select_parentage().root
        return selectiontools.VerticalMoment(governor, offset)

    def _select_vertical_moment_at(self, offset):
        return selectiontools.VerticalMoment(self, offset)

    def _set_keyword_value(self, key, value):
        attribute_chain = key.split('__')
        plug_in_name = attribute_chain[0]
        names = attribute_chain[1:]
        if plug_in_name == 'duration':
            attribute_name = names[0]
            command = 'self.%s.%s = %r' % (plug_in_name, attribute_name, value)
            print command
            if 'multiplier' not in command:
                exec(command)
        elif plug_in_name == 'override':
            if len(names) == 2:
                grob_name, attribute_name = names
                exec('self.override.%s.%s = %r' % (
                    grob_name, attribute_name, value))
            elif len(names) == 3:
                context_name, grob_name, attribute_name = names
                exec('self.override.%s.%s.%s = %r' % (
                    context_name, grob_name, attribute_name, value))
            else:
                raise ValueError
        elif plug_in_name == 'set':
            if len(names) == 1:
                setting_name = names[0]
                exec('self.set.%s = %r' % (setting_name, value))
            elif len(names) == 2:
                context_name, setting_name = names
                exec('self.set.%s.%s = %r' % (
                    context_name, setting_name, value))
            else:
                raise ValueError
        else:
            message = 'Unknown keyword argument plug-in name: {!r}.'
            message = message.format(plug_in_name)
            raise ValueError(message)

    def _set_parent(self, new_parent):
        r'''Not composer-safe.
        '''
        named_children = self._cache_named_children()
        self._remove_named_children_from_parentage(named_children)
        self._remove_from_parent()
        self._parent = new_parent
        self._restore_named_children_to_parentage(named_children)
        self._update_later(offsets=True)

    def _splice(
        self,
        components,
        direction=Right,
        grow_spanners=True,
        ):
        from abjad.tools import componenttools
        from abjad.tools import spannertools
        assert all(isinstance(x, componenttools.Component) for x in components)
        if direction == Right:
            if grow_spanners:
                insert_offset = self._get_timespan().stop_offset
                receipt = spannertools.get_spanners_that_dominate_components(
                    [self])
                for spanner, index in receipt:
                    insert_component = \
                        spannertools.find_spanner_component_starting_at_exactly_score_offset(
                        spanner, insert_offset)
                    if insert_component is not None:
                        insert_index = spanner.index(insert_component)
                    else:
                        insert_index = len(spanner)
                    for component in reversed(components):
                        spanner._insert(insert_index, component)
                        component._spanners.add(spanner)
            selection = self.select(sequential=True)
            parent, start, stop = selection._get_parent_and_start_stop_indices()
            if parent is not None:
                if grow_spanners:
                    for component in reversed(components):
                        component._set_parent(parent)
                        parent._music.insert(start + 1, component)
                else:
                    after = stop + 1
                    parent.__setitem__(slice(after, after), components)
            return [self] + components
        else:
            if grow_spanners:
                offset= self._get_timespan().start_offset
                receipt = spannertools.get_spanners_that_dominate_components(
                    [self])
                for spanner, x in receipt:
                    index = \
                        spannertools.find_index_of_spanner_component_at_score_offset(
                        spanner, offset)
                    for component in reversed(components):
                        spanner._insert(index, component)
                        component._spanners.add(spanner)
            selection = self.select(sequential=True)
            parent, start, stop = \
                selection._get_parent_and_start_stop_indices()
            if parent is not None:
                if grow_spanners:
                    for component in reversed(components):
                        component._set_parent(parent)
                        parent._music.insert(start, component)
                else:
                    parent.__setitem__(slice(start, start), components)
            return components + [self]

    def _split_by_duration(
        self,
        offset,
        fracture_spanners=False,
        tie_split_notes=True,
        ):
        from abjad.tools import componenttools
        from abjad.tools import containertools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools import measuretools
        from abjad.tools import notetools
        from abjad.tools import resttools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        # check input
        offset = durationtools.Offset(offset)
        assert 0 <= offset, repr(offset)
        # if zero offset then return empty list and self
        if offset == 0:
            return [], self
        if isinstance(self, leaftools.Leaf):
            halves = self._split_by_duration(
                offset,
                fracture_spanners=fracture_spanners,
                tie_split_notes=tie_split_notes,
                )
            assert len(halves) == 2
            return halves
        # get split point score offset
        global_split_point = self._get_timespan().start_offset + offset
        # get any duration-crossing descendents
        cross_offset = self._get_timespan().start_offset + offset
        duration_crossing_descendants = []
        for descendant in self._select_descendants():
            start_offset = descendant._get_timespan().start_offset
            stop_offset = descendant._get_timespan().stop_offset
            if start_offset < cross_offset < stop_offset:
                duration_crossing_descendants.append(descendant)
        # get any duration-crossing measure descendents
        measures = [
            x for x in duration_crossing_descendants 
            if isinstance(x, measuretools.Measure)
            ]
        # if we must split a power-of-two measure at non-power-of-two split point
        # go ahead and transform the power-of-two measure to non-power-of-two 
        # equivalent now; code that crawls and splits later on will be happier
        if len(measures) == 1:
            measure = measures[0]
            split_point_in_measure = \
                global_split_point - measure._get_timespan().start_offset
            if measure.has_non_power_of_two_denominator:
                if not measure.implied_prolation ==\
                    split_point_in_measure.implied_prolation:
                    raise NotImplementedError
            elif not mathtools.is_nonnegative_integer_power_of_two(
                split_point_in_measure.denominator):
                non_power_of_two_factors = mathtools.remove_powers_of_two(
                    split_point_in_measure.denominator)
                non_power_of_two_factors = mathtools.factors(
                    non_power_of_two_factors)
                non_power_of_two_product = 1
                for non_power_of_two_factor in non_power_of_two_factors:
                    non_power_of_two_product *= non_power_of_two_factor
                measuretools.scale_measure_denominator_and_adjust_measure_contents(
                    measure, non_power_of_two_product)
                # rederive duration crosses with possibly new measure contents
                cross_offset = self._get_timespan().start_offset + offset
                duration_crossing_descendants = []
                for descendant in self._select_descendants():
                    start_offset = descendant._get_timespan().start_offset
                    stop_offset = descendant._get_timespan().stop_offset
                    if start_offset < cross_offset < stop_offset:
                        duration_crossing_descendants.append(descendant)
        elif 1 < len(measures):
            raise Exception('measures can not nest.')
        # any duration-crossing leaf will be at end of list
        bottom = duration_crossing_descendants[-1]
        did_split_leaf = False
        # if split point necessitates leaf split
        if isinstance(bottom, leaftools.Leaf):
            assert isinstance(bottom, leaftools.Leaf)
            did_split_leaf = True
            split_point_in_bottom = \
                global_split_point - bottom._get_timespan().start_offset
            left_list, right_list = bottom._split_by_duration(
                split_point_in_bottom,
                fracture_spanners=fracture_spanners,
                tie_split_notes=tie_split_notes,
                )
            right = right_list[0]
            leaf_right_of_split = right
            leaf_left_of_split = left_list[-1]
            duration_crossing_containers = duration_crossing_descendants[:-1]
            if not len(duration_crossing_containers):
                return left_list, right_list
        # if split point falls between leaves
        # then find leaf to immediate right of split point
        # in order to start upward crawl through duration-crossing containers
        else:
            duration_crossing_containers = duration_crossing_descendants[:]
            for leaf in iterationtools.iterate_leaves_in_expr(bottom):
                if leaf._get_timespan().start_offset == global_split_point:
                    leaf_right_of_split = leaf
                    leaf_left_of_split = \
                        leaftools.get_nth_leaf_in_logical_voice_from_leaf(
                        leaf_right_of_split, -1)
                    break
            else:
                message = 'can not split empty container {!r}.'
                raise ContainmentError(message.format(bottom))
        # find component to right of split that is also immediate child of 
        # last duration-crossing container
        for component in \
            leaf_right_of_split._select_parentage(include_self=True):
            if component._parent is duration_crossing_containers[-1]:
                highest_level_component_right_of_split = component
                break
        else:
            raise ValueError('should we be able to get here?')
        # crawl back up through duration-crossing containers and 
        # fracture spanners if requested
        if fracture_spanners:
            start_offset = leaf_right_of_split._get_timespan().start_offset
            for parent in leaf_right_of_split._select_parentage():
                if parent._get_timespan().start_offset == start_offset:
                    spannertools.fracture_spanners_attached_to_component(
                        parent, direction=Left)
                if parent is component:
                    break
        # crawl back up through duration-crossing containers and split each
        previous = highest_level_component_right_of_split
        for duration_crossing_container in reversed(duration_crossing_containers):
            assert isinstance(
                duration_crossing_container, containertools.Container)
            i = duration_crossing_container.index(previous)
            left, right = duration_crossing_container._split_at_index(
                i,
                fracture_spanners=fracture_spanners,
                )
            previous = right
        # NOTE: If tie chain here is convenience, then fusing is good.
        #       If tie chain here is user-given, then fusing is less good.
        #       Maybe later model difference between user tie chains and not.
        left_tie_chain = leaf_left_of_split._select_tie_chain()
        right_tie_chain = leaf_right_of_split._select_tie_chain()
        leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(left_tie_chain)
        leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(right_tie_chain)
        # reapply tie here if crawl above killed tie applied to leaves
        if did_split_leaf:
            if tie_split_notes and isinstance(leaf_left_of_split, notetools.Note):
                if leaf_left_of_split._select_parentage().root is \
                    leaf_right_of_split._select_parentage().root:
                    leaves_around_split = (leaf_left_of_split, leaf_right_of_split)
                    selection = selectiontools.ContiguousLeafSelection(
                        leaves_around_split)
                    selection._attach_tie_spanner_to_leaf_pair()
        # return pair of left and right list-wrapped halves of container
        return ([left], [right])

    def _update_later(self, offsets=False, offsets_in_seconds=False):
        assert offsets or offsets_in_seconds
        for component in self._select_parentage(include_self=True):
            if offsets:
                component._offsets_are_current = False
            elif offsets_in_seconds:
                component._offsets_in_seconds_are_current = False

    def _update_now(
        self, 
        offsets=False, 
        offsets_in_seconds=False, 
        marks=False,
        ):
        from abjad.tools import updatetools
        return updatetools.UpdateManager._update_now(
            self,
            offsets=offsets,
            offsets_in_seconds=offsets_in_seconds,
            marks=marks,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        '''Lilypond format of component.

        Returns string.
        '''
        self._update_now(marks=True)
        return self._format_component()

    @property
    def override(self):
        r'''LilyPond grob override component plug-in.

        Returns LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = \
                lilypondproxytools.LilyPondGrobOverrideComponentPlugIn()
        return self._override

    @property
    def set(self):
        r'''LilyPond context setting component plug-in.

        Returns LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = \
                lilypondproxytools.LilyPondContextSettingComponentPlugIn()
        return self._set

    @property
    def storage_format(self):
        r'''Storage format of component.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PUBLIC METHODS ###

    def select(self, sequential=False):
        r'''Selects component.

        Returns component selection when `sequential` is false.

        Returns sequential selection when `sequential` is true.
        '''
        if not sequential:
            return selectiontools.FreeComponentSelection(music=self)
        else:
            return selectiontools.SliceSelection(music=self)
