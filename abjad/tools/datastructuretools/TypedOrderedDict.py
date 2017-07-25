# -*- coding: utf-8 -*-
import collections
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedOrderedDict(TypedCollection):
    r'''Typed ordered dictionary.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from list of pairs:

        ::

            >>> dictionary = abjad.TypedOrderedDict([
            ...     ('color', 'red'),
            ...     ('directive', abjad.Markup(r'\italic Allegretto')),
            ...     ])

        ::

            >>> f(dictionary)
            abjad.TypedOrderedDict(
                [
                    ('color', 'red'),
                    (
                        'directive',
                        abjad.Markup(
                            contents=[
                                abjad.MarkupCommand(
                                    'italic',
                                    'Allegretto'
                                    ),
                                ],
                            ),
                        ),
                    ]
                )

    ..  container:: example

        Initializes from built-in dictionary:

        ::

            >>> dictionary = {
            ...     'color': 'red',
            ...     'directive': abjad.Markup(r'\italic Allegretto'),
            ...     }
            >>> dictionary = abjad.TypedOrderedDict(
            ...     dictionary
            ...     )

        ::

            >>> f(dictionary)
            abjad.TypedOrderedDict(
                [
                    ('color', 'red'),
                    (
                        'directive',
                        abjad.Markup(
                            contents=[
                                abjad.MarkupCommand(
                                    'italic',
                                    'Allegretto'
                                    ),
                                ],
                            ),
                        ),
                    ]
                )

    ..  container:: example

        Initializes from other typed ordered dictionary:

        ::

            >>> dictionary_1 = abjad.TypedOrderedDict([
            ...     ('color', 'red'),
            ...     ('directive', abjad.Markup(r'\italic Allegretto')),
            ...     ])
            >>> dictionary_2 = abjad.TypedOrderedDict(
            ...     dictionary_1
            ...     )

        ::

            >>> f(dictionary_2)
            abjad.TypedOrderedDict(
                [
                    ('color', 'red'),
                    (
                        'directive',
                        abjad.Markup(
                            contents=[
                                abjad.MarkupCommand(
                                    'italic',
                                    'Allegretto'
                                    ),
                                ],
                            ),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        TypedCollection.__init__(
            self,
            item_class=item_class,
            )
        if isinstance(items, dict):
            items = sorted(items.items())
        elif isinstance(items, collections.Mapping):
            items = list(items.items())
        items = items or []
        the_items = []
        for item in items:
            assert len(item) == 2, repr(item)
            key = item[0]
            value = self._item_coercer(item[1])
            the_item = (key, value)
            the_items.append(the_item)
        self._collection = collections.OrderedDict(the_items)

    ### SPECIAL METHODS ###

    def __cmp__(self, argument):
        r'''Aliases OrderedDict.__cmp__().

        Returns true or false.
        '''
        assert isinstance(argument, type(self))
        ordered_dictionary = argument._collection
        return self._collection.__cmp__(ordered_dictionary)

    def __contains__(self, key):
        r'''Aliases OrderedDict.__contains__().

        Returns true or false.
        '''
        return key in self._collection

    def __delitem__(self, i):
        r'''Aliases OrderedDict.__delitem__().

        Returns none.
        '''
        del(self._collection[i])

    def __ge__(self, argument):
        r'''Is true when typed ordered dictionary is greater than or equal
        to `argument`. Otherwise false.

        Returns true or false.
        '''
        argument = type(self)(argument)
        return self._collection.__ge__(argument._collection)

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        Returns item or slice.
        '''
        return self._collection.__getitem__(argument)

    def __gt__(self, argument):
        r'''Is true when typed ordered dictionary is greater than `argument`.
        Otherwise false.

        Returns true or false.
        '''
        argument = type(self)(argument)
        return self._collection.__gt__(argument._collection)

    def __le__(self, argument):
        r'''Is true when typed ordered dictionary is less than or equal
        to `argument`. Otherwise false.

        Returns true or false.
        '''
        argument = type(self)(argument)
        return self._collection.__le__(argument._collection)

    def __lt__(self, argument):
        r'''Is true when typed ordered dictionary is less than `argument`.
        Otherwise false.

        Returns true or false.
        '''
        argument = type(self)(argument)
        return self._collection.__lt__(argument._collection)

    def __reversed__(self):
        r'''Aliases OrderedDict.__reversed__().

        Returns generatos.
        '''
        return self._collection.__reversed__()

    def __setitem__(self, i, argument):
        r'''Changes items in `argument` to items and sets.

        Returns none.
        '''
        new_item = self._item_coercer(argument)
        self._collection[i] = new_item

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        if 'items' in names:
            names.remove('items')
        values = [list(self._collection.items())]
        return systemtools.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=values,
            storage_format_kwargs_names=names,
            storage_format_includes_root_package=True,
            )

    ### PUBLIC METHODS ###

    def clear(self):
        r'''Clears typed ordered dictionary.

        Returns none.
        '''
        self._collection.clear()

    def copy(self):
        r'''Copies typed ordered dictionary.

        Returns new typed ordered dictionary.
        '''
        ordered_dictionary = self._collection.copy()
        items = list(ordered_dictionary.items())
        return type(self)(
            item_class=self.item_class,
            items=items,
            )

    def get(self, i, default=None):
        r'''Aliases OrderedDict.get().

        Returns item or raises key error.
        '''
        return self._collection.get(i, default)

    def has_key(self, key):
        r'''Aliases OrderdDict.has_key().

        Returns true or false.
        '''
        return key in self._collection

    def items(self):
        r'''Aliases OrderedDict.items().

        Returns generator.
        '''
        return iter(self._collection.items())

    def keys(self):
        r'''Aliases OrderedDict.keys().

        Returns generator.
        '''
        return iter(self._collection.keys())

    def pop(self, key, default=None):
        r'''Aliases OrderedDict.pop().

        Returns items.
        '''
        return self._collection.pop(key, default)

    def popitem(self):
        r'''Aliases OrderedDict.popitem().

        Returns generator.
        '''
        return self._collection.popitem()

    def setdefault(self, key, default=None):
        r'''Aliases OrderedDict.setdefault().

        Returns items.
        '''
        return self._collection.setdefault(key, default)

    def update(self, *arguments, **keywords):
        r'''Aliases OrderedDict.update().

        Returns none.
        '''
        return self._collection.update(*arguments, **keywords)

    def values(self):
        r'''Aliases OrderedDict.values().

        Returns generator.
        '''
        return iter(self._collection.values())


collections.MutableMapping.register(TypedOrderedDict)
