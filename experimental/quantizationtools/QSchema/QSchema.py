from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
import bisect
import copy


class QSchema(abctools.AbjadObject):
    '''The schema for a quantization run.

    `QSchema` is abstract.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items', '_lookups')

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, *args, **kwargs):
        if 1 == len(args) and isinstance(args[0], type(self)):
            items = copy.copy(args[0].items)

        elif 1 == len(args) and isinstance(args[0], dict):
            items = args[0].items()
            if items:
                assert 0 <= min(items)
            assert sequencetools.all_are_pairs_of_types(items, int, self.item_klass)

        elif sequencetools.all_are_pairs_of_types(args, int, self.item_klass):
            items = dict(args)
            if items:
                assert 0 <= min(items)
            
        elif all([isinstance(x, self.item_klass) for x in args]):
            items = [(i, x) for i, x in enumerate(args)]

        else:
            raise ValueError

        self._items = datastructuretools.ImmutableDictionary(items)

        self._lookups = self._create_lookups()

    ### SPECIAL METHODS ###

    def __call__(self, duration):
        targets = []
        idx, current_offset = 0, 0
        while current_offset < duration:
            lookup = self[idx]
            lookup['offset_in_ms'] = current_offset
            target = self.target_klass(**lookup)
            targets.append(target)
            current_offset += target.duration_in_ms
            idx += 1
        return tuple(targets)

    def __getitem__(self, i):
        assert isinstance(i, int) and 0 <= i
        result = {}
        for field in self._lookups:
            lookup = self._lookups[field].get(i)
            if lookup is not None:
                result[field] = lookup
            else:
                keys = sorted(self._lookups[field].keys())
                idx = bisect.bisect(keys, i)
                if len(keys) == idx:
                    key = keys[-1]
                elif i < keys[idx]:
                    key = keys[idx - 1]
                result[field] = self._lookups[field][key]
        return result

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def cyclic(self):
        '''True if the schema should generate its QTarget cyclically.'''
        return self._cyclic

    @abstractproperty
    def item_klass(self):
        '''The schema's item class.'''
        raise NotImplemented

    @property
    def items(self):
        '''The item dictionary.'''
        return self._items

    @property
    def search_tree(self):
        '''The default search tree.'''
        return self._search_tree

    @abstractproperty
    def target_klass(self):
        '''The schema's target class.'''
        raise NotImplemented

    @property
    def tempo(self):
        '''The default tempo.'''
        return self._tempo

    ### PRIVATE METHODS ###

    def _create_lookups(self):
        lookups = {}
        fields = self.item_klass._fields
        for field in fields:
            lookups[field] = {0: getattr(self, field)}
            for position, item in self.items.iteritems():
                value = getattr(item, field)
                if value is not None:
                    lookups[field][position] = value
            lookups[field] = datastructuretools.ImmutableDictionary(lookups[field])
        return datastructuretools.ImmutableDictionary(lookups)

    def _get_tools_package_qualified_repr_pieces(self):
        if not len(self.items):
            return ['{}()'.format(self._tools_package_qualified_class_name)]
        result = ['{}({{'.format(self._tools_package_qualified_class_name)]
        for key, value in sorted(self.items.items()):
            value_repr = value._get_tools_package_qualified_repr_pieces()
            result.append('\t{}: {}'.format(key, value_repr[0]))
            result.extend(['\t' + x for x in value_repr[1:-1]])
            result.append('\t{},'.format(value_repr[-1]))
        result.append('\t})')
        return result

