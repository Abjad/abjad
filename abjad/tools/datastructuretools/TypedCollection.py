# -*- coding: utf-8 -*-
import abc
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class TypedCollection(AbjadObject):
    r'''Abstract typed collection.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_collection',
        '_item_class',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        assert isinstance(item_class, (type(None), type))
        self._item_class = item_class

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        r'''Is true when typed collection contains `item`.
        Otherwise false.

        Returns true or false.
        '''
        try:
            item = self._item_coercer(item)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __eq__(self, argument):
        r'''Is true when `argument` is a typed collection with items that
        compare equal to those of this typed collection. Otherwise false.

        Returns true or false.
        '''
        if issubclass(type(argument), type(self)):
            return self._collection == argument._collection
        elif isinstance(argument, type(self._collection)):
            return self._collection == argument
        return False

    def __hash__(self):
        r'''Hashes typed collection.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(TypedCollection, self).__hash__()

    def __iter__(self):
        r'''Iterates typed collection.

        Returns generator.
        '''
        return self._collection.__iter__()

    def __len__(self):
        r'''Gets length of typed collection.

        Returns nonnegative integer.
        '''
        return len(self._collection)

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def coerce_(x):
            if isinstance(x, self._item_class):
                return x
            return self._item_class(x)
        if self._item_class is None:
            return lambda x: x
        return coerce_

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        if 'items' in names:
            names.remove('items')
        return systemtools.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self._collection],
            storage_format_kwargs_names=names,
            )

    def _on_insertion(self, item):
        r'''Override to operate on item after insertion into collection.
        '''
        pass

    def _on_removal(self, item):
        r'''Override to operate on item after removal from collection.
        '''
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Gets item class of collection.
        
        Collection coerces items according to `item_class`.

        Returns class.
        '''
        return self._item_class

    @property
    def items(self):
        r'''Gets items in collection.

        Returns list.
        '''
        return [_ for _ in self]
