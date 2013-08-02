# -*- encoding: utf-8 -*-
import abc
import copy
import fractions
from abjad.tools import durationtools
from abjad.tools import formattools
from abjad.tools import lilypondproxytools
from abjad.tools import mathtools
from abjad.tools import timespantools
from abjad.tools.abctools import AbjadObject


class Component(AbjadObject):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_duration', 
        '_is_forbidden_to_update', 
        '_marks_are_current',
        '_dependent_context_marks',
        '_start_marks',
        '_offset', 
        '_offset_values_in_seconds_are_current', 
        '_override', 
        '_parent',
        '_prolated_offset_values_are_current', 
        '_set', 
        '_spanners',
        '_start_offset', 
        '_start_offset_in_seconds', 
        '_stop_offset', 
        '_stop_offset_in_seconds',
        '_timespan',
        'lilypond_file',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._is_forbidden_to_update = False
        self._marks_are_current = False
        self._dependent_context_marks = list()
        self._start_marks = list()
        self._offset_values_in_seconds_are_current = False
        self._parent = None
        self._prolated_offset_values_are_current = False
        self._spanners = set([])
        self._start_offset = None
        self._start_offset_in_seconds = None
        self._stop_offset = None
        self._stop_offset_in_seconds = None
        self._timespan = timespantools.Timespan()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        '''Copy component with marks but without children or spanners.

        Return newly created component.
        '''
        return self._copy_with_marks_but_without_children_or_spanners()

    def __getnewargs__(self):
        return ()

    def __mul__(self, n):
        '''Copy `n` times and detach spanners.

        Return list of newly created components.
        '''
        from abjad.tools import componenttools
        return componenttools.copy_components_and_detach_spanners([self], n)

    def __rmul__(self, n):
        '''Copy `n` times and detach spanners.

        Return list of newly created components.
        '''
        return self * n

    ### PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._format_component(pieces=True)

    @property
    def _id_string(self):
        lhs = self._class_name
        rhs = getattr(self, 'name', None) or id(self)
        return '{}-{!r}'.format(lhs, rhs)

#    @property
#    def _prolation(self):
#        products = [fractions.Fraction(1)] + self._prolations
#        products = mathtools.cumulative_products(products)
#        return products[-1]

