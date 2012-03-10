from abc import ABCMeta
from abc import abstractproperty
from abjad.tools.abctools.MutableAbjadObject import MutableAbjadObject


class ObjectInventory(list, MutableAbjadObject):
    '''.. versionadded:: 2.8

    Ordered collection of custom objects.

    Object inventories extend ``append()``, ``extend()`` and ``__contains__()`` and allow token input.

    Object inventories inherit from list and are mutable.

    This class is an abstract base class that can not instantiate and should be subclassed.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    def __init__(self, tokens=None, inventory_name=None):
        list.__init__(self)
        if isinstance(tokens, type(self)):
            for token in tokens:
                self.append(self._item_class(token))
            self.inventory_name = tokens.inventory_name or inventory_name
        else:
            tokens = tokens or []
            items = []
            for token in tokens:
                items.append(self._item_class(token))
            self.extend(items)
            self.inventory_name = inventory_name

    ### OVERLOADS ###

    def __contains__(self, token):
        try:
            item = self._item_class(token)
        except ValueError:
            return False
        return list.__contains__(self, item)        

    def __repr__(self):
        if self._kwargs_string:
            return '{}({}, {})'.format(self._class_name, list.__repr__(self), self._kwargs_string)
        else:
            return '{}({})'.format(self._class_name, list.__repr__(self))

    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _contents_tools_package_qualified_repr(self):
        part_reprs = []
        for element in self:
            part_repr = getattr(element, '_tools_package_qualified_repr', repr(element))
            part_reprs.append(part_repr)
        return ', '.join(part_reprs)

    @property
    def _tools_package_qualified_repr(self):
        return '{}([{}])'.format(
            self._tools_package_qualified_class_name, self._contents_tools_package_qualified_repr)

    @abstractproperty
    def _item_class(self):
        pass

    @property
    def _kwargs_string(self):
        result = []
        if self.inventory_name:
            result.append('inventory_name={!r}'.format(self.inventory_name))
        return ', '.join(result)

    @property
    def _repr_pieces(self):
        result = []
        if len(self) == 0:
            result.append(repr(self))
        else:
            result.append('{}(['.format(self._class_name))
            for item in self[:-1]:
                repr_pieces = item._repr_pieces
                for repr_piece in repr_pieces[:-1]:
                    result.append('\t{}'.format(repr_piece))
                result.append('\t{},'.format(repr_pieces[-1]))
            for repr_piece in self[-1]._repr_pieces:
                result.append('\t{}'.format(repr_piece))
            result.append('])')
        return result

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

    ### PUBLIC METHODS ###

    def append(self, token):
        '''Change `token` to item and append.
        '''
        item = self._item_class(token)
        list.append(self, item)

    def extend(self, tokens):
        '''Change `tokens` to items and extend.
        '''
        for token in tokens:
            self.append(token)
