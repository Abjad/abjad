# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TypedCollection(AbjadObject):
    r'''Abstract base class for typed collections.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_collection',
        '_item_class',
        '_custom_identifier',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, tokens=None, item_class=None, custom_identifier=None):
        assert isinstance(item_class, (type(None), type))
        self._item_class = item_class
        if isinstance(tokens, type(self)):
            custom_identifier = tokens.custom_identifier or custom_identifier
        self.custom_identifier = custom_identifier

    ### SPECIAL METHODS ###

    def __contains__(self, token):
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return self._collection.__contains__(item)

    def __eq__(self, expr):
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
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    def __getnewargs__(self):
        return (self._collection, self.item_class, self.custom_identifier)

    def __iter__(self):
        return self._collection.__iter__()

    def __len__(self):
        return len(self._collection)

    def __ne__(self, expr):
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
    def _keyword_argument_names(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        names = manager.get_signature_keyword_argument_names(self)
        names = list(names)
        if 'tokens' in names:
            names.remove('tokens')
        names = tuple(names)
        return names

    @property
    def _positional_argument_repr_string(self):
        positional_argument_repr_string = [
            repr(x) for x in self]
        positional_argument_repr_string = ', '.join(
            positional_argument_repr_string)
        positional_argument_repr_string = '[{}]'.format(
            positional_argument_repr_string)
        return positional_argument_repr_string

    @property
    def _positional_argument_values(self):
        return [list(self)]

    @property
    def _tokens_brace_characters(self):
        return ('[', ']')

    ### PUBLIC METHODS ###

    def new(self, tokens=None, item_class=None, custom_identifier=None):
        # Allow for empty iterables:
        if tokens is None:
            tokens = self._collection
        item_class = item_class or self.item_class
        custom_identifier = custom_identifier or self.custom_identifier
        return type(self)(
            tokens=tokens,
            item_class=item_class,
            custom_identifier=custom_identifier,
            )

    ### PUBLIC PROPERTIES ###

    @apply
    def custom_identifier():
        def fget(self):
            r'''Read / write custom identifier of typed collection.
            '''
            return self._custom_identifier
        def fset(self, _custom_identifier):
            assert isinstance(_custom_identifier, (str, type(None)))
            self._custom_identifier = _custom_identifier
        return property(**locals())

    @property
    def item_class(self):
        r'''Item class to coerce tokens into.
        '''
        return self._item_class
