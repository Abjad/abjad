from abc import ABCMeta
from abc import abstractproperty
from abjad.mixins._MutableAbjadObject import _MutableAbjadObject


class ObjectInventory(list, _MutableAbjadObject):
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
        return '{}({})'.format(self.class_name, list.__repr__(self))

    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _class_name_with_tools_package(self):
        return '{}.{}'.format(self._tools_package, self.class_name)

    @property
    def _contents_repr_with_tools_package(self):
        part_reprs = []
        for element in self:
            part_repr = getattr(element, '_repr_with_tools_package', repr(element))
            part_reprs.append(part_repr)
        return ', '.join(part_reprs)

    @abstractproperty
    def _item_class(self):
        pass

    @property
    def _repr_with_tools_package(self):
        return '{}([{}])'.format(
            self._class_name_with_tools_package, self._contents_repr_with_tools_package)

    @property
    def _tools_package(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self.class_name:
                return part

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
