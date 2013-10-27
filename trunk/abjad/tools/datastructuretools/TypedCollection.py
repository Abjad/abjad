# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TypedCollection(AbjadObject):

    ### CLASS VARIABLES ### 

    __slots__ = (
        '_item_class',
        '_collection',
        '_name',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, tokens=None, item_class=None, name=None):
        assert isinstance(item_class, (type(None), type))
        self._item_class = item_class
        if isinstance(tokens, type(self)):
            name = tokens.name or name
        self.name = name

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

    def __getnewargs__(self):
        return tuple((self._collection, self.item_class, self.name))

    def __iter__(self):
        return self._collection.__iter__()

    def __len__(self):
        return len(self._collection)

    def __ne__(self, expr):
        return not self.__eq__(expr)

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
        result = AbjadObject._keyword_argument_names.fget(self)
        result = list(result)
        if 'tokens' in result:
            result.remove('tokens')
        result = tuple(result)
        return result

    ### PUBLIC METHODS ###

    def new(self, tokens=None, item_class=None, name=None):
        # Allow for empty iterables:
        if tokens is None:
            tokens = self._collection
        item_class = item_class or self.item_class
        name = name or self.name
        return type(self)(
            tokens=tokens,
            item_class=item_class,
            name=name,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Item class to coerce tokens into.
        '''
        return self._item_class

    @apply
    def name():
        def fget(self):
            r'''Read / write name of typed tuple.
            '''
            return self._name
        def fset(self, _name):
            assert isinstance(_name, (str, type(None)))
            self._name = _name
        return property(**locals())

    @property
    def storage_format(self):
        r'''Storage format of typed tuple.
        '''
        return self._tools_package_qualified_indented_repr
