# -*- coding: utf-8 -*-
import collections
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TypedCollection import TypedCollection


class TypedOrderedDict(TypedCollection):
    r'''A typed ordered dictionary.

    ..  container:: example

        **Example 1.** Initializes from list of pairs:

        ::

            >>> dictionary = datastructuretools.TypedOrderedDict([
            ...     ('color', 'red'),
            ...     ('directive', Markup(r'\italic Allegretto')),
            ...     ])

        ::

            >>> print(format(dictionary))
            abjad.datastructuretools.TypedOrderedDict(
                [
                    ('color', 'red'),
                    (
                        'directive',
                        markuptools.Markup(
                            contents=(
                                markuptools.MarkupCommand(
                                    'italic',
                                    'Allegretto'
                                    ),
                                ),
                            ),
                        ),
                    ]
                )

    ..  container:: example

        **Example 2.** Initializes from built-in dictionary:

        ::

            >>> dictionary = {
            ...     'color': 'red',
            ...     'directive': Markup(r'\italic Allegretto'),
            ...     }
            >>> dictionary = datastructuretools.TypedOrderedDict(
            ...     dictionary
            ...     )

        ::

            >>> print(format(dictionary))
            abjad.datastructuretools.TypedOrderedDict(
                [
                    ('color', 'red'),
                    (
                        'directive',
                        markuptools.Markup(
                            contents=(
                                markuptools.MarkupCommand(
                                    'italic',
                                    'Allegretto'
                                    ),
                                ),
                            ),
                        ),
                    ]
                )

    ..  container:: example

        **Example 3.** Initializes from other typed ordered dictionary:

        ::

            >>> dictionary_1 = datastructuretools.TypedOrderedDict([
            ...     ('color', 'red'),
            ...     ('directive', Markup(r'\italic Allegretto')),
            ...     ])
            >>> dictionary_2 = datastructuretools.TypedOrderedDict(
            ...     dictionary_1
            ...     )

        ::

            >>> print(format(dictionary_2))
            abjad.datastructuretools.TypedOrderedDict(
                [
                    ('color', 'red'),
                    (
                        'directive',
                        markuptools.Markup(
                            contents=(
                                markuptools.MarkupCommand(
                                    'italic',
                                    'Allegretto'
                                    ),
                                ),
                            ),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

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

    def __cmp__(self, expr):
        r'''Aliases OrderedDict.__cmp__().

        Returns true or false.
        '''
        assert isinstance(expr, type(self))
        ordered_dictionary = expr._collection
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

    def __ge__(self, expr):
        r'''Is true when typed ordered dictionary is greater than or equal
        to `expr`. Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__ge__(expr._collection)

    def __getitem__(self, i):
        r'''Aliases OrderedDict.__getitem__().

        Returns item.
        '''
        return self._collection[i]

    def __gt__(self, expr):
        r'''Is true when typed ordered dictionary is greater than `expr`.
        Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__gt__(expr._collection)

    def __le__(self, expr):
        r'''Is true when typed ordered dictionary is less than or equal
        to `expr`. Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__le__(expr._collection)

    def __lt__(self, expr):
        r'''Is true when typed ordered dictionary is less than `expr`.
        Otherwise false.

        Returns true or false.
        '''
        expr = type(self)(expr)
        return self._collection.__lt__(expr._collection)

    def __ne__(self, expr):
        r'''Is true when typed ordered dictionary is not equal to `expr`.
        Otherwise false.

        Returns true or false.
        '''
        return not self == expr

    def __reversed__(self):
        r'''Aliases OrderedDict.__reversed__().

        Returns generatos.
        '''
        return self._collection.__reversed__()

    def __setitem__(self, i, expr):
        r'''Changes items in `expr` to items and sets.

        Returns none.
        '''
        new_item = self._item_coercer(expr)
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

    def update(self, *args, **kwargs):
        r'''Aliases OrderedDict.update().

        Returns none.
        '''
        return self._collection.update(*args, **kwargs)

    def values(self):
        r'''Aliases OrderedDict.values().

        Returns generator.
        '''
        return iter(self._collection.values())


collections.MutableMapping.register(TypedOrderedDict)
