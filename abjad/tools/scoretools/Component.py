# -*- encoding: utf-8 -*-
import abc
import copy
import types
from abjad.tools import durationtools
from abjad.tools import systemtools
from abjad.tools import lilypondnametools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import timespantools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import contextualize
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import override
from abjad.tools.abctools import AbjadObject


class Component(AbjadObject):
    r'''A score component.

    Notes, rests, chords, tuplets, voices, staves
    and scores are all components.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_after_grace',
        '_dependent_expressions',
        '_grace',
        '_indicators',
        '_indicators_are_current',
        '_is_forbidden_to_update',
        '_offsets_are_current',
        '_offsets_in_seconds_are_current',
        '_override',
        '_parent',
        '_set',
        '_spanners',
        '_start_offset',
        '_start_offset_in_seconds',
        '_stop_offset',
        '_stop_offset_in_seconds',
        '_timespan',
        )

    _is_counttime_component = False

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._after_grace = None
        self._dependent_expressions = []
        self._grace = None
        self._indicators = []
        self._indicators_are_current = False
        self._is_forbidden_to_update = False
        self._offsets_are_current = False
        self._offsets_in_seconds_are_current = False
        self._override = None
        self._parent = None
        self._set = None
        self._spanners = set()
        self._start_offset = None
        self._start_offset_in_seconds = None
        self._stop_offset = None
        self._stop_offset_in_seconds = None
        self._timespan = timespantools.Timespan()

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies component with indicators but without children of component
        or spanners attached to component.

        Returns new component.
        '''
        return self._copy_with_indicators_but_without_children_or_spanners()

    def __format__(self, format_specification=''):
        r'''Formats component.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return ()

    def __illustrate__(self):
        r'''Illustrates component.

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(self)
        lilypond_file.header_block.tagline = markuptools.Markup('""')
        return lilypond_file

    def __mul__(self, n):
        r'''Copies component `n` times and detaches spanners.

        Returns list of new components.
        '''
        from abjad.tools import spannertools
        result = mutate(self).copy(n=n)
        for component in iterate(result).by_class():
            detach(spannertools.Spanner, component)
        if isinstance(result, type(self)):
            result = [result]
        else:
            result = list(result)
        result = selectiontools.Selection(result)
        return result

    def __repr__(self):
        '''Gets interpreter representation of leaf.

        Returns string.
        '''
        return systemtools.StorageFormatManager.get_repr_format(self)

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
        self._update_now(indicators=True)
        return self._format_component()

    @property
    def _repr_specification(self):
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            body_text=repr(self._compact_representation),
            positional_argument_values=(),
            )

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

    def _copy_with_children_and_indicators_but_without_spanners(self):
        return self._copy_with_indicators_but_without_children_or_spanners()

    def _copy_with_indicators_but_without_children_or_spanners(self):
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(override(self))
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(contextualize(self))
        for indicator in self._get_indicators():
            new_indicator = copy.copy(indicator)
            attach(new_indicator, new)
        return new

    def _detach_grace_containers(self, kind=None):
        from abjad.tools import scoretools
        grace_containers = self._get_grace_containers(kind=kind)
        for grace_container in grace_containers:
            detach(grace_container, self)
        return grace_containers

    def _detach_spanners(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
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

    def _format_after_slot(self, bundle):
        pass

    def _format_before_slot(self, bundle):
        pass

    def _format_close_brackets_slot(self, bundle):
        pass

    def _format_closing_slot(self, bundle):
        pass

    def _format_component(self, pieces=False):
        result = []
        manager = systemtools.LilyPondFormatManager
        bundle = manager.bundle_format_contributions(self)
        result.extend(self._format_before_slot(bundle))
        result.extend(self._format_open_brackets_slot(bundle))
        result.extend(self._format_opening_slot(bundle))
        result.extend(self._format_contents_slot(bundle))
        result.extend(self._format_closing_slot(bundle))
        result.extend(self._format_close_brackets_slot(bundle))
        result.extend(self._format_after_slot(bundle))
        contributions = []
        for contributor, contribution in result:
            contributions.extend(contribution)
        if pieces:
            return contributions
        else:
            return '\n'.join(contributions)

    def _format_contents_slot(self, bundle):
        pass

    def _format_open_brackets_slot(self, bundle):
        pass

    def _format_opening_slot(self, bundle):
        pass

    def _get_components(self, prototype=None, include_self=True):
        expr = self
        if include_self:
            expr = [self]
        components = iterate(expr).by_class(prototype)
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

    def _get_effective(self, prototype=None, unwrap=True):
        from abjad.tools import indicatortools
        from abjad.tools import datastructuretools
        from abjad.tools import scoretools
        # return time signature attached to measure regardless of scope
        if prototype == indicatortools.TimeSignature or \
            prototype == (indicatortools.TimeSignature,):
            if isinstance(self, scoretools.Measure):
                if self._has_indicator(indicatortools.TimeSignature):
                    indicator = self._get_indicator(
                        indicatortools.TimeSignature)
                    return indicator
                else:
                    return
        # update indicators of entire score tree if necessary
        self._update_now(indicators=True)
        # gather candidate expressions
        candidate_expressions = datastructuretools.SortedCollection(
            key=lambda x: x.component._get_timespan().start_offset
            )
        for parent in self._get_parentage(include_self=True):
            expressions = parent._dependent_expressions[:]
            for expression in parent._indicators:
                if expression.scope is None:
                    expressions.append(expression)
            for expression in expressions:
                if isinstance(expression.indicator, prototype):
                    candidate_expressions.insert(expression)
        #print candidate_expressions, 'CW'
        # elect most recent candidate expression
        if candidate_expressions:
            try:
                start_offset = self._get_timespan().start_offset
                expression = candidate_expressions.find_le(start_offset)
                if unwrap:
                    return expression.indicator
                else:
                    return expression
            except ValueError:
                pass

    def _get_effective_staff(self):
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        staff_change = self._get_effective(
            indicatortools.StaffChange)
        if staff_change is not None:
            effective_staff = staff_change.staff
        else:
            parentage = self._get_parentage()
            effective_staff = parentage.get_first(scoretools.Staff)
        return effective_staff

    def _get_format_contributions_for_slot(
        self, 
        slot_identifier, 
        bundle=None
        ):
        result = []
        if bundle is None:
            manager = systemtools.LilyPondFormatManager
            bundle = manager.bundle_format_contributions(self)
        slot_names = (
            'before',
            'open_brackets',
            'opening',
            'contents',
            'closing',
            'close_brackets',
            'after',
            )
        if isinstance(slot_identifier, int):
            assert slot_identifier in range(1, 7 + 1)
            slot_index = slot_number - 1
            slot_name = slot_names[slot_index]
        elif isinstance(slot_identifier, str):
            slot_name = slot_identifier.replace(' ', '_')
            assert slot_name in slot_names
        method_name = '_format_{}_slot'.format(slot_name)
        method = getattr(self, method_name)
        for source, contributions in method(bundle):
            result.extend(contributions)
        return result

    def _get_grace_containers(self, kind=None):
        from abjad.tools import scoretools
        result = []
        if kind in (None, 'grace') and \
            getattr(self, '_grace', None) is not None:
            result.append(self._grace)
        if kind in (None, 'after') and \
            getattr(self, '_after_grace', None) is not None:
            result.append(self._after_grace)
        elif kind == scoretools.GraceContainer:
            if self._grace is not None:
                result.append(self._grace)
            if self._after_grace is not None:
                result.append(self._after_grace)
        elif isinstance(kind, scoretools.GraceContainer):
            if self._grace is not None:
                result.append(self._grace)
            if self._after_grace is not None:
                result.append(self._after_grace)
        return tuple(result)

    def _get_in_my_logical_voice(self, n, component_class=None):
        if 0 <= n:
            generator = iterate(self).by_logical_voice_from_component(
                component_class=component_class,
                reverse=False,
                )
            for i, component in enumerate(generator):
                if i == n:
                    return component
        else:
            n = abs(n)
            generator = iterate(self).by_logical_voice_from_component(
                component_class=component_class,
                reverse=True,
                )
            for i, component in enumerate(generator):
                if i == n:
                    return component

    def _get_indicator(self, prototype=None, unwrap=True):
        indicators = self._get_indicators(prototype=prototype, unwrap=unwrap)
        if not indicators:
            message = 'no attached indicators found matching {!r}.'
            message = message.format(prototype)
            raise ValueError(message)
        elif 1 < len(indicators):
            message = 'multiple attached indicators found matching {!r}.'
            message = message.format(prototype)
            raise ValueError(message)
        else:
            return indicators[0]

    def _get_indicators(self, prototype=None, unwrap=True):
        from abjad.tools import indicatortools
        prototype = prototype or (object,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        prototype_objects, prototype_classes = [], []
        for indicator_prototype in prototype:
            if isinstance(indicator_prototype, types.TypeType):
                prototype_classes.append(indicator_prototype)
            else:
                prototype_objects.append(indicator_prototype)
        prototype_objects = tuple(prototype_objects)
        prototype_classes = tuple(prototype_classes)
        matching_indicators = []
        for indicator in self._indicators:
            if isinstance(indicator, prototype_classes):
                matching_indicators.append(indicator)
            elif any(indicator == x for x in prototype_objects):
                matching_indicators.append(indicator)
            elif isinstance(indicator, indicatortools.IndicatorExpression):
                if isinstance(indicator.indicator, prototype_classes):
                    matching_indicators.append(indicator)
                elif any(indicator.indicator == x for x in prototype_objects):
                    matching_indicators.append(indicator)
        if unwrap:
            matching_indicators = [x.indicator for x in matching_indicators]
        matching_indicators = tuple(matching_indicators)
        return matching_indicators

    def _get_lineage(self):
        return selectiontools.Lineage(self)

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        markup = self._get_indicators(markuptools.Markup)
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

    def _get_spanner(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
        if not spanners:
            message = 'no spanner found.'
            raise MissingSpannerError(message)
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            message = 'multiple spanners found.'
            raise ExtraSpannerError(message)

    def _get_spanner_indicators(self, prototype=None, unwrap=True):
        matching_indicators = []
        for spanner in self._get_spanners():
            result = spanner._get_indicators(
                prototype=prototype,
                unwrap=unwrap,
                )
            matching_indicators.extend(result)
        return matching_indicators

    def _get_spanners(self, prototype=None):
        from abjad.tools import spannertools
        prototype = prototype or (spannertools.Spanner,)
        if not isinstance(prototype, tuple):
            prototype = (prototype, )
        spanner_items = prototype[:]
        prototype, spanner_objects = [], []
        for spanner_item in spanner_items:
            if isinstance(spanner_item, types.TypeType):
                prototype.append(spanner_item)
            elif isinstance(spanner_item, spannertools.Spanner):
                spanner_objects.append(spanner_item)
            else:
                message = 'must be spanner class or spanner object: {!r}'
                message = message.format(spanner_item)
        prototype = tuple(prototype)
        spanner_objects = tuple(spanner_objects)
        matching_spanners = set()
        for spanner in set(self._spanners):
            if isinstance(spanner, prototype):
                matching_spanners.add(spanner)
            elif any(spanner == x for x in spanner_objects):
                matching_spanners.add(spanner)
        return matching_spanners

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

    def _has_effective_indicator(self, prototype=None):
        indicator = self._get_effective(prototype=prototype)
        return bool(indicator)

    def _has_indicator(self, prototype=None):
        indicators = self._get_indicators(prototype=prototype)
        return bool(indicators)

    def _has_spanner(self, prototype=None):
        spanners = self._get_spanners(prototype=prototype)
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

    def _move_indicators(self, recipient_component):
        from abjad.tools import indicatortools
        for indicator in self._get_indicators():
            detach(indicator, self)
            attach(indicator, recipient_component)

    # TODO: eventually reimplement as a keyword option to remove()
    def _remove_and_shrink_durated_parent_containers(self):
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
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
                indicator = parent._get_indicator(indicatortools.TimeSignature)
                parent_time_signature = indicator
                old_prolation = parent_time_signature.implied_prolation
                naive_time_signature = (
                    parent_time_signature.duration - prolated_leaf_duration)
                better_time_signature = mathtools.NonreducedFraction(
                    naive_time_signature)
                better_time_signature = better_time_signature.with_denominator(
                    parent_time_signature.denominator)
                better_time_signature = indicatortools.TimeSignature(
                    better_time_signature)
                detach(indicatortools.TimeSignature, parent)
                attach(better_time_signature, parent)
                indicator = parent._get_indicator(indicatortools.TimeSignature)
                parent_time_signature = indicator
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
            selection = selectiontools.SliceSelection(self)
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
                        message = 'no component in spanner at offset.'
                        raise ValueError(message)
                    for component in reversed(components):
                        spanner._insert(index, component)
                        component._spanners.add(spanner)
            selection = selectiontools.SliceSelection(self)
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
        indicators=False,
        ):
        from abjad.tools import systemtools
        return systemtools.UpdateManager._update_now(
            self,
            offsets=offsets,
            offsets_in_seconds=offsets_in_seconds,
            indicators=indicators,
            )
