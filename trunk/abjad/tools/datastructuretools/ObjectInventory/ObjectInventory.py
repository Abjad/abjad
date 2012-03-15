from abjad.tools.abctools.AbjadObject import AbjadObject


class ObjectInventory(list, AbjadObject):
    '''.. versionadded:: 2.8

    Ordered collection of custom objects.

    Object inventories extend ``append()``, ``extend()`` and ``__contains__()`` and allow token input.

    Object inventories inherit from list and are mutable.

    This class is an abstract base class that can not instantiate and should be subclassed.
    '''

    ### INITIALIZER ###

    def __init__(self, tokens=None, inventory_name=None):
        list.__init__(self)
        if isinstance(tokens, type(self)):
            for token in tokens:
                self.append(self._item_callable(token))
            self.inventory_name = tokens.inventory_name or inventory_name
        else:
            tokens = tokens or []
            items = []
            for token in tokens:
                items.append(self._item_callable(token))
            self.extend(items)
            self.inventory_name = inventory_name

    ### SPECIAL METHODS ###

    def __contains__(self, token):
        try:
            item = self._item_callable(token)
        except ValueError:
            return False
        return list.__contains__(self, item)        

    def __repr__(self):
        return AbjadObject.__repr__(self)

    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _item_callable(self):
        return lambda x: x

    @property
    def _keyword_argument_names(self):
        return (
            'inventory_name',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            list(self),
            ) 

    ### READ / WRITE PUBLIC ATTRIBUTES ###

    @apply
    def inventory_name():
        def fget(self):
            '''Read / write name of inventory.
            '''
            return self._inventory_name
        def fset(self, _inventory_name):
            assert isinstance(_inventory_name, (str, type(None)))
            self._inventory_name = _inventory_name
        return property(**locals())

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        result = []
        if len(self) == 0:
            result.append(repr(self))
        else:
            if is_indented:
                prefix = '\t'
            else:
                prefix = ''
            result.append('{}(['.format(self._tools_package_qualified_class_name))
            for item in self[:-1]:
                if hasattr(item, '_get_tools_package_qualified_repr_pieces'):
                    repr_pieces = item._get_tools_package_qualified_repr_pieces(is_indented=is_indented)
                    for repr_piece in repr_pieces[:-1]:
                        result.append('{}{}'.format(prefix, repr_piece))
                    if is_indented:
                        result.append('{}{},'.format(prefix, repr_pieces[-1]))
                    else:
                        result.append('{}{}, '.format(prefix, repr_pieces[-1]))
                else:
                    if is_indented:
                        result.append('{}{},'.format(prefix, repr(item)))
                    else:
                        result.append('{}{}, '.format(prefix, repr(item)))
            if hasattr(self[-1], '_get_tools_package_qualified_repr_pieces'):
                for repr_piece in self[-1]._get_tools_package_qualified_repr_pieces(is_indented=is_indented):
                    result.append('{}{}'.format(prefix, repr_piece))
            else:
                result.append('{}{}'.format(prefix, repr(self[-1])))
            result.append('{}])'.format(prefix))
        return result

    ### PUBLIC METHODS ###

    def append(self, token):
        '''Change `token` to item and append.
        '''
        item = self._item_callable(token)
        list.append(self, item)

    def extend(self, tokens):
        '''Change `tokens` to items and extend.
        '''
        for token in tokens:
            self.append(token)
