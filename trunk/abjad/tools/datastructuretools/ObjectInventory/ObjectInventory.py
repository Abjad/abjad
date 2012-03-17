from abjad.tools.abctools.AbjadObject import AbjadObject
import types


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

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _item_callable(self):
        return lambda x: x

    @property
    def _keyword_argument_names(self):
        result = []
        result.extend([
            'inventory_name',
            ])
        return result

    @property
    def _mandatory_argument_repr_string(self):
        mandatory_argument_repr_string = [repr(x) for x in self._mandatory_argument_values]
        mandatory_argument_repr_string = ', '.join(mandatory_argument_repr_string)
        mandatory_argument_repr_string = '[{}]'.format(mandatory_argument_repr_string)
        return mandatory_argument_repr_string

    @property
    def _mandatory_argument_values(self):
        return tuple(self)

    ### PUBLIC READ / WRITE ATTRIBUTES ###

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
        if is_indented:
            prefix = '\t'
        else:
            prefix = ''
        mandatories = self._get_tools_package_qualified_mandatory_argument_repr_pieces(is_indented=is_indented)
        keywords = self._get_tools_package_qualified_keyword_argument_repr_pieces(is_indented=is_indented)
        if not mandatories and not keywords:
            result.append('{}([])'.format(self._tools_package_qualified_class_name))
        elif not mandatories and keywords:
            result.append('{}([],'.format(self._tools_package_qualified_class_name))
            keywords[-1] = keywords[-1].rstrip(' ')
            keywords[-1] = keywords[-1].rstrip(',')
            result.extend(keywords)
            result.append('{})'.format(prefix))
        elif mandatories and not keywords:
            result.append('{}(['.format(self._tools_package_qualified_class_name))
            mandatories[-1] = mandatories[-1].rstrip(' ')
            mandatories[-1] = mandatories[-1].rstrip(',')
            result.extend(mandatories)
            result.append('{}])'.format(prefix))
        elif mandatories and keywords:
            result.append('{}(['.format(self._tools_package_qualified_class_name))
            mandatories[-1] = mandatories[-1].rstrip(' ')
            mandatories[-1] = mandatories[-1].rstrip(',')
            result.extend(mandatories)
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
        '''Change `token` to item and append.
        '''
        item = self._item_callable(token)
        list.append(self, item)

    def extend(self, tokens):
        '''Change `tokens` to items and extend.
        '''
        for token in tokens:
            self.append(token)
