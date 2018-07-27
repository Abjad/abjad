import abc
import bisect
import copy
import uqbar.graphs
from abjad import enums
from abjad import exceptions
from abjad import mathtools
from abjad.system.AbjadObject import AbjadObject
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.UpdateManager import UpdateManager
from abjad.system.Wrapper import Wrapper
from abjad.timespans.Timespan import Timespan
from abjad.utilities.Duration import Duration


class Component(AbjadObject):
    """
    Component baseclass.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_indicators_are_current',
        '_is_forbidden_to_update',
        '_overrides',
        '_lilypond_setting_name_manager',
        '_measure_number',
        '_offsets_are_current',
        '_offsets_in_seconds_are_current',
        '_parent',
        '_start_offset',
        '_start_offset_in_seconds',
        '_stop_offset',
        '_stop_offset_in_seconds',
        '_timespan',
        '_wrappers',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, name=None):
        self._indicators_are_current = False
        self._is_forbidden_to_update = False
        self._measure_number = None
        self._offsets_are_current = False
        self._offsets_in_seconds_are_current = False
        self._overrides = None
        self._parent = None
        self._lilypond_setting_name_manager = None
        self._start_offset = None
        self._start_offset_in_seconds = None
        self._stop_offset = None
        self._stop_offset_in_seconds = None
        self._timespan = Timespan()
        self._wrappers = []

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies component.

        Copies indicators.

        Does not copy spanners.

        Does not copy children.

        Returns new component.
        """
        import abjad
        new_component = type(self)(*self.__getnewargs__())
        if getattr(self, '_overrides', None) is not None:
            manager = copy.copy(abjad.override(self))
            new_component._overrides = manager
        if getattr(self, '_lilypond_setting_name_manager', None) is not None:
            manager = copy.copy(abjad.setting(self))
            new_component._lilypond_setting_name_manager = manager
        for wrapper in abjad.inspect(self).annotation_wrappers():
            new_wrapper = copy.copy(wrapper)
            abjad.attach(new_wrapper, new_component)
        for wrapper in abjad.inspect(self).wrappers():
            new_wrapper = copy.copy(wrapper)
            abjad.attach(new_wrapper, new_component)
        return new_component

    def __format__(self, format_specification=''):
        """
        Formats component.

        Returns string.
        """
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return StorageFormatManager(self).get_storage_format()
        raise ValueError(repr(format_specification))

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return ()

    def __illustrate__(self):
        """
        Illustrates component.

        Returns LilyPond file.
        """
        import abjad
        lilypond_file = abjad.LilyPondFile.new(self)
        return lilypond_file

    def __mul__(self, n):
        """
        Copies component `n` times and detaches spanners.

        Returns list of new components.
        """
        import abjad
        components = []
        for i in range(n):
            component = abjad.mutate(self).copy()
            components.append(component)
        for component in abjad.iterate(components).components():
            abjad.detach(abjad.Spanner, component)
        result = abjad.select(components)
        return result

    def __repr__(self):
        """
        Gets interpreter representation of leaf.

        Returns string.
        """
        return StorageFormatManager(self).get_repr_format()

    def __rmul__(self, n):
        """
        Copies component `n` times and detach spanners.

        Returns list of new components.
        """
        return self * n

    ### PRIVATE METHODS ###

    def _as_graphviz_node(self):
        import abjad
        score_index = abjad.inspect(self).parentage().score_index
        score_index = '_'.join(str(_) for _ in score_index)
        class_name = type(self).__name__
        if score_index:
            name = '{}_{}'.format(class_name, score_index)
        else:
            name = class_name
        node = uqbar.graphs.Node(
            name=name,
            attributes={
                'margin': 0.05,
                'style': 'rounded',
                },
            )
        table = uqbar.graphs.Table(
            attributes={
                'border': 2,
                'cellpadding': 5,
                },
            )
        node.append(table)
        return node

    def _cache_named_children(self):
        name_dictionary = {}
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        name = getattr(self, 'name', None)
        if name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = []
            name_dictionary[self.name].append(self)
        return name_dictionary

    def _check_for_cycles(self, components):
        import abjad
        parentage = abjad.inspect(self).parentage()
        for component in components:
            if component in parentage:
                return True
        return False

    def _extract(self, scale_contents=False):
        import abjad
        if scale_contents:
            self._scale_contents(self.multiplier)
        selection = abjad.select([self])
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        components = list(getattr(self, 'components', ()))
        parent.__setitem__(slice(start, stop + 1), components)
        return self

    def _format_absolute_after_slot(self, bundle):
        return []

    def _format_absolute_before_slot(self, bundle):
        return []

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
        bundle = LilyPondFormatManager.bundle_format_contributions(self)
        result.extend(self._format_absolute_before_slot(bundle))
        result.extend(self._format_before_slot(bundle))
        result.extend(self._format_open_brackets_slot(bundle))
        result.extend(self._format_opening_slot(bundle))
        result.extend(self._format_contents_slot(bundle))
        result.extend(self._format_closing_slot(bundle))
        result.extend(self._format_close_brackets_slot(bundle))
        result.extend(self._format_after_slot(bundle))
        result.extend(self._format_absolute_after_slot(bundle))
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

    def _get_contents(self, include_self=True):
        import abjad
        result = []
        if include_self:
            result.append(self)
        result.extend(getattr(self, 'components', []))
        result = abjad.select(result)
        return result

    def _get_descendants(self, include_self=True):
        import abjad
        return abjad.Descendants(self, include_self=include_self)

    def _get_descendants_starting_with(self):
        import abjad
        result = []
        result.append(self)
        if isinstance(self, abjad.Container):
            if self.is_simultaneous:
                for x in self:
                    result.extend(x._get_descendants_starting_with())
            elif self:
                result.extend(self[0]._get_descendants_starting_with())
        return result

    def _get_descendants_stopping_with(self):
        import abjad
        result = []
        result.append(self)
        if isinstance(self, abjad.Container):
            if self.is_simultaneous:
                for x in self:
                    result.extend(x._get_descendants_stopping_with())
            elif self:
                result.extend(self[-1]._get_descendants_stopping_with())
        return result

    def _get_duration(self, in_seconds=False):
        import abjad
        if in_seconds:
            return self._get_duration_in_seconds()
        else:
            parentage = abjad.inspect(self).parentage(include_self=False)
            return parentage.prolation * self._get_preprolated_duration()

    def _get_effective(self, prototype, unwrap=True, n=0):
        import abjad
        # return time signature attached to measure regardless of context
        if (prototype == abjad.TimeSignature or
            prototype == (abjad.TimeSignature,)):
            if isinstance(self, abjad.Measure):
                if self._has_indicator(abjad.TimeSignature):
                    indicator = self._get_indicator(abjad.TimeSignature)
                    return indicator
                else:
                    return
        self._update_now(indicators=True)
        candidate_wrappers = {}
        parentage = abjad.inspect(self).parentage(
            include_self=True,
            grace_notes=True,
            )
        for component in parentage:
            these_wrappers = []
            for wrapper in component._wrappers:
                if wrapper.annotation:
                    continue
                if isinstance(wrapper.indicator, prototype):
                    #offset = wrapper.start_offset
                    #candidate_wrappers.setdefault(offset, []).append(wrapper)
                    these_wrappers.append(wrapper)
            # activate indicator takes precendence over inactive indicator
            if (any(_.deactivate is True for _ in these_wrappers) and
                not all(_.deactivate is True for _ in these_wrappers)):
                these_wrappers = [
                    _ for _ in these_wrappers if _.deactivate is not True
                    ]
            for wrapper in these_wrappers:
                offset = wrapper.start_offset
                candidate_wrappers.setdefault(offset, []).append(wrapper)
            if not isinstance(component, abjad.Context):
                continue
            for wrapper in component._dependent_wrappers:
                if wrapper.annotation:
                    continue
                if isinstance(wrapper.indicator, prototype):
                    offset = wrapper.start_offset
                    candidate_wrappers.setdefault(offset, []).append(wrapper)
        if not candidate_wrappers:
            return
        all_offsets = sorted(candidate_wrappers)
        start_offset = abjad.inspect(self).timespan().start_offset
        index = bisect.bisect(all_offsets, start_offset) - 1 + int(n)
        if index < 0:
            return
        elif len(candidate_wrappers) <= index:
            return
        wrapper = candidate_wrappers[all_offsets[index]][0]
        if unwrap:
            return wrapper.indicator
        return wrapper

    def _get_effective_staff(self):
        import abjad
        staff_change = self._get_effective(abjad.StaffChange)
        if staff_change is not None:
            effective_staff = staff_change.staff
        else:
            parentage = abjad.inspect(self).parentage()
            effective_staff = parentage.get_first(abjad.Staff)
        return effective_staff

    def _get_format_contributions_for_slot(self, slot_identifier, bundle=None):
        result = []
        if bundle is None:
            manager = LilyPondFormatManager
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
            slot_index = slot_identifier - 1
            slot_name = slot_names[slot_index]
        elif isinstance(slot_identifier, str):
            slot_name = slot_identifier.replace(' ', '_')
            assert slot_name in slot_names
        method_name = '_format_{}_slot'.format(slot_name)
        method = getattr(self, method_name)
        for source, contributions in method(bundle):
            result.extend(contributions)
        return result

    def _get_format_pieces(self):
        return self._format_component(pieces=True)

    def _get_format_specification(self):
        values = []
        summary = self._get_contents_summary()
        if summary:
            values.append(summary)
        return FormatSpecification(
            client=self,
            repr_args_values=values,
            storage_format_kwargs_names=[]
            )

    def _get_in_my_logical_voice(self, n, prototype=None):
        import abjad
        if 0 <= n:
            generator = abjad.iterate(self)._logical_voice(
                prototype=prototype,
                reverse=False,
                )
            for i, component in enumerate(generator):
                if i == n:
                    return component
        else:
            n = abs(n)
            generator = abjad.iterate(self)._logical_voice(
                prototype=prototype,
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
        if 1 < len(indicators):
            message = 'multiple attached indicators found matching {!r}.'
            message = message.format(prototype)
            raise ValueError(message)
        return indicators[0]

    def _get_indicators(self, prototype=None, unwrap=True):
        prototype = prototype or (object,)
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        prototype_objects, prototype_classes = [], []
        for indicator_prototype in prototype:
            if isinstance(indicator_prototype, type):
                prototype_classes.append(indicator_prototype)
            else:
                prototype_objects.append(indicator_prototype)
        prototype_objects = tuple(prototype_objects)
        prototype_classes = tuple(prototype_classes)
        result = []
        for wrapper in self._wrappers:
            if wrapper.annotation:
                continue
            if isinstance(wrapper, prototype_classes):
                result.append(wrapper)
            elif any(wrapper == _ for _ in prototype_objects):
                result.append(wrapper)
            elif isinstance(wrapper, Wrapper):
                if isinstance(wrapper.indicator, prototype_classes):
                    result.append(wrapper)
                elif any(wrapper.indicator == _ for _ in prototype_objects):
                    result.append(wrapper)
        if unwrap:
            result = [_.indicator for _ in result]
        result = tuple(result)
        return result

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    def _get_lineage(self):
        import abjad
        return abjad.Lineage(self)

    def _get_markup(self, direction=None):
        import abjad
        markup = self._get_indicators(abjad.Markup)
        if direction is enums.Up:
            return tuple(x for x in markup if x.direction is enums.Up)
        elif direction is enums.Down:
            return tuple(x for x in markup if x.direction is enums.Down)
        return markup

    def _get_next_measure(self):
        import abjad
        if isinstance(self, abjad.Leaf):
            for parent in abjad.inspect(self).parentage(
                include_self=False):
                if isinstance(parent, abjad.Measure):
                    return parent
            raise exceptions.MissingMeasureError
        elif isinstance(self, abjad.Measure):
            return self._get_in_my_logical_voice(1, prototype=abjad.Measure)
        elif isinstance(self, abjad.Container):
            contents = self._get_descendants_starting_with()
            contents = [x for x in contents if isinstance(x, abjad.Measure)]
            if contents:
                return contents[0]
            raise exceptions.MissingMeasureError
        elif isinstance(self, (list, tuple)):
            measure_generator = abjad.iterate(self).components(abjad.Measure)
            try:
                measure = next(measure_generator)
                return measure
            except StopIteration:
                raise exceptions.MissingMeasureError
        else:
            message = 'unknown component: {!r}.'
            raise TypeError(message.format(self))

    def _get_nth_component_in_time_order_from(self, n):
        import abjad
        assert mathtools.is_integer_equivalent(n)
        def next(component):
            if component is not None:
                for parent in abjad.inspect(component).parentage(
                    include_self=True):
                    next_sibling = parent._get_sibling(1)
                    if next_sibling is not None:
                        return next_sibling
        def previous(component):
            if component is not None:
                for parent in abjad.inspect(component).parentage(
                    include_self=True):
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

    def _get_parentage(self, include_self=True, grace_notes=False):
        import abjad
        return abjad.Parentage(
            self,
            include_self=include_self,
            grace_notes=grace_notes,
            )

    def _get_previous_measure(self):
        import abjad
        if isinstance(self, abjad.Leaf):
            for parent in abjad.inspect(self).parentage(
                include_self=False):
                if isinstance(parent, abjad.Measure):
                    return parent
            raise exceptions.MissingMeasureError
        elif isinstance(self, abjad.Measure):
            return self._get_in_my_logical_voice(-1, prototype=abjad.Measure)
        elif isinstance(self, abjad.Container):
            contents = self._get_descendants_stopping_with()
            contents = [x for x in contents if isinstance(x, abjad.Measure)]
            if contents:
                return contents[0]
            raise exceptions.MissingMeasureError
        elif isinstance(self, (list, tuple)):
            measure_generator = abjad.iterate(self).components(
                abjad.Measure,
                reverse=True,
                )
            try:
                measure = next(measure_generator)
                return measure
            except StopIteration:
                raise exceptions.MissingMeasureError
        else:
            message = 'unknown component: {!r}.'
            raise TypeError(message.format(self))

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

    def _get_timespan(self, in_seconds=False):
        import abjad
        if in_seconds:
            self._update_now(offsets_in_seconds=True)
            if self._start_offset_in_seconds is None:
                raise exceptions.MissingMetronomeMarkError
            return Timespan(
                start_offset=self._start_offset_in_seconds,
                stop_offset=self._stop_offset_in_seconds,
                )
        else:
            self._update_now(offsets=True)
            return self._timespan

    def _get_vertical_moment(self, governor=None):
        import abjad
        offset = abjad.inspect(self).timespan().start_offset
        if governor is None:
            governor = abjad.inspect(self).parentage().root
        return abjad.VerticalMoment(governor, offset)

    def _get_vertical_moment_at(self, offset):
        import abjad
        return abjad.VerticalMoment(self, offset)

    def _has_effective_indicator(self, prototype=None):
        indicator = self._get_effective(prototype=prototype)
        return indicator is not None

    def _has_indicator(self, prototype=None):
        indicators = self._get_indicators(prototype=prototype)
        return bool(indicators)

    def _is_immediate_temporal_successor_of(self, component):
        temporal_successors = []
        current = self
        while current is not None:
            next_sibling = current._get_sibling(1)
            if next_sibling is None:
                current = current._parent
            else:
                descendants = next_sibling._get_descendants_starting_with()
                temporal_successors = descendants
                break
        return component in temporal_successors

    def _move_indicators(self, recipient_component):
        import abjad
        for wrapper in abjad.inspect(self).wrappers():
            abjad.detach(wrapper, self)
            abjad.attach(wrapper, recipient_component)

    # TODO: eventually reimplement as a keyword option to remove()
    def _remove_and_shrink_durated_parent_containers(self):
        import abjad
        prolated_leaf_duration = self._get_duration()
        parentage = abjad.inspect(self).parentage(include_self=False)
        prolations = parentage._prolations
        current_prolation, i = Duration(1), 0
        parent = self._parent
        while parent is not None and not parent.is_simultaneous:
            current_prolation *= prolations[i]
            if isinstance(parent, abjad.Measure):
                indicator = parent._get_indicator(abjad.TimeSignature)
                parent_time_signature = indicator
                old_prolation = parent_time_signature.implied_prolation
                naive_time_signature = (
                    parent_time_signature.duration - prolated_leaf_duration)
                better_time_signature = abjad.NonreducedFraction(
                    naive_time_signature)
                better_time_signature = better_time_signature.with_denominator(
                    parent_time_signature.denominator)
                better_time_signature = abjad.TimeSignature(
                    better_time_signature)
                abjad.detach(abjad.TimeSignature, parent)
                abjad.attach(better_time_signature, parent)
                indicator = parent._get_indicator(abjad.TimeSignature)
                parent_time_signature = indicator
                new_prolation = parent_time_signature.implied_prolation
                adjusted_prolation = old_prolation / new_prolation
                for x in parent:
                    if adjusted_prolation != 1:
                        new_target = x._get_preprolated_duration()
                        new_target *= adjusted_prolation
                        contents_duration = abjad.inspect(x)
                        multiplier = new_target / contents_duration
                        tuplet = abjad.Tuplet(multiplier, [])
                        abjad.mutate(x).wrap(tuplet)
            parent = parent._parent
            i += 1
        parentage = abjad.inspect(self).parentage(include_self=False)
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
        import abjad
        self._update_later(offsets=True)
        for component in abjad.inspect(self).parentage(include_self=False):
            if not isinstance(component, abjad.Context):
                continue
            for wrapper in component._dependent_wrappers[:]:
                if wrapper.component is self:
                    component._dependent_wrappers.remove(wrapper)
        if self._parent is not None:
            self._parent._components.remove(self)
        self._parent = None

    def _remove_named_children_from_parentage(self, name_dictionary):
        import abjad
        if self._parent is not None and name_dictionary:
            for parent in abjad.inspect(self).parentage(
                include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    for component in name_dictionary[name]:
                        named_children[name].remove(component)
                    if not named_children[name]:
                        del named_children[name]

    def _restore_named_children_to_parentage(self, name_dictionary):
        import abjad
        if self._parent is not None and name_dictionary:
            for parent in abjad.inspect(self).parentage(
                include_self=False):
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].extend(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

    def _set_parent(self, new_parent):
        """
        Not composer-safe.
        """
        named_children = self._cache_named_children()
        self._remove_named_children_from_parentage(named_children)
        self._remove_from_parent()
        self._parent = new_parent
        self._restore_named_children_to_parentage(named_children)
        self._update_later(offsets=True)

    def _splice(
        self,
        components,
        direction=enums.Right,
        grow_spanners=True,
        ):
        import abjad
        assert all(isinstance(x, Component) for x in components)
        selection = abjad.select(self)
        if direction is enums.Right:
            if grow_spanners:
                insert_offset = abjad.inspect(self).timespan().stop_offset
                receipt = selection._get_dominant_spanners()
                for spanner, index in receipt:
                    insert_component = None
                    for component in spanner:
                        start_offset = abjad.inspect(
                            component).timespan().start_offset
                        if start_offset == insert_offset:
                            insert_component = component
                            break
                    if insert_component is not None:
                        insert_index = spanner._index(insert_component)
                    else:
                        insert_index = len(spanner)
                    for component in reversed(components):
                        leaves = abjad.select(component).leaves()
                        for leaf in reversed(leaves):
                            spanner._insert(insert_index, leaf)
                            leaf._append_spanner(spanner)
            selection = abjad.select(self)
            parent, start, stop = \
                selection._get_parent_and_start_stop_indices()
            if parent is not None:
                if grow_spanners:
                    for component in reversed(components):
                        component._set_parent(parent)
                        parent._components.insert(start + 1, component)
                else:
                    after = stop + 1
                    parent.__setitem__(slice(after, after), components)
            return [self] + components
        else:
            if grow_spanners:
                offset = abjad.inspect(self).timespan().start_offset
                receipt = selection._get_dominant_spanners()
                for spanner, x in receipt:
                    for component in spanner:
                        timespan = abjad.inspect(component).timespan()
                        if timespan.start_offset == offset:
                            index = spanner._index(component)
                            break
                    else:
                        raise ValueError('no component in spanner at offset.')
                    for component in reversed(components):
                        leaves = abjad.select(component).leaves()
                        for leaf in reversed(leaves):
                            spanner._insert(index, leaf)
                            if isinstance(component, abjad.Leaf):
                                component._append_spanner(spanner)
            selection = abjad.select(self)
            parent, start, stop = \
                selection._get_parent_and_start_stop_indices()
            if parent is not None:
                if grow_spanners:
                    for component in reversed(components):
                        component._set_parent(parent)
                        parent._components.insert(start, component)
                else:
                    parent.__setitem__(slice(start, start), components)
            return components + [self]

    def _update_later(self, offsets=False, offsets_in_seconds=False):
        import abjad
        assert offsets or offsets_in_seconds
        for component in abjad.inspect(self).parentage(include_self=True):
            if offsets:
                component._offsets_are_current = False
            elif offsets_in_seconds:
                component._offsets_in_seconds_are_current = False

    def _update_measure_numbers(self):
        update_manager = UpdateManager()
        update_manager._update_measure_numbers(self)

    def _update_now(
        self,
        offsets=False,
        offsets_in_seconds=False,
        indicators=False,
        ):
        update_manager = UpdateManager()
        return update_manager._update_now(
            self,
            offsets=offsets,
            offsets_in_seconds=offsets_in_seconds,
            indicators=indicators,
            )
