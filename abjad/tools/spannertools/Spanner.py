import collections
import copy
import typing
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.datastructuretools import Left
from abjad.tools.datastructuretools import Right
from abjad.tools.datastructuretools.Duration import Duration
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from abjad.tools.scoretools.Leaf import Leaf
from abjad.tools.scoretools.Selection import Selection
from abjad.tools.systemtools.LilyPondFormatManager import LilyPondFormatManager
from abjad.tools.systemtools.Wrapper import Wrapper
from abjad.tools.segmenttools.Tags import Tags
from abjad.tools.systemtools.FormatSpecification import FormatSpecification
from abjad.tools.systemtools.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.tools.systemtools.StorageFormatManager import StorageFormatManager
from abjad.tools.systemtools.Tag import Tag
from abjad.tools.timespantools.Timespan import Timespan
from abjad.tools.topleveltools.attach import attach
from abjad.tools.topleveltools.inspect import inspect
from abjad.tools.topleveltools.override import override
from abjad.tools.topleveltools.select import select
from abjad.tools.topleveltools.setting import setting
from abjad.tools.topleveltools.tweak import tweak
abjad_tags = Tags()


class Spanner(AbjadObject, collections.Sequence):
    '''Spanner.

    Any object that stretches horizontally and encompasses leaves.

    Examples include beams, slurs, hairpins and trills.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contiguity_constraint',
        '_deactivate',
        '_ignore_attachment_test',
        '_ignore_before_attach',
        '_leaves',
        '_left_broken',
        '_lilypond_grob_name_manager',
        '_lilypond_setting_name_manager',
        '_lilypond_tweak_manager',
        '_right_broken',
        '_tag',
        '_wrappers',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides: OrderedDict = None,
        ) -> None:
        overrides = overrides or OrderedDict()
        self._contiguity_constraint = 'logical voice'
        self._apply_overrides(overrides)
        self._deactivate = None
        self._ignore_attachment_test = None
        self._ignore_before_attach = None
        self._leaves: typing.List[Leaf] = []
        self._left_broken = None
        self._lilypond_setting_name_manager = None
        self._lilypond_tweak_manager = None
        self._right_broken = None
        self._tag = None
        self._wrappers: typing.List[Wrapper] = []

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
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_lilypond_grob_name_manager', None) is not None:
            new._lilypond_grob_name_manager = copy.copy(override(self))
        if getattr(self, '_lilypond_setting_name_manager', None) is not None:
            new._lilypond_setting_name_manager = copy.copy(setting(self))
        if getattr(self, '_lilypond_tweak_manager', None) is not None: new._lilypond_tweak_manager = copy.copy(tweak(self))
        self._copy_keyword_args(new)
        return new

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        Returns leaf.
        '''
        if isinstance(argument, slice):
            leaves = self.leaves.__getitem__(argument)
            return select(leaves)
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
        if self._ignore_attachment_test:
            pass
        elif not self._attachment_test(leaf):
            message = f'can not attach {self!r} to {leaf!r}.'
            raise Exception(message)
        if self._contiguity_constraint == 'logical voice':
            leaves = self[-1:] + [leaf]
            leaves = select(leaves)
            if not leaves.are_contiguous_logical_voice():
                raise Exception(type(self), leaves)
        leaf._append_spanner(self)
        self._leaves.append(leaf)

    def _append_left(self, leaf):
        leaves = [leaf] + self[:1]
        leaves = select(leaves)
        assert leaves.are_contiguous_logical_voice()
        leaf._append_spanner(self)
        self._leaves.insert(0, leaf)

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

    def _at_least_two_leaves(self, argument):
        leaves = select(argument).leaves()
        if 1 < len(leaves):
            return True
        return [
            'Requires at least two leaves.',
            f'Not just {leaves[0]!r}.',
            ]

    def _attach(
        self,
        argument,
        deactivate=None,
        left_broken=None,
        right_broken=None,
        tag=None,
        ):
        assert not self, repr(self)
        assert isinstance(argument, Selection), repr(argument)
        assert argument.are_leaves(), repr(argument)
        self._extend(argument)
        self._deactivate = deactivate
        self._left_broken = left_broken
        self._right_broken = right_broken
        if tag is not None:
            tag = Tag(tag)
        self._tag = tag

    def _attach_piecewise(
        self,
        indicator,
        leaf,
        alternate=None,
        deactivate=None,
        tag=None,
        wrapper=None,
        ):
        if leaf not in self:
            raise Exception(f'must be leaf in spanner: {leaf!r}.')
        if isinstance(indicator, Wrapper):
            alternate = indicator.alternate
            annotation = indicator.annotation
            context = indicator.context
            deactivate = deactivate or indicator.deactivate
            synthetic_offset = indicator.synthetic_offset
            tag = tag or indicator.tag
            indicator._detach()
            indicator = indicator.indicator
        context = getattr(self, 'context', None)
        context = context or getattr(indicator, 'context', None)
        wrapper_ = Wrapper(
            alternate=alternate,
            component=leaf,
            context=context,
            deactivate=deactivate,
            indicator=indicator,
            spanner=self,
            tag=tag,
            )
        wrapper_._bind_to_component(leaf)
        self._wrappers.append(wrapper_)
        if wrapper:
            return wrapper_

    def _attachment_test(self, argument):
        return isinstance(argument, Leaf)

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
        leaf._remove_spanner(self)

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
        leaf_input = list(self[-1:])
        leaf_input.extend(leaves)
        leaf_input = select(leaf_input)
        if self._contiguity_constraint == 'logical voice':
            if not leaf_input.are_contiguous_logical_voice():
                message = f'{self!r} leaves must be contiguous:\n'
                message += f'  {leaf_input}'
                raise Exception(message)
        for leaf in leaves:
            self._append(leaf)

    def _extend_left(self, leaves):
        leaf_input = leaves + list(self[:1])
        leaf_input = select(leaf_input)
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
        bundle = LilyPondFormatBundle()
        if leaf is self[-1]:
            contributions = override(self)._list_format_contributions(
                'revert',
                )
            bundle.grob_reverts.extend(contributions)
        if leaf is self[0]:
            contributions = override(self)._list_format_contributions(
                'override',
                once=False,
                )
            bundle.grob_overrides.extend(contributions)
            contributions = tweak(self)._list_format_contributions()
            bundle.right.spanner_starts.extend(contributions)
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
        duration = Duration(0)
        for leaf in self.leaves:
            duration += leaf._get_duration(in_seconds=True)
        return duration

    def _get_format_specification(self):
        agent = StorageFormatManager(self)
        names = list(agent.signature_keyword_names)
        if self._get_compact_summary() == '':
            values = []
        else:
            values = [self._get_compact_summary()]
        if 'overrides' in names and not self.overrides:
            names.remove('overrides')
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_args_values=values,
            storage_format_kwargs_names=names,
            )

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
        matching_indicators = []
        for wrapper in self._wrappers:
            if isinstance(wrapper, prototype_classes):
                matching_indicators.append(wrapper)
            elif any(wrapper == x for x in prototype_objects):
                matching_indicators.append(wrapper)
            elif isinstance(wrapper, Wrapper):
                if isinstance(wrapper.indicator, prototype_classes):
                    matching_indicators.append(wrapper)
                elif any(wrapper.indicator == x for x in prototype_objects):
                    matching_indicators.append(wrapper)
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
            message = 'no piecewise {prototype!s} indicator found.'
            raise Exception(message)
        if len(indicators) == 1:
            return indicators[0]
        message = f'multiple piecewise {prototype!s} indicators found.'
        raise Exception(message)

    def _get_piecewise_indicators(self, leaf, prototype=None):
        assert leaf in self, repr(leaf)
        indicators = []
        for wrapper in inspect(leaf).wrappers(prototype):
            if wrapper.spanner is self:
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
        if len(self):
            timespan_ = self[0]._get_timespan(in_seconds=in_seconds)
            start_offset = timespan_.start_offset
            timespan_ = self[-1]._get_timespan(in_seconds=in_seconds)
            stop_offset = timespan_.stop_offset
        else:
            start_offset = Duration(0)
            stop_offset = Duration(0)
        return Timespan(
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
        if not isinstance(leaf, Leaf):
            message = 'spanners attach only to leaves: {!s}.'
            message = message.format(leaf)
            raise Exception(message)
        leaf._append_spanner(self)
        self._leaves.insert(i, leaf)

    def _is_exterior_leaf(self, leaf):
        r'''True if leaf is first or last in spanner.
        True if next leaf or previous leaf is none.
        Otherwise false.
        '''
        if leaf is self[0]:
            return True
        elif leaf is self[-1]:
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

    def _is_trending(self, leaf):
        return False

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
            raise ValueError(f'{leaf!r} not in spanner.')

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
        leaf_start_offset = inspect(leaf).get_timespan().start_offset
        self_start_offset = inspect(self).get_timespan().start_offset
        return leaf_start_offset - self_start_offset

    def _stop_offset_in_me(self, leaf):
        leaf_start_offset = self._start_offset_in_me(leaf)
        leaf_stop_offset = leaf_start_offset + leaf._get_duration()
        return leaf_stop_offset

    @staticmethod
    def _tag_hide(strings):
        return LilyPondFormatManager.tag(
            strings,
            deactivate=False,
            tag=abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS,
            )

    @staticmethod
    def _tag_show(strings):
        return LilyPondFormatManager.tag(
            strings,
            deactivate=True,
            tag=abjad_tags.SHOW_TO_JOIN_BROKEN_SPANNERS,
            )

    def _unblock_all_leaves(self):
        r'''Not composer-safe.
        '''
        for leaf in self:
            self._unblock_leaf(leaf)

    def _unblock_leaf(self, leaf):
        r'''Not composer-safe.
        '''
        leaf._append_spanner(self)

    def _unconstrain_contiguity(self):
        r'''Not composer-safe.
        '''
        self._contiguity_constraint = None

    ### PUBLIC PROPERTIES ###

    @property
    def leaves(self) -> Selection:
        r'''Gets leaves in spanner.
        '''
        for leaf in self._leaves:
            if not isinstance(leaf, Leaf):
                message = f'spanners attach only to leaves (not {leaf!s}).'
                raise Exception(message)
        return select(self._leaves)

    @property
    def overrides(self) -> OrderedDict:
        r'''Gets overrides.
        '''
        manager = override(self)
        overrides = OrderedDict()
        for attribute_tuple in manager._get_attribute_tuples():
            attribute = '__'.join(attribute_tuple[:-1])
            value = attribute_tuple[-1]
            overrides[attribute] = value
        return overrides
