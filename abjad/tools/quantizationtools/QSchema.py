# -*- coding: utf-8 -*-
import abc
import bisect
import copy
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadObject


class QSchema(AbjadObject):
    r'''The *schema* for a quantization run.

    ``QSchema`` allows for the specification of quantization settings
    diachronically, at any time-step of the quantization process.

    In practice, this provides a means for the composer to change the tempo,
    search-tree, time-signature etc., effectively creating a template into
    which quantized rhythms can be "poured", without yet knowing what those
    rhythms might be, or even how much time the ultimate result will take.
    Like Abjad indicators the settings made at any given time-step via
    a ``QSchema`` instance are understood to persist until changed.

    All concrete ``QSchema`` subclasses strongly implement default values for
    all of their parameters.

    `QSchema` is abstract.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        '_lookups',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        if 1 == len(args) and isinstance(args[0], type(self)):
            items = copy.copy(args[0].items)
        elif 1 == len(args) and isinstance(args[0], dict):
            items = list(args[0].items())
            if mathtools.all_are_pairs_of_types(items, int, dict):
                items = [(x, self.item_class(**y)) for x, y in items]
            assert mathtools.all_are_pairs_of_types(
                items, int, self.item_class)
            items = dict(items)
        elif mathtools.all_are_pairs_of_types(args, int, self.item_class):
            items = dict(args)
        elif mathtools.all_are_pairs_of_types(args, int, dict):
            items = [(x, self.item_class(**y)) for x, y in args]
            items = dict(items)
        elif all(isinstance(x, self.item_class) for x in args):
            items = [(i, x) for i, x in enumerate(args)]
            items = dict(items)
        elif all(isinstance(x, dict) for x in args):
            items = [(i, self.item_class(**x)) for i, x in enumerate(args)]
            items = dict(items)
        else:
            raise ValueError
        if items:
            assert 0 <= min(items)
        self._items = dict(items)
        self._lookups = self._create_lookups()

    ### SPECIAL METHODS ###

    def __call__(self, duration):
        r'''Calls QSchema on `duration`.
        '''
        target_items = []
        idx, current_offset = 0, 0
        while current_offset < duration:
            lookup = self[idx]
            lookup['offset_in_ms'] = current_offset
            target_item = self.target_item_class(**lookup)
            target_items.append(target_item)
            current_offset += target_item.duration_in_ms
            idx += 1
        return self.target_class(target_items)

    def __format__(self, format_specification=''):
        r'''Formats q-event.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __getitem__(self, i):
        r'''Gets item `i` in QSchema.
        '''
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

    ### PRIVATE METHODS ###

    def _create_lookups(self):
        names = self._keyword_argument_names
        lookups = {}
        for name in names:
            lookups[name] = {0: getattr(self, name)}
            for position, item in self.items.items():
                value = getattr(item, name)
                if value is not None:
                    lookups[name][position] = value
            lookups[name] = dict(lookups[name])
        return dict(lookups)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def item_class(self):
        r'''The schema's item class.
        '''
        raise NotImplementedError

    @property
    def items(self):
        r'''The item dictionary.
        '''
        return self._items

    @property
    def search_tree(self):
        r'''The default search tree.
        '''
        return self._search_tree

    @abc.abstractproperty
    def target_class(self):
        r'''The schema's target class.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def target_item_class(self):
        r'''The schema's target class' item class.
        '''
        raise NotImplementedError

    @property
    def tempo(self):
        r'''The default tempo.
        '''
        return self._tempo
