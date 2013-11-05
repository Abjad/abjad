# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import lilypondproxytools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import timespantools
from abjad.tools.functiontools import override
from abjad.tools.abctools import AbjadObject


class Component(AbjadObject):
    r'''Any score component.

    Notes, rests, chords, tuplets, voices, staves
    and scores are all components.
    '''

    ### CLASS VARIABLES ###

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

    @abc.abstractmethod
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
        r'''Copies component with marks but without children of component
        or spanners attached to component.

        Returns new component.
        '''
        return self._copy_with_marks_but_without_children_or_spanners()

    def __format__(self, format_specification=''):
        r'''Formats component.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return self.storage_format
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return ()

    def __mul__(self, n):
        r'''Copies component `n` times and detaches spanners.

        Returns list of new components.
        '''
        from abjad.tools.functiontools import mutate
        from abjad.tools import iterationtools
        result = mutate(self).copy(n=n)
        for component in iterationtools.iterate_components_in_expr(result):
            for spanner in component._get_spanners():
                spanner.detach()
        if isinstance(result, type(self)):
            result = [result]
        else:
            result = list(result)
        result = selectiontools.Selection(result)
        return result

    def __rmul__(self, n):
        r'''Copies component `n` times and detach spanners.

        Returns list of new components.
        '''
        return self * n

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._format_component(pieces=True)

    @property
    def _lilypond_format(self):
        self._update_now(marks=True)
        return self._format_component()

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
        from abjad.tools.functiontools import attach
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(override(self))
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(self.set)
        for mark in self._get_marks():
            new_mark = copy.copy(mark)
            attach(new_mark, new)
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

    # TODO: remove scale_contents keyword
    def _extract(self, scale_contents=None):
        from abjad.tools import selectiontools
        selection = selectiontools.SliceSelection([self])
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        music_list = list(getattr(self, '_music', ()))
        parent.__setitem__(slice(start, stop + 1), music_list)
        return self

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
        format_contributions = \
            formattools.LilyPondFormatManager.get_all_format_contributions(
                self)
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

    def _get_components(self, component_classes=None, include_self=True):
        from abjad.tools import iterationtools
        expr = self
        if include_self:
            expr = [self]
        components = iterationtools.iterate_components_in_expr(
            expr, component_class=component_classes)
        return selectiontools.Selection(components)

    def _get_contents(self, include_self=True):
        result = []
        if include_self:
            result.append(self)
        result.extend(getattr(self, '_music', []))
        result = selectiontools.SliceSelection(result)
        return result

    def _get_descendants(
        self,
        include_self=True,
        ):
        return selectiontools.Descendants(
            self,
            include_self=include_self,
            )

    def _get_descendants_starting_with(self):
        from abjad.tools import scoretools
        result = []
        result.append(self)
        if isinstance(self, scoretools.Container):
            if self.is_simultaneous:
                for x in self:
                    result.extend(x._get_descendants_starting_with())
            elif self:
                result.extend(self[0]._get_descendants_starting_with())
        return result

    def _get_descendants_stopping_with(self):
        from abjad.tools import scoretools
        result = []
        result.append(self)
        if isinstance(self, scoretools.Container):
            if self.is_simultaneous:
                for x in self:
                    result.extend(x._get_descendants_stopping_with())
            elif self:
                result.extend(self[-1]._get_descendants_stopping_with())
        return result

    def _get_duration(self, in_seconds=False):
        if in_seconds:
            return self._duration_in_seconds
        else:
            parentage = self._get_parentage(include_self=False)
            return parentage.prolation * self._preprolated_duration

    def _get_effective_context_mark(self, context_mark_classes=None):
        from abjad.tools import marktools
        from abjad.tools import datastructuretools
        from abjad.tools import scoretools
        # do special things for time signature marks
        if context_mark_classes == marktools.TimeSignatureMark:
            if isinstance(self, scoretools.Measure):
                if self._has_mark(marktools.TimeSignatureMark):
                    return self._get_mark(marktools.TimeSignatureMark)
        # updating marks of entire score tree if necessary
        self._update_now(marks=True)
        # gathering candidate marks
        candidate_marks = datastructuretools.SortedCollection(
            key=lambda x: x.start_component._get_timespan().start_offset)
        for parent in self._get_parentage(include_self=True):
            parent_marks = parent._dependent_context_marks
            for mark in parent_marks:
                if isinstance(mark, context_mark_classes):
                    if mark.effective_context is not None:
                        candidate_marks.insert(mark)
                    elif isinstance(mark, marktools.TimeSignatureMark):
                        if isinstance(
                            mark.start_component, scoretools.Measure):
                            candidate_marks.insert(mark)
        # elect most recent candidate mark
        if candidate_marks:
            try:
                start_offset = self._get_timespan().start_offset
                return candidate_marks.find_le(start_offset)
            except ValueError:
                pass

    def _get_effective_staff(self):
        from abjad.tools import marktools
        from abjad.tools import scoretools
        staff_change_mark = self._get_effective_context_mark(
            marktools.StaffChangeMark)
        if staff_change_mark is not None:
            effective_staff = staff_change_mark.staff
        else:
            parentage = self._get_parentage()
            effective_staff = parentage.get_first(scoretools.Staff)
        return effective_staff

    def _get_format_contributions_for_slot(self, n, format_contributions=None):
        if format_contributions is None:
            format_contributions = \
                formattools.LilyPondFormatManager.get_all_format_contributions(
                    self)
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
            n = slots[n - 1]
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

    def _get_lineage(self):
        return selectiontools.Lineage(self)

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
        assert mathtools.is_integer_equivalent_expr(n)

        def next(component):
            if component is not None:
                for parent in component._get_parentage(include_self=True):
                    next_sibling = parent._get_sibling(1)
                    if next_sibling is not None:
                        return next_sibling

        def previous(component):
            if component is not None:
                for parent in component._get_parentage(include_self=True):
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

    def _get_parentage(self, include_self=True):
        return selectiontools.Parentage(self, include_self=include_self)

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

    def _get_vertical_moment(self, governor=None):
        offset = self._get_timespan().start_offset
        if governor is None:
            governor = self._get_parentage().root
        return selectiontools.VerticalMoment(governor, offset)

    def _get_vertical_moment_at(self, offset):
        return selectiontools.VerticalMoment(self, offset)

    def _has_mark(self, mark_classes=None):
        marks = self._get_marks(mark_classes=mark_classes)
        return bool(marks)

    def _has_spanner(self, spanner_classes=None):
        spanners = self._get_spanners(spanner_classes=spanner_classes)
        return bool(spanners)

    def _is_immediate_temporal_successor_of(self, component):
        temporal_successors = []
        current = self
        while current is not None:
            next_sibling = current._get_sibling(1)
            if next_sibling is None:
                current = current._parent
            else:
                temporal_successors = \
                    next_sibling._get_descendants_starting_with()
                break
        return component in temporal_successors

    def _move_marks(self, recipient_component):
        from abjad.tools.functiontools import attach
        result = []
        for mark in self._get_marks():
            result.append(attach(mark, recipient_component))
        return tuple(result)

    # TODO: eventually reimplement as a keyword option to remove()
    def _remove_and_shrink_durated_parent_containers(self):
        from abjad.tools import marktools
        from abjad.tools import scoretools
        from abjad.tools.functiontools import attach
        prolated_leaf_duration = self._get_duration()
        parentage = self._get_parentage(include_self=False)
        prolations = parentage._prolations
        current_prolation, i = durationtools.Duration(1), 0
        parent = self._parent
        while parent is not None and not parent.is_simultaneous:
            current_prolation *= prolations[i]
            if isinstance(parent, scoretools.FixedDurationTuplet):
                candidate_new_parent_dur = (parent.target_duration -
                    current_prolation * self.written_duration)
                if durationtools.Duration(0) < candidate_new_parent_dur:
                    parent.target_duration = candidate_new_parent_dur
            elif isinstance(parent, scoretools.Measure):
                parent_time_signature = parent._get_mark(
                    marktools.TimeSignatureMark)
                old_prolation = parent_time_signature.implied_prolation
                naive_time_signature = (
                    parent_time_signature.duration - prolated_leaf_duration)
                better_time_signature = mathtools.NonreducedFraction(
                    naive_time_signature)
                better_time_signature = better_time_signature.with_denominator(
                    parent_time_signature.denominator)
                better_time_signature = marktools.TimeSignatureMark(
                    better_time_signature)
                for mark in parent._get_marks(marktools.TimeSignatureMark):
                    mark.detach()
                attach(better_time_signature, parent)
                parent_time_signature = parent._get_mark(
                    marktools.TimeSignatureMark)
                #new_denominator = parent_time_signature.denominator
                new_prolation = parent_time_signature.implied_prolation
                adjusted_prolation = old_prolation / new_prolation
                for x in parent:
                    if isinstance(x, scoretools.FixedDurationTuplet):
                        x.target_duration *= adjusted_prolation
                    else:
                        if adjusted_prolation != 1:
                            new_target = \
                                x._preprolated_duration * adjusted_prolation
                            scoretools.FixedDurationTuplet(new_target, [x])
            parent = parent._parent
            i += 1
        parentage = self._get_parentage(include_self=False)
        parent = self._parent
        if parent:
            index = parent.index(self)
            del(parent[index])
        for x in parentage:
            if not len(x):
                x._extract()
            else:
                break

    def _remove_from_parent(self):
        self._update_later(offsets=True)
        if self._parent is not None:
            self._parent._music.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self._get_parentage(include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    for component in name_dictionary[name]:
                        named_children[name].remove(component)
                    if not named_children[name]:
                        del named_children[name]

    def _restore_named_children_to_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self._get_parentage(include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].extend(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

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
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        assert all(isinstance(x, scoretools.Component) for x in components)
        selection = selectiontools.ContiguousSelection(self)
        if direction is Right:
            if grow_spanners:
                insert_offset = self._get_timespan().stop_offset
                receipt = selection._get_dominant_spanners()
                for spanner, index in receipt:
                    insert_component = None
                    for component in spanner:
                        start_offset = component._get_timespan().start_offset
                        if start_offset == insert_offset:
                            insert_component = component
                            break
                    if insert_component is not None:
                        insert_index = spanner.index(insert_component)
                    else:
                        insert_index = len(spanner)
                    for component in reversed(components):
                        spanner._insert(insert_index, component)
                        component._spanners.add(spanner)
            selection = self.select(sequential=True)
            parent, start, stop = \
                selection._get_parent_and_start_stop_indices()
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
                offset = self._get_timespan().start_offset
                receipt = selection._get_dominant_spanners()
                for spanner, x in receipt:
                    for component in spanner:
                        if component._get_timespan().start_offset == offset:
                            index = spanner.index(component)
                            break
                    else:
                        message = 'no component in spanner at offset'
                        raise SpannerPopulationError(message)
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

    def _update_later(self, offsets=False, offsets_in_seconds=False):
        assert offsets or offsets_in_seconds
        for component in self._get_parentage(include_self=True):
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
        from abjad.tools import systemtools
        return systemtools.UpdateManager._update_now(
            self,
            offsets=offsets,
            offsets_in_seconds=offsets_in_seconds,
            marks=marks,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def set(self):
        r'''LilyPond context setting component plug-in.

        Returns LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = \
                lilypondproxytools.LilyPondSettingManager()
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
            return selectiontools.Selection(music=self)
        else:
            return selectiontools.SliceSelection(music=self)
