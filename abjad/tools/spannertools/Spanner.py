import collections
import copy
from abjad.tools.abctools import AbjadObject


class Spanner(AbjadObject):
    '''Spanner.

    Any object that stretches horizontally and encompasses leaves.

    Examples include beams, slurs, hairpins and trills.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contiguity_constraint',
        '_ignore_attachment_test',
        '_ignore_before_attach',
        '_indicator_wrappers',
        '_leaves',
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
        self._contiguity_constraint = 'logical voice'
        self._apply_overrides(overrides)
        self._ignore_attachment_test = None
        self._ignore_before_attach = None
        self._indicator_wrappers = []
        self._leaves = []
        self._lilypond_setting_name_manager = None
        if name is not None:
            name = str(name)
        self._name = name

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when spanner contains `argument`.
        Otherwise false.

        Returns true or false.
        '''
        for leaf in self.leaves:
            if leaf is argument:
                return True
        else:
            return False

    def __copy__(self, *arguments):
        r'''Copies spanner.

        Does not copy spanner leaves.

        Returns new spanner.
        '''
        import abjad
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_lilypond_grob_name_manager', None) is not None:
            new._lilypond_grob_name_manager = copy.copy(abjad.override(self))
        if getattr(self, '_lilypond_setting_name_manager', None) is not None:
            new._lilypond_setting_name_manager = copy.copy(abjad.setting(self))
        self._copy_keyword_args(new)
        new._name = self.name
        return new

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        Returns leaf.
        '''
        import abjad
        if isinstance(argument, slice):
            leaves = self.leaves.__getitem__(argument)
            return abjad.select(leaves)
        return self.leaves.__getitem__(argument)

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
        r'''Gets number of leaves in spanner.

        Returns nonnegative integer.
        '''
        return len(self.leaves)

    def __lt__(self, argument):
        r'''Is true when spanner is less than `argument`. Otherwise false.

        Trivial comparison to allow doctests to work.

        Returns true or false.
        '''
        assert isinstance(argument, Spanner), repr(argument)
        return repr(self) < repr(argument)

    ### PRIVATE METHODS ###

    def _append(self, leaf):
        import abjad
        if self._ignore_attachment_test:
            pass
        elif not self._attachment_test(leaf):
            message = 'can not attach {!r} to {!r}.'
            message = message.format(self, leaf)
            raise Exception(message)
        if self._contiguity_constraint == 'logical voice':
            leaves = self[-1:] + [leaf]
            leaves = abjad.select(leaves)
            if not leaves.are_contiguous_logical_voice():
                raise Exception(leaves)
        leaf._spanners.add(self)
        self._leaves.append(leaf)

    def _append_left(self, leaf):
        import abjad
        leaves = [leaf] + self[:1]
        leaves = abjad.select(leaves)
        assert leaves.are_contiguous_logical_voice()
        leaf._spanners.add(self)
        self._leaves.insert(0, leaf)

    def _apply_overrides(self, overrides):
        import abjad
        namespace = abjad.__dict__.copy()
        manager = abjad.override(self)
        for key, value in overrides.items():
            grob_name, attribute = key.split('__', 1)
            grob_manager = getattr(manager, grob_name)
            if isinstance(value, str):
                if 'markuptools' in value or 'schemetools' in value:
                    value = eval(value, namespace, namespace)
            setattr(grob_manager, attribute, value)

    def _at_least_two_leaves(self, argument):
        import abjad
        leaves = abjad.select(argument).leaves()
        return 1 < len(leaves)

    def _attach(self, argument):
        import abjad
        assert not self, repr(self)
        if isinstance(argument, abjad.Leaf):
            self._append(argument)
        elif isinstance(argument, (list, tuple, abjad.Selection)):
            self._extend(argument)
        else:
            raise TypeError(argument)

    def _attach_piecewise(self, indicator, leaf, tag=None):
        import abjad
        if leaf not in self:
            message = 'must be leaf in spanner: {!r}.'
            message = message.format(leaf)
            raise Exception(message)
        context = getattr(indicator, '_context', None)
        wrapper = abjad.IndicatorWrapper(
            component=leaf,
            context=context,
            indicator=indicator,
            is_piecewise=True,
            piecewise_spanner=self,
            tag=tag,
            )
        wrapper._bind_to_component(leaf)

    def _attachment_test(self, argument):
        import abjad
        return isinstance(argument, abjad.Leaf)

    def _attachment_test_all(self, argument):
        return True

    def _before_attach(self, argument):
        pass

    def _block_all_leaves(self):
        r'''Not composer-safe.
        '''
        for leaf in self:
            self._block_leaf(leaf)

    def _block_leaf(self, leaf):
        r'''Not composer-safe.
        '''
        leaf._spanners.remove(self)

    def _constrain_contiguity(self):
        r'''Not composer-safe.
        '''
        self._contiguity_constraint = 'logical_voice'

    def _copy(self, leaves):
        r'''Returns copy of spanner with `leaves`.

        `leaves` must already be contained in spanner.
        '''
        my_leaf = self._leaves[:]
        self._leaves = []
        result = copy.copy(self)
        self._leaves = my_leaf
        for leaf in leaves:
            assert leaf in self
        for leaf in leaves:
            result._leaves.append(leaf)
        result._unblock_all_leaves()
        return result

    def _copy_keyword_args(self, new):
        pass

    def _detach(self):
        self._sever_all_leaves()

    def _extend(self, leaves):
        import abjad
        leaf_input = list(self[-1:])
        leaf_input.extend(leaves)
        leaf_input = abjad.select(leaf_input)
        if self._contiguity_constraint == 'logical voice':
            if not leaf_input.are_contiguous_logical_voice():
                message = 'must be contiguous: {!r}.'
                message = message.format(leaf_input)
                raise Exception(self, message)
        for leaf in leaves:
            self._append(leaf)

    def _extend_left(self, leaves):
        import abjad
        leaf_input = leaves + list(self[:1])
        leaf_input = abjad.select(leaf_input)
        assert leaf_input.are_contiguous_logical_voice()
        for leaf in reversed(leaves):
            self._append_left(leaf)

    def _format_after_leaf(self, leaf):
        return []

    def _format_before_leaf(self, leaf):
        return []

    def _format_right_of_leaf(self, leaf):
        return []

    def _fracture(self, i, direction=None):
        r'''Fractures spanner at `direction` of leaf at index `i`.

        Valid values for `direction` are ``Left``, ``Right`` and ``None``.

        Set `direction=None` to fracture on both left and right sides.

        Returns tuple of original, left and right spanners.
        '''
        import abjad
        if i < 0:
            i = len(self) + i
        if direction == abjad.Left:
            return self._fracture_left(i)
        elif direction == abjad.Right:
            return self._fracture_right(i)
        elif direction is None:
            left = self._copy(self[:i])
            right = self._copy(self[i + 1:])
            center = self._copy(self[i:i + 1])
            self._block_all_leaves()
            return self, left, center, right
        else:
            message = 'direction {!r} must be left, right or none.'
            message = message.format(direction)
            raise ValueError(message)

    def _fracture_left(self, i):
        left = self._copy(self[:i])
        right = self._copy(self[i:])
        self._block_all_leaves()
        return self, left, right

    def _fracture_right(self, i):
        left = self._copy(self[:i + 1])
        right = self._copy(self[i + 1:])
        self._block_all_leaves()
        return self, left, right

    def _fuse_by_reference(self, spanner):
        result = self._copy(self[:])
        self._block_all_leaves()
        spanner._block_all_leaves()
        result._extend(spanner.leaves)
        return [(self, spanner, result)]

    def _get_basic_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        if self._is_my_last_leaf(leaf):
            contributions = abjad.override(self)._list_format_contributions(
                'revert',
                )
            bundle.grob_reverts.extend(contributions)
        if self._is_my_first_leaf(leaf):
            contributions = abjad.override(self)._list_format_contributions(
                'override',
                once=False,
                )
            bundle.grob_overrides.extend(contributions)
        return bundle

    def _get_compact_summary(self):
        if not len(self):
            return ''
        elif 0 < len(self) <= 8:
            return ', '.join([str(_) for _ in self])
        else:
            left = ', '.join([str(_) for _ in self[:2]])
            right = ', '.join([str(_) for _ in self[-2:]])
            number = len(self) - 4
            middle = ', ... [{}] ..., '.format(number)
            return left + middle + right

    def _get_duration(self, in_seconds=False):
        return sum(_._get_duration(in_seconds=in_seconds) for _ in self)

    def _get_duration_in_seconds(self):
        import abjad
        duration = abjad.Duration(0)
        for leaf in self.leaves:
            duration += leaf._get_duration(in_seconds=True)
        return duration

    def _get_format_specification(self):
        import abjad
        agent = abjad.StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if self._get_compact_summary() == '':
            values = []
        else:
            values = [self._get_compact_summary()]
        if 'overrides' in names and not self.overrides:
            names.remove('overrides')
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=values,
            storage_format_kwargs_names=names,
            )

    def _get_indicators(self, prototype=None, name=None, unwrap=True):
        import abjad
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
        for indicator in self._indicator_wrappers:
            if name is not None and indicator._name != name:
                continue
            if isinstance(indicator, prototype_classes):
                matching_indicators.append(indicator)
            elif any(indicator == x for x in prototype_objects):
                matching_indicators.append(indicator)
            elif isinstance(indicator, abjad.IndicatorWrapper):
                if isinstance(indicator.indicator, prototype_classes):
                    matching_indicators.append(indicator)
                elif any(indicator.indicator == x for x in prototype_objects):
                    matching_indicators.append(indicator)
        if unwrap:
            matching_indicators = [x.indicator for x in matching_indicators]
        matching_indicators = tuple(matching_indicators)
        return matching_indicators

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        return bundle

    def _get_my_first_leaf(self):
        if self.leaves:
            return self.leaves[0]

    def _get_my_last_leaf(self):
        if self.leaves:
            return self.leaves[-1]

    def _get_my_nth_leaf(self, n):
        return self.leaves[n]

    def _get_piecewise_indicator(self, leaf, prototype=None):
        indicators = self._get_piecewise_indicators(leaf, prototype)
        if not indicators:
            message = 'no piecewise indicator found.'
            raise Exception(message)
        if len(indicators) == 1:
            return indicators[0]
        message = 'multiple piecewise indicators found.'
        raise Exception(message)

    def _get_piecewise_indicators(self, leaf, prototype=None):
        import abjad
        assert leaf in self, repr(leaf)
        indicators = []
        for wrapper in abjad.inspect(leaf).get_indicators(
            prototype,
            unwrap=False,
            ):
            if wrapper.is_piecewise and wrapper.piecewise_spanner is self:
                indicators.append(wrapper.indicator)
        return indicators

    def _get_preprolated_duration(self):
        return sum([_._get_preprolated_duration() for _ in self])

    def _get_summary(self):
        if 0 < len(self):
            return ', '.join([str(_) for _ in self])
        else:
            return ' '

    def _get_timespan(self, in_seconds=False):
        import abjad
        if len(self):
            timespan_ = self[0]._get_timespan(in_seconds=in_seconds)
            start_offset = timespan_.start_offset
            timespan_ = self[-1]._get_timespan(in_seconds=in_seconds)
            stop_offset = timespan_.stop_offset
        else:
            start_offset = abjad.Duration(0)
            stop_offset = abjad.Duration(0)
        return abjad.Timespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            )

    def _has_piecewise_indicator(self, leaf, prototype=None):
        indicators = self._get_piecewise_indicators(leaf, prototype)
        return bool(indicators)

    def _index(self, leaf):
        return self._leaves.index(leaf)

    def _insert(self, i, leaf):
        r'''Not composer-safe.
        '''
        import abjad
        if not isinstance(leaf, abjad.Leaf):
            message = 'spanners attach only to leaves: {!s}.'
            message = message.format(leaf)
            raise Exception(message)
        leaf._spanners.add(self)
        self._leaves.insert(i, leaf)

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
        if leaf not in self.leaves:
            return False
        if len(self.leaves) < 3:
            return False
        leaf_count = len(self.leaves)
        first_index = 0
        last_index = leaf_count - 1
        leaf_index = list(self.leaves).index(leaf)
        if first_index < leaf_index < last_index:
            return True
        return False

    def _is_my_first(self, leaf, prototype):
        leaves = [_ for _ in self if isinstance(_, prototype)]
        return (leaves and leaves[0] is leaf)

    def _is_my_first_leaf(self, leaf):
        return (self.leaves and self.leaves[0] is leaf)

    def _is_my_last(self, leaf, prototype):
        leaves = [_ for _ in self if isinstance(_, prototype)]
        return (leaves and leaves[-1] is leaf)

    def _is_my_last_leaf(self, leaf):
        return (self.leaves and self.leaves[-1] is leaf)

    def _is_my_only(self, leaf, prototype):
        leaves = [_ for _ in self if isinstance(_, prototype)]
        return (leaves and len(leaves) == 1 and leaves[0] is leaf)

    def _is_my_only_leaf(self, leaf):
        return len(self) == 1 and self.leaves[0] is leaf

    def _remove(self, leaf):
        r'''Not composer-safe.
        '''
        self._sever_leaf(leaf)

    def _remove_leaf(self, leaf):
        r'''Not composer-safe.
        '''
        for i, leaf_ in enumerate(self.leaves):
            if leaf_ is leaf:
                self._leaves.pop(i)
                break
        else:
            message = '{!r} not in spanner.'
            raise ValueError(message.format(leaf))

    # TODO: remove
    def _reverse_leaves(self):
        r'''Reverses order of spanner leaves.

        Not composer-safe because reversing the order of spanner leaves
        could scramble leaves of some other spanner.

        Call method only as part of a full leaf- and spanner-reversal
        routine.

        Spanner subclasses with mapping variables (like the 'durations' list
        attaching to durated complex beam spanners) should override this
        method to reverse mapping elements.
        '''
        self._leaves.reverse()

    def _sever_all_leaves(self):
        r'''Not composer-safe.
        '''
        for i in reversed(range(len(self))):
            leaf = self[i]
            self._sever_leaf(leaf)

    def _sever_leaf(self, leaf):
        r'''Not composer-safe.
        '''
        self._block_leaf(leaf)
        self._remove_leaf(leaf)

    def _start_offset_in_me(self, leaf):
        import abjad
        leaf_start_offset = abjad.inspect(leaf).get_timespan().start_offset
        self_start_offset = abjad.inspect(self).get_timespan().start_offset
        return leaf_start_offset - self_start_offset

    def _stop_offset_in_me(self, leaf):
        leaf_start_offset = self._start_offset_in_me(leaf)
        leaf_stop_offset = leaf_start_offset + leaf._get_duration()
        return leaf_stop_offset

    def _unblock_all_leaves(self):
        r'''Not composer-safe.
        '''
        for leaf in self:
            self._unblock_leaf(leaf)

    def _unblock_leaf(self, leaf):
        r'''Not composer-safe.
        '''
        leaf._spanners.add(self)

    def _unconstrain_contiguity(self):
        r'''Not composer-safe.
        '''
        self._contiguity_constraint = None

    ### PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        r'''Gets leaves in spanner.

        Returns selection of leaves.
        '''
        import abjad
        for leaf in self._leaves:
            if not isinstance(leaf, abjad.Leaf):
                message = 'spanners attach only to leaves: {!s}.'
                message = message.format(leaf)
                raise Exception(message)
        return abjad.select(self._leaves)

    @property
    def name(self):
        r'''Gets spanner name.

        Returns string.
        '''
        return self._name

    @property
    def overrides(self):
        r'''Gets overrides.

        Returns dictionary.
        '''
        import abjad
        manager = abjad.override(self)
        overrides = {}
        for attribute_tuple in manager._get_attribute_tuples():
            attribute = '__'.join(attribute_tuple[:-1])
            value = attribute_tuple[-1]
            overrides[attribute] = value
        return overrides


collections.Sequence.register(Spanner)
