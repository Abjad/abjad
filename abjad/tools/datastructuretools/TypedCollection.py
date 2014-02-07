# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TypedCollection(AbjadObject):
    r'''Abstract base class for typed collections.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_collection',
        '_custom_identifier',
        '_item_class',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, tokens=None, item_class=None, custom_identifier=None):
        assert isinstance(item_class, (type(None), type))
        self._item_class = item_class
        if isinstance(tokens, type(self)):
            custom_identifier = tokens.custom_identifier or custom_identifier
        self._custom_identifier = custom_identifier

    ### SPECIAL METHODS ###

    def __contains__(self, token):
        r'''Is true when typed collection container `token`.
        Otherwise false.

        Returns boolean.
        '''
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __eq__(self, expr):
        r'''Is true when `expr` is a typed collection with items that compare
        equal to those of this typed collection. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self._collection == expr._collection
        elif isinstance(expr, type(self._collection)):
            return self._collection == expr
        return False

    def __format__(self, format_specification=''):
        r'''Formats typed collection.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self._collection, self.item_class, self.custom_identifier)

    def __iter__(self):
        r'''Iterates typed collection.

        Returns generator.
        '''
        return self._collection.__iter__()

    def __len__(self):
        r'''Length of typed collection.

        Returns nonnegative integer.
        '''
        return len(self._collection)

#    def __makenew__(
#        self, 
#        tokens=None, 
#        item_class=None, 
#        custom_identifier=None,
#        ):
#        r'''Makes new typed collection with optional new values.
#
#        Returns new typed collection.
#        '''
#        # allow for empty iterables
#        if tokens is None:
#            tokens = self._collection
#        item_class = item_class or self.item_class
#        custom_identifier = custom_identifier or self.custom_identifier
#        return type(self)(
#            tokens=tokens,
#            item_class=item_class,
#            custom_identifier=custom_identifier,
#            )

    def __ne__(self, expr):
        r'''Is true when `expr` is not a typed collection with items equal to 
        this typed collection. Otherwise false.

        Returns boolean.
        '''
        return not self.__eq__(expr)

    ### PRIVATE METHODS ###

    def _on_insertion(self, item):
        r'''Override to operate on item after insertion into collection.
        '''
        pass

    def _on_removal(self, item):
        r'''Override to operate on item after removal from collection.
        '''
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        def coerce(x):
            if isinstance(x, self._item_class):
                return x
            return self._item_class(x)
        if self._item_class is None:
            return lambda x: x
        return coerce

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = list(
            manager.get_signature_keyword_argument_names(
                self))
        if 'tokens' in keyword_argument_names:
            keyword_argument_names.remove('tokens')
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=(
                self._collection,
                )
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = list(
            manager.get_signature_keyword_argument_names(
                self))
        if 'tokens' in keyword_argument_names:
            keyword_argument_names.remove('tokens')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=(
                self._collection,
                )
            )

    ### PUBLIC PROPERTIES ###

    @property
    def custom_identifier(self):
        r'''Gets and sets custom identifier of typed collection.

        Returns string or none.
        '''
        return self._custom_identifier

    @custom_identifier.setter
    def custom_identifier(self, custom_identifier):
        assert isinstance(custom_identifier, (str, type(None)))
        self._custom_identifier = custom_identifier

    @property
    def item_class(self):
        r'''Item class to coerce tokens into.
        '''
        return self._item_class

    @property
    def tokens(self):
        r'''Gets collection tokens.
        '''
        return [x for x in self]
