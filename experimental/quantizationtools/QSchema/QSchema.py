import abc
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

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        if 1 == len(args) and isinstance(args[0], type(self)):
            items = copy.copy(args[0].items)

        elif 1 == len(args) and isinstance(args[0], dict):
            items = args[0].items()
            if items:
                assert 0 <= min(items)
            if sequencetools.all_are_pairs_of_types(items, int, dict):
                items = [(x, self.item_klass(**y)) for x, y in items]
            assert sequencetools.all_are_pairs_of_types(items, int, self.item_klass)

        elif sequencetools.all_are_pairs_of_types(args, int, self.item_klass):
            items = dict(args)
            if items:
                assert 0 <= min(items)
            
        elif all([isinstance(x, self.item_klass) for x in args]):
            items = [(i, x) for i, x in enumerate(args)]

        elif all([isinstance(x, dict) for x in args]):
            items = [(i, self.item_klass(**x)) for i, x in enumerate(args)]

        else:
            raise ValueError

        self._items = datastructuretools.ImmutableDictionary(items)

        self._lookups = self._create_lookups()

    ### SPECIAL METHODS ###

    def __call__(self, duration):
        target_items = []
        idx, current_offset = 0, 0
        while current_offset < duration:
            lookup = self[idx]
            lookup['offset_in_ms'] = current_offset
            target_item = self.target_item_klass(**lookup)
            target_items.append(target_item)
            current_offset += target_item.duration_in_ms
            idx += 1
        return self.target_klass(target_items)

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
        if self.items:
            result = ['{}({{'.format(self._tools_package_qualified_class_name)]
            for i, pair in enumerate(sorted(self.items.items())):
                key, value = pair
                itemrepr = value._get_tools_package_qualified_repr_pieces()
                result.append('\t{}: {}'.format(key, itemrepr[0]))
                result.extend(['\t{}'.format(x) for x in itemrepr[1:-1]])
                if i == len(self.items) - 1:
                    result.append('\t{}'.format(itemrepr[-1]))
                else:
                    result.append('\t{},'.format(itemrepr[-1]))
            result.append('\t},')
        else:
            result = ['{}('.format(self._tools_package_qualified_class_name)]
        result.extend(self._get_tools_package_qualified_keyword_argument_repr_pieces())
        result.append('\t)')
        return '\n'.join(result)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _keyword_argument_names(self):
        raise NotImplemented

    @property
    def _mandatory_argument_names(self):
        return ('items',)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
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

    @abc.abstractproperty
    def target_item_klass(self):
        '''The schema's target class' item class.'''
        raise NotImplemented

    @abc.abstractproperty
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