#    @property
#    def _prolations(self):
#        prolations = []
#        parent = self._parent
#        default = durationtools.Multiplier(1)
#        while parent is not None:
#            prolation = getattr(parent, 'implied_prolation', default)
#            prolations.append(prolation)
#            parent = parent._parent
#        return prolations

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
        for mark in self.get_marks():
            new_mark = copy.copy(mark)
            new_mark.attach(new)
        return new

    def _detach_marks(
        self,
        mark_classes=None,
        ):
        marks = []
        for mark in self.get_marks(mark_classes=mark_classes):
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

    def _get_namesake(self, n):
        from abjad.tools import iterationtools
        if 0 <= n:
            for i, namesake in enumerate(
                iterationtools.iterate_namesakes_from_component(self)):
                if i == n:
                    return namesake
        else:
            n = abs(n)
            for i, namesake in enumerate(
                iterationtools.iterate_namesakes_from_component(
                    self, reverse=True)):
                if i == n:
                    return namesake

    def _get_sibling(self, n):
        if n == 0:
            return self
        elif 0 < n:
            if self._parent is not None:
                if not self._parent.is_parallel:
                    index = self._parent.index(self)
                    if index + n < len(self._parent):
                        return self._parent[index + n]
        elif n < 0:
            if self._parent is not None:
                if not self._parent.is_parallel:
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
        for spanner in self.spanners:
            if isinstance(spanner, spanner_classes):
                spanners.add(spanner)
        return spanners

    def _has_mark(self, mark_classes=None):
        marks = self.get_marks(mark_classes=mark_classes)
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
        for mark in self.get_marks():
            result.append(mark.attach(recipient_component))
        return tuple(result)

    def _remove_from_parent(self):
        self._mark_entire_score_tree_for_later_update('prolated')
        if self._parent is not None:
            self._parent._music.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        from abjad.tools import componenttools
        if self._parent is not None and name_dictionary:
            for parent in self.select_parentage(include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    for component in name_dictionary[name]:
                        named_children[name].remove(component)
                    if not named_children[name]:
                        del named_children[name]

    def _restore_named_children_to_parentage(self, name_dictionary):
        from abjad.tools import componenttools
        if self._parent is not None and name_dictionary:
            for parent in self.select_parentage(include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].extend(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

    def _select_descendants_starting_with(self):
        from abjad.tools import containertools
        result = []
        result.append(self)
        if isinstance(self, containertools.Container):
            if self.is_parallel:
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
            if self.is_parallel:
                for x in self:
                    result.extend(x._select_descendants_stopping_with())
            elif self:
                result.extend(self[-1]._select_descendants_stopping_with())
        return result

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
        self._mark_entire_score_tree_for_later_update('prolated')

    ### UPDATE METHODS ###

    def _allow_component_update(self):
        self._is_forbidden_to_update = False

    def _forbid_component_update(self):
        self._is_forbidden_to_update = True

    def _get_score_tree_state_flags(self):
        prolated_offset_values_are_current = True
        marks_are_current = True
        offset_values_in_seconds_are_current = True
        parentage = self.select_parentage()
        for component in parentage:
            if prolated_offset_values_are_current and \
                not component._prolated_offset_values_are_current:
                prolated_offset_values_are_current = False
            if marks_are_current and not component._marks_are_current:
                marks_are_current = False
            if offset_values_in_seconds_are_current and \
                not component._offset_values_in_seconds_are_current:
                offset_values_in_seconds_are_current = False
        return (prolated_offset_values_are_current,
            marks_are_current,
            offset_values_in_seconds_are_current)

    def _iterate_score_components_depth_first(self):
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        kwargs = {
            'capped': True, 
            'unique': True, 
            'forbid': None, 
            'direction': 'left',
            }
        parentage = self.select_parentage()
        components = iterationtools.iterate_components_depth_first(
            parentage.root, **kwargs)
        return components

    def _mark_entire_score_tree_for_later_update(self, value):
        r'''Call immediately after modifying score tree.

        Only dynamic measures mark time signature for udpate.
        '''
        for component in self.select_parentage(include_self=True):
            if value == 'prolated':
                component._prolated_offset_values_are_current = False
            elif value == 'seconds':
                component._offset_values_in_seconds_are_current = False
            else:
                raise ValueError('unknown value: "%s"' % value)
            if hasattr(component, '_time_signature_is_current'):
                component._time_signature_is_current = False

    def _update_leaf_indices_and_measure_numbers_in_score_tree(self):
        r'''Called only when updating prolated offset of score components.
        No separate state flags for leaf indices or measure numbers.
        '''
        from abjad.tools import componenttools
        from abjad.tools import contexttools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools import measuretools
        parentage = self.select_parentage()
        score_root = parentage.root
        if isinstance(score_root, contexttools.Context):
            for context in \
                iterationtools.iterate_contexts_in_expr(score_root):
                for leaf_index, leaf in enumerate(
                    iterationtools.iterate_leaves_in_expr(context)):
                    leaf._leaf_index = leaf_index
                for measure_index, measure in enumerate(
                    iterationtools.iterate_measures_in_expr(context)):
                    measure_number = measure_index + 1
                    measure._measure_number = measure_number
        else:
            for leaf_index, leaf in enumerate(
                iterationtools.iterate_leaves_in_expr(score_root)):
                leaf._leaf_index = leaf_index
            for measure_index, measure in enumerate(
                iterationtools.iterate_measures_in_expr(score_root)):
                measure_number = measure_index + 1
                measure._measure_number = measure_number

    def _update_marks_of_entire_score_tree(self):
        r'''Updating marks does not cause prolated offset values to update.
        On the other hand, getting effective mark causes prolated offset values
        to update when at least one mark of appropriate type attaches to score.
        '''
        components = self._iterate_score_components_depth_first()
        for component in components:
            for mark in component._start_marks:
                if hasattr(mark, '_update_effective_context'):
                    mark._update_effective_context()
            component._marks_are_current = True

    def _update_marks_of_entire_score_tree_if_necessary(self):
        r'''Call immediately before reading effective mark.
        '''
        if self._is_forbidden_to_update:
            return
        state_flags = self._get_score_tree_state_flags()
        marks_are_current = state_flags[1]
        if not marks_are_current:
            self._update_marks_of_entire_score_tree()
            self._update_offset_values_in_seconds_of_entire_score_tree()

    def _update_offset_values_in_seconds_of_entire_score_tree(self):
        from abjad.tools import offsettools
        components = self._iterate_score_components_depth_first()
        for component in components:
            offsettools.update_offset_values_of_component_in_seconds(component)
            component._offset_values_in_seconds_are_current = True

    def _update_offset_values_in_seconds_of_entire_score_tree_if_necessary(
        self):
        if self._is_forbidden_to_update:
            return
        state_flags = self._get_score_tree_state_flags()
        offset_values_in_seconds_are_current = state_flags[2]
        if not offset_values_in_seconds_are_current:
            self._update_offset_values_in_seconds_of_entire_score_tree()

    def _update_prolated_offset_values_of_entire_score_tree(self):
        r'''Updating prolated offset values does NOT update marks.
        Updating prolated offset values does NOT update offset values 
        in seconds.
        '''
        from abjad.tools import offsettools
        components = self._iterate_score_components_depth_first()
        for component in components:
            offsettools.update_offset_values_of_component(component)
            component._prolated_offset_values_are_current = True

    def _update_prolated_offset_values_of_entire_score_tree_if_necessary(self):
        if self._is_forbidden_to_update:
            return
        state_flags = self._get_score_tree_state_flags()
        prolated_offset_values_are_current = state_flags[0]
        if not prolated_offset_values_are_current:
            self._update_prolated_offset_values_of_entire_score_tree()
            self._update_leaf_indices_and_measure_numbers_in_score_tree()

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        '''Lilypond format.

        Return string.
        '''
        self._update_marks_of_entire_score_tree_if_necessary()
        return self._format_component()

    @property
    def override(self):
        r'''Reference to LilyPond grob override component plug-in.
        '''
        if not hasattr(self, '_override'):
            self._override = \
                lilypondproxytools.LilyPondGrobOverrideComponentPlugIn()
        return self._override

    @property
    def set(self):
        r'''Reference LilyPond context setting component plug-in.
        '''
        if not hasattr(self, '_set'):
            self._set = \
                lilypondproxytools.LilyPondContextSettingComponentPlugIn()
        return self._set

    @property
    def spanners(self):
        r'''Reference to unordered set of spanners attached 
        to component.
        '''
        return set(self._spanners)

    @property
    def timespan(self):
        r'''Timespan of component.
        '''
        self._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._timespan

    @property
    def timespan_in_seconds(self):
        r'''Timespan of component in seconds.
        '''
        self._update_offset_values_in_seconds_of_entire_score_tree_if_necessary()
        if self._start_offset_in_seconds is None:
            raise MissingTempoError
        return timespantools.Timespan(
            start_offset=self._start_offset_in_seconds, 
            stop_offset=self._stop_offset_in_seconds,
            )

    ### PUBLIC METHODS ###

    def extend_in_parent(
        self,
        new_components,
        direction=Right,
        grow_spanners=True,
        ):
        '''Extend `new_components` in parent of component.

        Return list of component followed by `new_components`.
        '''
        from abjad.tools import componenttools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        assert componenttools.all_are_components(new_components)
        if direction == Right:
            if grow_spanners:
                insert_offset = self.timespan.stop_offset
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
                    for new_component in reversed(new_components):
                        spanner._insert(insert_index, new_component)
                        new_component._spanners.add(spanner)
            selection = self.select(sequential=True)
            parent, start, stop = selection._get_parent_and_start_stop_indices()
            if parent is not None:
                if grow_spanners:
                    for new_component in reversed(new_components):
                        new_component._set_parent(parent)
                        parent._music.insert(start + 1, new_component)
                else:
                    after = stop + 1
                    parent.__setitem__(slice(after, after), new_components)
            return [self] + new_components
        else:
            if grow_spanners:
                offset = self.timespan.start_offset
                receipt = spannertools.get_spanners_that_dominate_components(
                    [self])
                for spanner, x in receipt:
                    index = \
                        spannertools.find_index_of_spanner_component_at_score_offset(
                        spanner, offset)
                    for new_component in reversed(new_components):
                        spanner._insert(index, new_component)
                        new_component._spanners.add(spanner)
            selection = self.select(sequential=True)
            parent, start, stop = selection._get_parent_and_start_stop_indices()
            if parent is not None:
                if grow_spanners:
                    for new_component in reversed(new_components):
                        new_component._set_parent(parent)
                        parent._music.insert(start, new_component)
                else:
                    parent.__setitem__(slice(start, start), new_components)
            return new_components + [self]


    def get_annotation_value(self, annotation_name, default=None):
        r'''Get value of `annotation_name`:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> marktools.Annotation('special dictionary', {})(staff[0])
            Annotation('special dictionary', {})(c'8)

        ::

            >>> staff[0].get_annotation_value('special dictionary')
            {}

        Return arbitrary value of annotation.

        Return `default` when no `annotation_name` is attached.

        Raise exception when more than one `annotation_name` is attached.
        '''
        from abjad.tools import marktools
        annotations = self.get_marks(marktools.Annotation)
        if not annotations:
            return default
        with_correct_name = []
        for annotation in annotations:
            if annotation.name == annotation_name:
                with_correct_name.append(annotation)
        if not with_correct_name:
            return default
        if 1 < len(with_correct_name):
            raise Exception('more than one annotation.')
        annotation_value = with_correct_name[0].value
        return annotation_value

    def get_duration(self, in_seconds=False):
        '''Get duration.

        Return duration.
        '''
        if in_seconds:
            return self._duration_in_seconds
        else:
            parentage = self.select_parentage(include_self=False)
            return parentage.prolation * self._preprolated_duration

    def get_effective_context_mark(
        self,
        context_mark_classes=None,
        ):
        r'''Get effective context mark of `context_mark_class` from 
        `component`:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> contexttools.TimeSignatureMark((4, 8))(staff)
            TimeSignatureMark((4, 8))(Staff{4})

        ::

            >>> f(staff)
            \new Staff {
                \time 4/8
                c'8
                d'8
                e'8
                f'8
            }

        ::

            >>> staff[0].get_effective_context_mark(
            ...     contexttools.TimeSignatureMark)
            TimeSignatureMark((4, 8))(Staff{4})

        Return context mark or none.
        '''
        from abjad.tools import contexttools
        from abjad.tools import datastructuretools
        from abjad.tools import measuretools
        # do special things for time signature marks
        if context_mark_classes == contexttools.TimeSignatureMark:
            if isinstance(self, measuretools.Measure):
                if not getattr(self, '_time_signature_is_current', True):
                    self._update_time_signature()
                if self._has_mark(contexttools.TimeSignatureMark):
                    return self.get_mark(contexttools.TimeSignatureMark)
        # updating marks of entire score tree if necessary
        self._update_marks_of_entire_score_tree_if_necessary()
        # gathering candidate marks
        candidate_marks = datastructuretools.SortedCollection(
            key=lambda x: x.start_component.timespan.start_offset)
        for parent in self.select_parentage(include_self=True):
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
                return candidate_marks.find_le(self.timespan.start_offset)
            except ValueError:
                pass

    def get_effective_staff(self):
        r'''Get effective staff.

        Return staff or none.
        '''
        from abjad.tools import contexttools
        from abjad.tools import stafftools
        staff_change_mark = self.get_effective_context_mark(
            contexttools.StaffChangeMark)
        if staff_change_mark is not None:
            effective_staff = staff_change_mark.staff
        else:
            parentage = self.select_parentage()
            effective_staff = parentage.get_first(stafftools.Staff)
        return effective_staff

    def get_mark(
        self,
        mark_classes=None,
        ):
        '''Get mark.

        Raise exception when no mark of `mark_classes` is attached.

        Return mark.
        '''
        marks = self.get_marks(mark_classes=mark_classes)
        if not marks:
            raise MissingMarkError
        elif 1 < len(marks):
            raise ExtraMarkError
        else:
            return marks[0]

    def get_marks(
        self,
        mark_classes=None,
        ):
        '''Get marks.

        Return list.
        '''
        from abjad.tools import marktools
        mark_classes = mark_classes or (marktools.Mark,)
        if not isinstance(mark_classes, tuple):
            mark_classes = (mark_classes,)
        marks = []
        for mark in self._start_marks:
            if isinstance(mark, mark_classes):
                marks.append(mark)
        return tuple(marks)

    def get_markup(
        self,
        direction=None,
        ):
        r"""Get markup attached to `component`:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> slur = spannertools.SlurSpanner(staff[:])

        ::

            >>> markuptools.Markup('foo')(staff[0])
            Markup(('foo',))(c'8)

        ::

            >>> markuptools.Markup('bar')(staff[0])
            Markup(('bar',))(c'8)

        .. doctest::

            >>> f(staff)
            \new Staff {
                c'8 (
                    - \markup {
                        \column
                            {
                                foo
                                bar
                            }
                        }
                d'8
                e'8
                f'8 )
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> staff[0].get_markup()
            (Markup(('foo',))(c'8), Markup(('bar',))(c'8))

        Get markup by direction:

        ::

            >>> chord = Chord([-11, 2, 5], (1, 4))

        ::

            >>> markuptools.Markup('UP', Up)(chord)
            Markup(('UP',), direction=Up)(<cs d' f'>4)

        ::

            >>> markuptools.Markup('DOWN', Down)(chord)
            Markup(('DOWN',), direction=Down)(<cs d' f'>4)

        ::

            >>> show(chord) # doctest: +SKIP
            
        ::

            >>> chord.get_markup(direction=Up)
            (Markup(('UP',), direction=Up)(<cs d' f'>4),)
            
        ::

            >>> chord.get_markup(direction=Down)
            (Markup(('DOWN',), direction=Down)(<cs d' f'>4),)

        Return tuple of zero or more markup objects.
        """
        from abjad.tools import markuptools
        markup = self.get_marks(mark_classes=(markuptools.Markup,))
        if direction is Up:
            return tuple(x for x in markup if x.direction is Up)
        elif direction is Down:
            return tuple(x for x in markup if x.direction is Down)
        return markup

    def select(self, sequential=False):
        r'''Select component.

        Return component selection when `sequential` is false.

        Return sequential selection when `sequential` is true.
        '''
        from abjad.tools import selectiontools
        if not sequential:
            return selectiontools.ComponentSelection(music=self)
        else:
            return selectiontools.SequentialSelection(music=self)

    def select_components(self, component_classes=None, include_self=True):
        r'''Select `component_classes` in component.

        Return component selection.
        '''
        from abjad.tools import iterationtools
        from abjad.tools import selectiontools
        expr = self
        if include_self:
            expr = [self]
        components = iterationtools.iterate_components_in_expr(
            expr, component_class=component_classes)
        return selectiontools.ComponentSelection(components)

    def select_contents(self, include_self=True):
        r'''Select contents of component.

        Return selection.
        '''
        from abjad.tools import selectiontools
        result = []
        if include_self:
            result.append(self)
        result.extend(getattr(self, '_music', []))
        result = selectiontools.SequentialSelection(result)
        return result

    def select_descendants(
        self,
        cross_offset=None,
        include_self=True,
        ):
        r'''Select descendants.
        '''
        from abjad.tools import componenttools
        return componenttools.Descendants(
            self,
            cross_offset=cross_offset,
            include_self=include_self,
            )

    def select_lineage(self):
        r'''Select lineage.
        '''
        from abjad.tools import componenttools
        return componenttools.Lineage(self)

    def select_parentage(self, include_self=True):
        r'''Select parentage.
        '''
        from abjad.tools import componenttools
        return componenttools.Parentage(self, include_self=include_self)

    def select_vertical_moment(self, governor=None):
        r'''Select vertical moment starting with component.
        '''
        from abjad.tools import componenttools
        offset = self.timespan.start_offset
        if governor is None:
            governor = self.select_parentage().root
        return componenttools.VerticalMoment(governor, offset)

    def select_vertical_moment_at(self, offset):
        r'''Select vertical moment at `offset`.
        '''
        from abjad.tools import componenttools
        return componenttools.VerticalMoment(self, offset)
