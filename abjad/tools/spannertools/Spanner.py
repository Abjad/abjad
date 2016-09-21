# -*-coding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import systemtools
from abjad.tools import timespantools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import select
from abjad.tools.topleveltools import set_
Selection = selectiontools.Selection


class Spanner(AbjadObject):
    '''Spanner.

    Any type of object that stretches horizontally and encompasses some number
    of score components.

    Examples include beams, slurs, hairpins and trills.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_components',
        '_contiguity_constraint',
        '_indicator_expressions',
        '_lilypond_grob_name_manager',
        '_lilypond_setting_name_manager',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        name=None,
        ):
        overrides = overrides or {}
        self._components = []
        self._contiguity_constraint = 'logical voice'
        self._apply_overrides(overrides)
        self._indicator_expressions = []
        self._lilypond_setting_name_manager = None
        if name is not None:
            name = str(name)
        self._name = name

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        r'''Is true when spanner contains `expr`.
        Otherwise false.

        Returns true or false.
        '''
        for x in self._components:
            if x is expr:
                return True
        else:
            return False

    def __copy__(self, *args):
        r'''Copies spanner.

        Does not copy spanner components.

        Returns new spanner.
        '''
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_lilypond_grob_name_manager', None) is not None:
            new._lilypond_grob_name_manager = copy.copy(override(self))
        if getattr(self, '_lilypond_setting_name_manager', None) is not None:
            new._lilypond_setting_name_manager = copy.copy(set_(self))
        self._copy_keyword_args(new)
        new._name = self.name
        return new

    def __getitem__(self, expr):
        r'''Gets item from spanner.

        Returns component.
        '''
        if isinstance(expr, slice):
            return selectiontools.Selection(self._components.__getitem__(expr))
        return self._components.__getitem__(expr)

    def __getnewargs__(self):
        r'''Gets new arguments of spanner.

        Returns empty tuple.
        '''
        return ()

    def __getstate__(self):
        r'''Gets state of spanner.

        Returns dictionary.
        '''
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __len__(self):
        r'''Gets number of components in spanner.

        Returns nonnegative integer.
        '''
        return len(self.components)

    def __lt__(self, expr):
        r'''Is true when spanner is less than `expr`. Otherwise false.

        Trivial comparison to allow doctests to work.

        Returns true or false.
        '''
        if not isinstance(expr, Spanner):
            raise TypeError
        return repr(self) < repr(expr)

    ### PRIVATE METHODS ###

    def _append(self, component):
        assert self._attachment_test(component), (repr(component), repr(self))
        if self._contiguity_constraint == 'logical voice':
            components = self[-1:] + [component]
            assert Selection._all_are_contiguous_components_in_same_logical_voice(
                components), repr(components)
        component._spanners.add(self)
        self._components.append(component)

    def _append_left(self, component):
        components = [component] + self[:1]
        assert Selection._all_are_contiguous_components_in_same_logical_voice(
            components)
        component._spanners.add(self)
        self._components.insert(0, component)

    def _apply_overrides(self, overrides):
        import abjad
        namespace = abjad.__dict__.copy()
        manager = override(self)
        for key, value in overrides.items():
            grob_name, attribute = key.split('__', 1)
            grob_manager = getattr(manager, grob_name)
            if isinstance(value, str):
                if 'markuptools' in value or 'schemetools' in value:
                    value = eval(value, namespace, namespace)
            setattr(grob_manager, attribute, value)

    def _at_least_two_leaves(self, component_expression):
        leaves = select(component_expression).by_leaf()
        return 1 < len(leaves)

    def _attach(self, components):
        from abjad.tools import selectiontools
        assert not self, repr(self)
        if isinstance(components, scoretools.Component):
            self._append(components)
        elif isinstance(components, (list, tuple, selectiontools.Selection)):
            self._extend(components)
        else:
            raise TypeError(components)

    def _attachment_test(self, component):
        from abjad.tools import scoretools
        return isinstance(component, scoretools.Leaf)

    def _attachment_test_all(self, component_expression):
        return True

    def _block_all_components(self):
        r'''Not composer-safe.
        '''
        for component in self:
            self._block_component(component)

    def _block_component(self, component):
        r'''Not composer-safe.
        '''
        component._spanners.remove(self)

    def _constrain_contiguity(self):
        r'''Not composer-safe.
        '''
        self._contiguity_constraint = 'logical_voice'

    def _copy(self, components):
        r'''Returns copy of spanner with `components`.
        `components` must be an iterable of components already
        contained in spanner.
        '''
        my_components = self._components[:]
        self._components = []
        result = copy.copy(self)
        self._components = my_components
        for component in components:
            assert component in self
        for component in components:
            result._components.append(component)
        result._unblock_all_components()
        return result

    def _copy_keyword_args(self, new):
        pass

    def _detach(self):
        self._sever_all_components()

    def _extend(self, components):
        component_input = list(self[-1:])
        component_input.extend(components)
        if self._contiguity_constraint == 'logical voice':
            if not Selection._all_are_contiguous_components_in_same_logical_voice(
                component_input):
                message = 'must be contiguous components'
                message += ' in same logical voice: {!r}.'
                message = message.format(component_input)
                raise Exception(message)
        for component in components:
            self._append(component)

    def _extend_left(self, components):
        component_input = components + list(self[:1])
        assert Selection._all_are_contiguous_components_in_same_logical_voice(
            component_input)
        for component in reversed(components):
            self._append_left(component)

    def _format_after_leaf(self, leaf):
        result = []
        if self._is_my_last_leaf(leaf):
            result.extend(getattr(self, '_reverts', []))
        return result

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.extend(getattr(self, '_overrides', []))
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        return result

    def _fracture(self, i, direction=None):
        r'''Fractures spanner at `direction` of component at index `i`.

        Valid values for `direction` are ``Left``, ``Right`` and ``None``.

        Set `direction=None` to fracture on both left and right sides.

        Returns tuple of original, left and right spanners.
        '''
        if i < 0:
            i = len(self) + i
        if direction == Left:
            return self._fracture_left(i)
        elif direction == Right:
            return self._fracture_right(i)
        elif direction is None:
            left = self._copy(self[:i])
            right = self._copy(self[i + 1:])
            center = self._copy(self[i:i + 1])
            self._block_all_components()
            return self, left, center, right
        else:
            message = 'direction {!r} must be left, right or none.'
            message = message.format(direction)
            raise ValueError(message)

    def _fracture_left(self, i):
        left = self._copy(self[:i])
        right = self._copy(self[i:])
        self._block_all_components()
        return self, left, right

    def _fracture_right(self, i):
        left = self._copy(self[:i + 1])
        right = self._copy(self[i + 1:])
        self._block_all_components()
        return self, left, right

    def _fuse_by_reference(self, spanner):
        result = self._copy(self[:])
        result._extend(spanner.components)
        self._block_all_components()
        spanner._block_all_components()
        return [(self, spanner, result)]

    def _get_basic_lilypond_format_bundle(self, leaf):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        if self._is_my_first_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'override',
                is_once=False,
                )
            lilypond_format_bundle.grob_overrides.extend(contributions)
        if self._is_my_last_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'revert',
                )
            lilypond_format_bundle.grob_reverts.extend(contributions)
        return lilypond_format_bundle

    def _get_duration(self, in_seconds=False):
        return sum(
            component._get_duration(in_seconds=in_seconds)
            for component in self
            )

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        if self._compact_summary == '':
            values = []
        else:
            values = [self._compact_summary]
        if 'overrides' in names and not self.overrides:
            names.remove('overrides')
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=values,
            storage_format_kwargs_names=names,
            )

    def _get_indicators(self, prototype=None, unwrap=True):
        from abjad.tools import indicatortools
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
        matching_indicators = []
        for indicator in self._indicator_expressions:
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

    def _get_leaves(self):
        result = []
        for component in self._components:
            for node in iterate(component).depth_first():
                if isinstance(node, scoretools.Leaf):
                    result.append(node)
        return result

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        lilypond_format_bundle.get('before').spanners.extend(
            self._format_before_leaf(leaf))
        lilypond_format_bundle.get('right').spanners.extend(
            self._format_right_of_leaf(leaf))
        lilypond_format_bundle.get('after').spanners.extend(
            self._format_after_leaf(leaf))
        return lilypond_format_bundle

    def _get_my_first_leaf(self):
        for leaf in iterate(self).by_class(scoretools.Leaf):
            return leaf

    def _get_my_last_leaf(self):
        for leaf in iterate(self).by_class(scoretools.Leaf, reverse=True):
            return leaf

    def _get_my_nth_leaf(self, n):
        from abjad.tools import scoretools
        if not isinstance(n, int):
            raise TypeError
        if 0 <= n:
            leaves = iterate(self).by_class(scoretools.Leaf)
            for leaf_index, leaf in enumerate(leaves):
                if leaf_index == n:
                    return leaf
        else:
            leaves = iterate(self).by_class(scoretools.Leaf, reverse=True)
            for leaf_index, leaf in enumerate(leaves):
                leaf_number = -leaf_index - 1
                if leaf_number == n:
                    return leaf
        raise IndexError

    def _get_timespan(self, in_seconds=False):
        from abjad.tools import durationtools
        if len(self):
            start_offset = \
                self[0]._get_timespan(in_seconds=in_seconds)._start_offset
            stop_offset = \
                self[-1]._get_timespan(in_seconds=in_seconds)._stop_offset
        else:
            start_offset = durationtools.Duration(0)
            stop_offset = durationtools.Duration(0)
        return timespantools.Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )

    def _index(self, component):
        return self._components.index(component)

    def _insert(self, i, component):
        r'''Not composer-safe.
        '''
        component._spanners.add(self)
        self._components.insert(i, component)

    def _is_exterior_leaf(self, leaf):
        r'''True if leaf is first or last in spanner.
        True if next leaf or previous leaf is none.
        Otherwise false.
        '''
        if self._is_my_first_leaf(leaf):
            return True
        elif self._is_my_last_leaf(leaf):
            return True
        elif not leaf._get_leaf(-1) and not leaf._get_leaf(1):
            return True
        else:
            return False

    def _is_interior_leaf(self, leaf):
        leaves = self._get_leaves()
        if leaf not in leaves:
            return False
        if len(leaves) < 3:
            return False
        leaf_count = len(leaves)
        first_index = 0
        last_index = leaf_count - 1
        leaf_index = leaves.index(leaf)
        if first_index < leaf_index < last_index:
            return True
        return False

    def _is_my_first(self, leaf, prototype):
        for component in iterate(self).by_class(prototype):
            if component is leaf:
                return True
            else:
                return False

    def _is_my_first_leaf(self, leaf):
        try:
            first_leaf = self._get_my_nth_leaf(0)
            return leaf is first_leaf
        except IndexError:
            return False

    def _is_my_last(self, leaf, prototype):
        for component in iterate(self).by_class(
            prototype,
            reverse=True,
            ):
            if component is leaf:
                return True
            else:
                return False

    def _is_my_last_leaf(self, leaf):
        try:
            last_leaf = self._get_my_nth_leaf(-1)
            return leaf is last_leaf
        except IndexError:
            return False

    def _is_my_only(self, leaf, prototype):
        i = None
        components = iterate(self).by_class(prototype)
        for i, component in enumerate(components):
            if 0 < i:
                return False
        return i == 0

    def _is_my_only_leaf(self, leaf):
        return self._is_my_first_leaf(leaf) and self._is_my_last_leaf(leaf)

    def _remove(self, component):
        r'''Not composer-safe.
        '''
        self._sever_component(component)

    def _remove_component(self, component):
        r'''Not composer-safe.
        '''
        for i, x in enumerate(self._components):
            if x is component:
                self._components.pop(i)
                break
        else:
            message = 'component {!r} not in spanner components list.'
            raise ValueError(message.format(component))

    def _reverse_components(self):
        r'''Reverses order of spanner components.

        Not composer-safe because reversing the order of spanner components
        could scramble components of some other spanner.

        Call method only as part of a full component- and spanner-reversal
        routine.

        Spanner subclasses with mapping variables (like the 'durations' list
        attaching to durated complex beam spanners) should override this
        method to reverse mapping elements.
        '''
        self._components.reverse()

    def _sever_all_components(self):
        r'''Not composer-safe.
        '''
        for n in reversed(range(len(self))):
            component = self[n]
            self._sever_component(component)

    def _sever_component(self, component):
        r'''Not composer-safe.
        '''
        self._block_component(component)
        self._remove_component(component)

    def _start_offset_in_me(self, leaf):
        leaf_start_offset = leaf._get_timespan().start_offset
        self_start_offset = self._get_timespan().start_offset
        return leaf_start_offset - self_start_offset

    def _stop_offset_in_me(self, leaf):
        leaf_start_offset = self._start_offset_in_me(leaf)
        leaf_stop_offset = leaf_start_offset + leaf._get_duration()
        return leaf_stop_offset

    def _unblock_all_components(self):
        r'''Not composer-safe.
        '''
        for component in self:
            self._unblock_component(component)

    def _unblock_component(self, component):
        r'''Not composer-safe.
        '''
        component._spanners.add(self)

    def _unconstrain_contiguity(self):
        r'''Not composer-safe.
        '''
        self._contiguity_constraint = None

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_summary(self):
        len_self = len(self)
        if not len_self:
            return ''
        elif 0 < len_self <= 8:
            return ', '.join([str(x) for x in self])
        else:
            left = ', '.join([str(x) for x in self[:2]])
            right = ', '.join([str(x) for x in self[-2:]])
            number_in_middle = len_self - 4
            middle = ', ... [%s] ..., ' % number_in_middle
            return left + middle + right

    @property
    def _duration_in_seconds(self):
        duration = durationtools.Duration(0)
        for leaf in self.leaves:
            duration += leaf._get_duration(in_seconds=True)
        return duration

    @property
    def _preprolated_duration(self):
        return sum([component._preprolated_duration for component in self])

    @property
    def _summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self])
        else:
            return ' '

    ### PUBLIC PROPERTIES ###

    @property
    def components(self):
        r'''Gets components in spanner.

        Returns selection.
        '''
        from abjad.tools import selectiontools
        return selectiontools.Selection(self._components[:])

    @property
    def name(self):
        r'''Gets spanner name.

        Returns string.
        '''
        return self._name

    @property
    def overrides(self):
        r'''Gets overrides.

        Returns dict.
        '''
        manager = override(self)
        overrides = {}
        for attribute_tuple in manager._get_attribute_tuples():
            attribute = '__'.join(attribute_tuple[:-1])
            value = attribute_tuple[-1]
            overrides[attribute] = value
        return overrides
