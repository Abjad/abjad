# -*- encoding: utf-8 -*-
import types
from abjad.tools.abctools.AbjadObject import AbjadObject


class ObjectInventory(AbjadObject):
    '''Ordered collection of objects, which optionally coerces its contents
    to the same type:

    ::

        >>> object_inventory = datastructuretools.ObjectInventory()
        >>> object_inventory.append(23)
        >>> object_inventory.append('foo')
        >>> object_inventory.append(False)
        >>> object_inventory.append((1, 2, 3))
        >>> object_inventory.append(3.14159)
        >>> z(object_inventory)
        datastructuretools.ObjectInventory([
            23,
            'foo',
            False,
            (1, 2, 3),
            3.14159
            ])

    ::

        >>> pitch_inventory = datastructuretools.ObjectInventory(
        ...     item_class=pitchtools.NamedChromaticPitch)
        >>> pitch_inventory.append(0)
        >>> pitch_inventory.append("d'")
        >>> pitch_inventory.append(('e', 4))
        >>> pitch_inventory.append(pitchtools.NamedChromaticPitch("f'"))
        >>> z(pitch_inventory)
        datastructuretools.ObjectInventory([
            pitchtools.NamedChromaticPitch("c'"),
            pitchtools.NamedChromaticPitch("d'"),
            pitchtools.NamedChromaticPitch("e'"),
            pitchtools.NamedChromaticPitch("f'")
            ],
            item_class=pitchtools.NamedChromaticPitch
            )

    Implements the list interface.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_item_class',
        '_list',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        assert isinstance(item_class, (type(None), type))
        self._item_class = item_class
        self._list = []
        if isinstance(tokens, type(self)):
            for token in tokens:
                self.append(self._item_callable(token))
            self.name = tokens.name or name
        else:
            tokens = tokens or []
            items = []
            for token in tokens:
                items.append(self._item_callable(token))
            self.extend(items)
            self.name = name

    ### SPECIAL METHODS ###

    def __contains__(self, token):
        '''Change `token` to item and return true if item exists in inventory:

        ::

            >>> pitchtools.NamedChromaticPitch("c'") in pitch_inventory
            True

        ::

            >>> pitchtools.NamedChromaticPitch("d'") in pitch_inventory
            True

        ::

            >>> pitchtools.NamedChromaticPitch("e'") in pitch_inventory
            True

        Return boolean.
        '''
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return self._list.__contains__(item)

    def __delitem__(self, i):
        del(self._list[i])

    def __eq__(self, expr):
        '''Compares equally with other object inventories, or lists with
        identical contents:

        ::
        
            >>> object_inventory == object_inventory
            True

        ::

            >>> object_inventory == [23, 'foo', False, (1, 2, 3), 3.14159]
            True

        ::

            >>> object_inventory == pitch_inventory
            False

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            return self._list == expr._list
        elif isinstance(expr, type(self._list)):
            return self._list == expr
        return False

    def __getitem__(self, i):
        return self._list[i]

    def __iadd__(self, expr):
        '''Change tokens in `expr` to items and extend:

        ::

            >>> dynamic_inventory = datastructuretools.ObjectInventory(
            ...     item_class=contexttools.DynamicMark)
            >>> dynamic_inventory.append('ppp')
            >>> dynamic_inventory += ['p', 'mp', 'mf', 'fff']
            >>> z(dynamic_inventory)
            datastructuretools.ObjectInventory([
                contexttools.DynamicMark(
                    'ppp',
                    target_context=stafftools.Staff
                    ),
                contexttools.DynamicMark(
                    'p',
                    target_context=stafftools.Staff
                    ),
                contexttools.DynamicMark(
                    'mp',
                    target_context=stafftools.Staff
                    ),
                contexttools.DynamicMark(
                    'mf',
                    target_context=stafftools.Staff
                    ),
                contexttools.DynamicMark(
                    'fff',
                    target_context=stafftools.Staff
                    )
                ],
                item_class=contexttools.DynamicMark
                )

        Return inventory.
        '''
        self.extend(expr)
        return self

    def __iter__(self):
        return self._list.__iter__()

    def __len__(self):
        return len(self._list)

    def __reversed__(self):
        return self._list.__reversed__()

    def __setitem__(self, i, expr):
        '''Change tokens in `expr` to items and set:

        ::

            >>> pitch_inventory[-1] = 'gqs,'
            >>> z(pitch_inventory)
            datastructuretools.ObjectInventory([
                pitchtools.NamedChromaticPitch("c'"),
                pitchtools.NamedChromaticPitch("d'"),
                pitchtools.NamedChromaticPitch("e'"),
                pitchtools.NamedChromaticPitch('gqs,')
                ],
                item_class=pitchtools.NamedChromaticPitch
                )

        ::

            >>> pitch_inventory[-1:] = ["f'", "g'", "a'", "b'", "c''"]
            >>> z(pitch_inventory)
            datastructuretools.ObjectInventory([
                pitchtools.NamedChromaticPitch("c'"),
                pitchtools.NamedChromaticPitch("d'"),
                pitchtools.NamedChromaticPitch("e'"),
                pitchtools.NamedChromaticPitch("f'"),
                pitchtools.NamedChromaticPitch("g'"),
                pitchtools.NamedChromaticPitch("a'"),
                pitchtools.NamedChromaticPitch("b'"),
                pitchtools.NamedChromaticPitch("c''")
                ],
                item_class=pitchtools.NamedChromaticPitch
                )

        '''
        if isinstance(i, int):
            item = self._item_callable(expr)
            self._list[i] = item
        elif isinstance(i, slice):
            items = [self._item_callable(token) for token in expr]
            self._list[i] = items

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        if self._item_class is None:
            return lambda x: x
        return self._item_class

    @property
    def _keyword_argument_names(self):
        result = AbjadObject._keyword_argument_names.fget(self)
        result = list(result)
        if 'tokens' in result:
            result.remove('tokens')
        result = tuple(result)
        return result

    @property
    def _positional_argument_repr_string(self):
        positional_argument_repr_string = [
            repr(x) for x in self._positional_argument_values]
        positional_argument_repr_string = ', '.join(
            positional_argument_repr_string)
        positional_argument_repr_string = '[{}]'.format(
            positional_argument_repr_string)
        return positional_argument_repr_string

    @property
    def _positional_argument_values(self):
        return tuple(self)

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        return self._item_class

    @apply
    def name():
        def fget(self):
            r'''Read / write name of inventory.
            '''
            return self._name
        def fset(self, _name):
            assert isinstance(_name, (str, type(None)))
            self._name = _name
        return property(**locals())

    @property
    def storage_format(self):
        r'''Storage format of object inventory.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        result = []
        if is_indented:
            prefix = '\t'
        else:
            prefix = ''
        positionals = \
            self._get_tools_package_qualified_positional_argument_repr_pieces(
            is_indented=is_indented)
        keywords = \
            self._get_tools_package_qualified_keyword_argument_repr_pieces(
            is_indented=is_indented)
        positionals, keywords = list(positionals), list(keywords)
        if not positionals and not keywords:
            result.append('{}([])'.format(
                self._tools_package_qualified_class_name))
        elif not positionals and keywords:
            result.append('{}([],'.format(
                self._tools_package_qualified_class_name))
            keywords[-1] = keywords[-1].rstrip(' ')
            keywords[-1] = keywords[-1].rstrip(',')
            result.extend(keywords)
            result.append('{})'.format(prefix))
        elif positionals and not keywords:
            result.append('{}(['.format(
                self._tools_package_qualified_class_name))
            positionals[-1] = positionals[-1].rstrip(' ')
            positionals[-1] = positionals[-1].rstrip(',')
            result.extend(positionals)
            result.append('{}])'.format(prefix))
        elif positionals and keywords:
            result.append('{}(['.format(
                self._tools_package_qualified_class_name))
            positionals[-1] = positionals[-1].rstrip(' ')
            positionals[-1] = positionals[-1].rstrip(',')
            result.extend(positionals)
            result.append('{}],'.format(prefix))
            keywords[-1] = keywords[-1].rstrip(' ')
            keywords[-1] = keywords[-1].rstrip(',')
            result.extend(keywords)
            result.append('{})'.format(prefix))
        else:
            raise ValueError("how'd we get here?")
        return result

    ### PUBLIC METHODS ###

    def append(self, token):
        r'''Change `token` to item and append.
        '''
        item = self._item_callable(token)
        self._list.append(item)

    def count(self, token):
        r'''Change `token` to item and return count.
        '''
        item = self._item_callable(token)
        return self._list.count(item)

    def extend(self, tokens):
        r'''Change `tokens` to items and extend.
        '''
        for token in tokens:
            self.append(token)

    def index(self, token):
        r'''Change `token` to item and return index.
        '''
        item = self._item_callable(token)
        return self._list.index(item)

    def insert(self, i, token):
        r'''Change `token` to item and insert.
        '''
        item = self._item_callable(token)
        return self._list.insert(i, item)

    def pop(self, i=-1):
        r'''Pop item at index `i`.
        '''
        return self._list.pop(i)

    def remove(self, token):
        r'''Change `token` to item and remove.
        '''
        item = self._item_callable(token)
        self._list.remove(item)

    def reverse(self):
        r'''Reverse items in place.
        '''
        self._list.reverse()

    def sort(self, cmp=None, key=None, reverse=False):
        r'''Sort items in place.
        '''
        self._list.sort(cmp=cmp, key=key, reverse=reverse)
